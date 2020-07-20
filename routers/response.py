from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List, Union, Dict

app = APIRouter()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserInDb(BaseModel):
    username: str
    hash_password: str
    email: EmailStr
    full_name: Optional[str] = None


def fake_pasword_hash(raw_password: str):
    return "salt" + raw_password


def fake_save_user(user_in: UserIn):
    hash_password = fake_pasword_hash(user_in.password)
    user_in_db = UserInDb(**user_in.dict(), hash_password=hash_password)
    return user_in_db


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


# Don't do this in production!
@app.post("/user/", response_model=UserOut)
async def create_user(*, user: UserIn):
    return fake_save_user(user)


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


items2 = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


# 包含
@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"}, )
async def read_item_name(item_id: str):
    return items2[item_id]


# 不包含
@app.get("/items/{item_id}/public",
         response_model=Item,
         response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items2[item_id]


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items3 = {
    "item1": {"description": "Foo", "type": "car"},
    "item2": {"description": "Foo", "type": "plane", "size": 8},

}


@app.get("/items/union/", response_model=Union[PlaneItem, CarItem])
def read_items(id: str):
    return items3[id]


class Image(BaseModel):
    url: HttpUrl
    name: str


items4 = [
    {"url": "http://www.baidu.com", "name": "百度"},
    {"url": "http://www.alibaba.com", "name": "阿里"},
]


@app.get("/items/list/", response_model=List[Image])
def get_images():
    return items4


@app.post("/weight/", response_model=Dict[str, float])
def weights(weights: Dict[str, float]):
    return weights
