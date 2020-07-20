from fastapi import APIRouter, status, Response, Request, HTTPException

app = APIRouter()


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}


@app.get("/items/get", status_code=201)
async def create_item_get(name: str):
    return {"name": name}


@app.post("/items2/", status_code=status.HTTP_201_CREATED)
async def create_item2(name: str):
    return {"name": name}


@app.post("/items3/", status_code=status.HTTP_401_UNAUTHORIZED)
async def create_item3(name: str, response: Response):
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"name": name}


@app.post("/items4/", status_code=status.HTTP_404_NOT_FOUND)
async def create_item4(name: str):
    return {"name": name}


items = {"foo": "The Foo Wrelers"}


@app.get("/items/{item_id}")
def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="item not found",
            headers={"X-Error": "There goes my error"})
    return items[item_id]


from .error import UnicornException


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


@app.get("/unicorn/httperror/{item_id}")
async def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=418, detail="item_id can not be 0")
    return {"item_id": item_id}
