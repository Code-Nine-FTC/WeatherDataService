# -*- coding: utf-8 -*-
from fastapi import APIRouter

router = APIRouter(tags=["example"], prefix="/example")


@router.get("/")
def hello_world() -> dict[str, str]:
    return {"msg": "Hello World"}
