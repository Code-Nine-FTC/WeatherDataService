# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    password: str
    email: str
    last_update: datetime
