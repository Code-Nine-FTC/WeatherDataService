from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


class DashboardService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_station_history(self, station_id: int) -> list[Row]:
        base_query = text("""
            SELECT
                m.value,
                m.measure_date,
                pt.name,
                pt.measure_unit
            FROM measures m
            JOIN parameters p ON m.parameter_id = p.id
            JOIN parameter_types pt ON p.parameter_type_id = pt.id
            WHERE p.station_id = :station_id
            ORDER BY m.measure_date DESC
        """)

        result = await self._session.execute(base_query, {"station_id": station_id})
        return result.fetchall()

    async def get_alert_type_distribution(self) -> list[Row]:
        query = text("""
            SELECT
                ta.name AS name,
                COALESCE(COUNT(a.id), 0) AS total
            FROM
                type_alerts ta
            LEFT JOIN
                alerts a ON a.type_alert_id = ta.id AND a.is_read = false
            WHERE
                ta.is_active = true AND ta.status = 'R' OR ta.status = 'Y'
            GROUP BY
                ta.name
            ORDER BY
                total DESC
        """)
        result = await self._session.execute(query)
        return result.fetchall()

    async def get_alert_counts(self) -> dict[str, int]:
        queries = {
            "R": (
                "SELECT COUNT(*) AS total "
                "FROM alerts a "
                "JOIN type_alerts ta ON a.type_alert_id = ta.id "
                "WHERE ta.status = 'R' AND a.is_read = false;"
            ),
            "Y": (
                "SELECT COUNT(*) AS total "
                "FROM alerts a "
                "JOIN type_alerts ta ON a.type_alert_id = ta.id "
                "WHERE ta.status = 'Y' AND a.is_read = false"
            ),
            "G": (
                "SELECT COUNT(*) AS total "
                "FROM alerts a "
                "JOIN type_alerts ta ON a.type_alert_id = ta.id "
                "WHERE ta.status = 'G' AND a.is_read = false"
            ),
        }
        counts = {}
        for key, query in queries.items():
            result = await self._session.execute(text(query))
            counts[key] = result.scalar()
        return counts

    async def get_station_status(self) -> dict[str, int]:
        total_query = "SELECT COUNT(*) AS total FROM weather_stations;"
        active_query = "SELECT COUNT(*) AS total FROM weather_stations WHERE is_active = true;"

        total_result = await self._session.execute(text(total_query))
        active_result = await self._session.execute(text(active_query))

        return {
            "total": total_result.scalar(),
            "active": active_result.scalar(),
        }

    async def get_measures_status(self) -> list[Row]:
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
