from fastapi import APIRouter, Depends

app = APIRouter()


# 被依赖项必须是可调用的类、函数、包等
async def common_parameters(q: str = None, skip: int = 0, limit: int = 10):
    limit += 66
    return {"q": q, "skip": skip, "limit": limit}


class CommonQueryParams:
    def __init__(self, q: str = None, skip: int = 0, limit: int = 10):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_iems(commons: dict = Depends(common_parameters)):
    commons['skip'] += 10
    return commons


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/users/")
def get_users(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items})
    return response
