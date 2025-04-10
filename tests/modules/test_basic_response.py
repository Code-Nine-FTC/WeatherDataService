from app.modules.basic_response import BasicResponse
from pydantic import BaseModel
from typing import Iterable

def test_basic_response_with_model():
    class TestModel(BaseModel):
        value: int
    data = TestModel(value=1)
    resp = BasicResponse(data=data)
    assert resp.data == data

def test_basic_response_with_iterable():
    resp = BasicResponse(data=[1, 2, 3])
    assert isinstance(resp.data, Iterable)