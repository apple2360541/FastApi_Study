from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = APIRouter()
fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    print(item)
    print(type(item))
    json_compatible_item_data = jsonable_encoder(item)
    print(json_compatible_item_data)
    print(type(json_compatible_item_data))
    fake_db[id] = json_compatible_item_data
    print(type(fake_db))
    return fake_db


class Items(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Items)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Items)
async def update_item(item_id: str, item: Items):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded


@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item



