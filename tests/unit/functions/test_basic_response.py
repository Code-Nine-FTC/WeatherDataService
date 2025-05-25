import pytest
from pydantic import BaseModel

from app.modules.basic_response import BasicResponse

pytestmark = pytest.mark.unit


class Item(BaseModel):
    id: int
    name: str


def test_basic_response_with_model() -> None:
    item = Item(id=1, name="Test")
    response: BasicResponse[Item] = BasicResponse(data=item)

    assert response.data == item
    assert isinstance(response.data, Item)


def test_basic_response_with_iterable() -> None:
    items = [Item(id=1, name="Test1"), Item(id=2, name="Test2")]
    response: BasicResponse[list[Item]] = BasicResponse(data=items)

    assert response.data is not None
    assert hasattr(response.data, "__iter__")
    assert all(isinstance(i, Item) for i in response.data)


def test_basic_response_with_none() -> None:
    response: BasicResponse[None] = BasicResponse(data=None)

    assert response.data is None
