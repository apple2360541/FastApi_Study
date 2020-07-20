from fastapi import APIRouter, Path, Body, Form
from typing import Optional, Set, List, Dict
from ext import templates

from uuid import UUID
from uuid import uuid1
from datetime import datetime, time, timedelta
from pydantic import BaseModel, Field, HttpUrl
from starlette.requests import Request

app = APIRouter()


class Item(BaseModel):
    name: str = Field(..., description="名字", example="吴世芊")
    price: float = Field(..., description="价格", example=32.5, gt=10, lt=100)
    is_offer: Optional[bool] = None
    tags1: list = []
    tags2: List[str] = []
    tags3: Set[str] = []


class User(BaseModel):
    username: str = Field(None, description="用户名", example="wsq")
    password: str = Field(None, description="密码", example="*****")


class Image(BaseModel):
    url: HttpUrl = Field(..., example="http://www.baidu.com/")
    name: str


class ImageItem(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: Set[str] = {}  # 创建一个空集合必须用set() 而不是{}
    image: Image = None
    images: List[Image] = None


@app.post("/image/items/")
def image_items(item: ImageItem):
    return item


@app.post("/image/create/")
def create_images(images: List[Image]):
    return images


# {
#   "additionalProp1": 0,
#   "additionalProp2": 0,
#   "additionalProp3": 0
# }

@app.post("/weight/")
async def create_weight(weights: Dict[int, float]):
    return weights


@app.get("/items/{item_id}")
def read_item(item_id: int = Path(..., ge=0, le=10000), q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/")
async def create_item(item: Item):
    print(item.dict())
    # return
    # [
    #     {
    #         "name": "吴世芊",
    #         "price": 32.5,
    #         "is_offer": true
    #     },
    #     "人生没有无意义的经历"
    # ]
    return item, "人生没有无意义的经历"


@app.put("/item1/{item_id}")
def update_item(item_id: int, item: Item = Body(..., embed=True), q: str = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


# {
#   "item": {
#     "name": "吴世芊",
#     "price": 32.5,
#     "is_offer": true
#   },
#   "user": {
#     "username": "string",
#     "password": "string"
#   }
# }
# 两个body embed=False不起作用
@app.delete("/items2/{item_id}/")
def update_item(item_id: int,
                item: Item = Body(..., embed=False),
                user: User = Body(..., embed=False,
                                  example={"username": "wushiqian",
                                           "password": "apple2882960"}
                                  )):
    return item


# [
#   1,
#   {
#     "name": "吴世芊",
#     "price": 32.5,
#     "is_offer": true
#   }
# ]


# {
#   "item": {
#     "name": "吴世芊",
#     "price": 32.5,
#     "is_offer": true
#   }
# }
@app.post("/items3/{item_id}/")
def update_item(item_id: int, item: Item = Body(..., embed=True)):
    return item


@app.get("/user/")
async def post_user(request: Request):
    return templates.TemplateResponse("post.html", {"request": request})


@app.post("/user/")
async def post_user(request: Request, username: str = Form(...),
                    password: str = Form(...)):
    return templates.TemplateResponse("user.html",
                                      {"request": request,
                                       "username": username,
                                       "password": password})
