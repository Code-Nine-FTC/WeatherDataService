from datetime import datetime

from app.modules.common import ConvertDates


def test_unix_to_datetime() -> None:
    timestamp = 1712553600
    result = ConvertDates.unix_to_datetime(timestamp)
    assert isinstance(result, datetime)
    assert result.isoformat().startswith("2024-04-08")
