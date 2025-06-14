from datetime import datetime, timezone

import pytest

from app.modules.common import ConvertDates

pytestmark = pytest.mark.unit


# ---------- Teste convert ----------


def test_convert_str_dates_to_datetime() -> None:
    input_data = {
        "initial_date": "2025-05-21",
        "last_data": "2025-06-01",
        "last_update": "2025-06-02",
        "other_field": "no_change",
    }

    result = ConvertDates.convert(input_data.copy())

    assert isinstance(result["initial_date"], datetime)
    assert result["initial_date"] == datetime(2025, 5, 21)
    assert isinstance(result["last_data"], datetime)
    assert result["last_data"] == datetime(2025, 6, 1)
    assert isinstance(result["last_update"], datetime)
    assert result["last_update"] == datetime(2025, 6, 2)

    assert result["other_field"] == "no_change"


def test_convert_with_missing_fields() -> None:
    input_data = {"other_field": "no_change"}

    result = ConvertDates.convert(input_data.copy())

    assert result == input_data


# ---------- Teste unix_to_datetime ----------


def test_unix_to_datetime_valid() -> None:
    unixtime = 1716240000
    dt = ConvertDates.unix_to_datetime(unixtime)

    assert isinstance(dt, datetime)
    assert dt == datetime.fromtimestamp(unixtime, tz=timezone.utc)


def test_unix_to_datetime_invalid() -> None:
    unixtime = "not_an_int"
    dt = ConvertDates.unix_to_datetime(unixtime)

    assert dt is None
