from fastapi import APIRouter, Query
from ext import templates
from pydantic import BaseModel
from datetime import date
from starlette.requests import Request

app = APIRouter()


class User(BaseModel):
    id: int
    name: str
    joined: date


@app.get("/", name="首页", tags=["首页"])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
