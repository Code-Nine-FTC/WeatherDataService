from datetime import datetime, timezone
from typing import Any, Sequence

from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


class DashboardService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_station_history(
        self, station_id: int, start_date: str | None = None, end_date: str | None = None
    ) -> Sequence[Row[Any]]:
        base_query = [
            """
            SELECT
                m.value,
                m.measure_date,
                pt.name AS title,
                pt.measure_unit,
                pt.detect_type AS type
            FROM measures m
            JOIN parameters p ON m.parameter_id = p.id
            JOIN parameter_types pt ON p.parameter_type_id = pt.id
        """
        ]

        where_conditions = []
        final_params = {"station_id": station_id}
        where_conditions.append("p.station_id = :station_id")

        start_epoch = self._parse_date_to_epoch(start_date)
        if start_epoch is not None:
            where_conditions.append("m.measure_date >= :start_date_epoch")
            final_params["start_date_epoch"] = start_epoch

        end_epoch = self._parse_date_to_epoch(end_date)
        if end_epoch is not None:
            if end_date and len(end_date) == 10:
                try:
                    datetime.strptime(end_date, "%Y-%m-%d")
                    end_epoch += (24 * 60 * 60) - 1
                except ValueError:
                    pass

            where_conditions.append("m.measure_date <= :end_date_epoch")
            final_params["end_date_epoch"] = end_epoch

        if where_conditions:
            base_query.append("WHERE " + " AND ".join(where_conditions))

        base_query.append("ORDER BY m.measure_date DESC")

        final_sql_string = " ".join(base_query)

        query = text(final_sql_string)
        result = await self._session.execute(query, final_params)
        return result.fetchall()

    async def get_alert_type_distribution(
        self, station_id: int | None = None
    ) -> Sequence[Row : [Any]]:
        params = {}
        sql_query = """
            SELECT
                ta.name AS name,
                COALESCE(COUNT(a.id), 0) AS total
            FROM
                type_alerts ta
            JOIN
                parameters p ON ta.parameter_id = p.id
            LEFT JOIN
                alerts a ON a.type_alert_id = ta.id AND a.is_read = false
        """

        where_clauses = ["ta.is_active = true"]

        if station_id is not None:
            where_clauses.append("p.station_id = :station_id")
            params["station_id"] = station_id

        if where_clauses:
            sql_query += " WHERE " + " AND ".join(where_clauses)

        sql_query += """
            GROUP BY
                ta.name
            ORDER BY
                total DESC
        """

        query = text(sql_query)
        result = await self._session.execute(query, params)
        return result.fetchall()

    async def get_alert_counts(self, station_id: int | None) -> dict[str, int]:
        base_params = {}

        station_join_clause = ""
        station_where_clause = ""
        if station_id is not None:
            station_join_clause = " JOIN parameters p ON ta.parameter_id = p.id"
            station_where_clause = " AND p.station_id = :station_id"
            base_params["station_id"] = station_id

        queries = {
            "R": (
                "SELECT COUNT(*) AS total "
                "FROM alerts a "
                "JOIN type_alerts ta ON a.type_alert_id = ta.id "
                f"{station_join_clause} "
                f"WHERE ta.status = 'R' AND a.is_read = false{station_where_clause}"
            ),
            "Y": (
                "SELECT COUNT(*) AS total "
                "FROM alerts a "
                "JOIN type_alerts ta ON a.type_alert_id = ta.id "
                f"{station_join_clause} "
                f"WHERE ta.status = 'Y' AND a.is_read = false{station_where_clause}"
            ),
            "G": (
                "SELECT COUNT(*) AS total "
                "FROM alerts a "
                "JOIN type_alerts ta ON a.type_alert_id = ta.id "
                f"{station_join_clause} "
                f"WHERE ta.status = 'G' AND a.is_read = false{station_where_clause}"
            ),
        }
        counts = {}
        for key, query in queries.items():
            result = await self._session.execute(text(query), base_params)
            counts[key] = result.scalar()
        return counts

    async def get_station_status(self) -> dict[str, int]:
        total_query = "SELECT COUNT(*) AS total FROM weather_stations;"
        active_query = "SELECT COUNT(*) AS total FROM weather_stations WHERE is_active = true;"

        total_result = await self._session.execute(text(total_query))
        active_result = await self._session.execute(text(active_query))

        return {
            "total": total_result.scalar() or 0,
            "active": active_result.scalar() or 0,
        }

    async def get_measures_status(self) -> list[Row[Any]]:
        query = text("""
            SELECT
                pt.name AS label,
                COUNT(m.id) AS number
            FROM measures m
            JOIN parameters p ON m.parameter_id = p.id
            JOIN parameter_types pt ON p.parameter_type_id = pt.id
            GROUP BY pt.name
        """)
        result = await self._session.execute(query)
        return result.fetchall()

    async def get_last_measures(self, station_id: int) -> list[Row[Any]]:
        query = text("""
            SELECT
                pt.name AS title,
                m.value AS value,
                pt.measure_unit AS measure_unit,
                pt.detect_type AS type,
                m.measure_date AS measure_date
            FROM measures m
            JOIN parameters p ON m.parameter_id = p.id
            JOIN parameter_types pt ON p.parameter_type_id = pt.id
            WHERE
                p.station_id = :station_id
                AND m.measure_date = (
                    SELECT MAX(m2.measure_date)
                    FROM measures m2
                    WHERE m2.parameter_id = p.id
                )
        """)
        result = await self._session.execute(query, {"station_id": station_id})
        return list(result.fetchall())

    def _parse_date_to_epoch(self, date_str: str | None) -> int | None:
        if date_str is None:
            return None
        try:
            dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return int(dt_obj.replace(tzinfo=timezone.utc).timestamp())
        except ValueError:
            try:
                return int(date_str)
            except ValueError:
                return None
