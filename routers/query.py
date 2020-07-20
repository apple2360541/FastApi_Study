from fastapi import APIRouter, Query
from typing import Optional, List
from enum import Enum

app = APIRouter()


class Name(str, Enum):
    Allan = "张三"
    Jon = "李四"
    Bob = "王五"


@app.get("/{who}")
async def get_day(who: Name):
    if who == Name.Allan:
        return {"who": who, "message": "张三是德国人"}
    elif who.value == "李四":
        return {"who": who, "message": "李四是英国人"}
    else:
        return {"who": who, "message": "王五是法国人"}


@app.get("/items/{item_id}")
def read_item(item_id: int = Query(None, ge=0, le=10000),
              q: Optional[str] = Query(None, min_length=3, max_length=15)):
    return {"item_id": item_id, "q": q}


# http://127.0.0.1:8000/items3/?q=a&q=d&q=c
@app.get("/items3/")
async def read_items3(q: List[str] = Query(["a", "b", ])):
    query_items = {"q": q}
    return query_items


@app.get("/items4/")
async def read_items4(q: str = Query(None, title="q title",alias="item_query", description="条目查询")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
