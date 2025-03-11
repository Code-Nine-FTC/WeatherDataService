# -*- coding: utf-8 -*-
from pydantic import BaseModel


class ResponseExempleService(BaseModel):
    value: str | None = None
