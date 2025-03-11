# -*- coding: utf-8 -*-
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BasicResponse(BaseModel, Generic[T]):
    data: T | None = None

    class Config:
        arbitrary_types_allowed = True
