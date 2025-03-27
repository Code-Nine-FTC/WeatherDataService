# -*- coding: utf-8 -*-
from pydantic import BaseModel


class RequestAlert(BaseModel):
    id: int
