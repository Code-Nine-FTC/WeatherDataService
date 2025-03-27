from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserViewResponse(BaseModel):
    name: str
    email: str
    last_update: datetime

    model_config = ConfigDict(from_attributes=True)
