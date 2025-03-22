from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class UserViewResponse(BaseModel):
    name: str
    email: str
    last_update: str

    @field_validator("last_update", mode="before")
    def parse_last_update(cls, value: str | datetime) -> str:
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value

    model_config = ConfigDict(from_attributes=True)
