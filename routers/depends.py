from fastapi import APIRouter, Depends, Cookie, Header, HTTPException

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


def query_extractor(q: str = None):
    return q


def query_or_cookie_extractor(q: str = Depends(query_extractor), last_query: str = Cookie(None)):
    if not q:
        return last_query
    return q


@app.get("/items/more_depend/")
async def more_depend(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/read/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
