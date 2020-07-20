from fastapi import APIRouter, Form
from ext import templates
from starlette.requests import Request

app = APIRouter()


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("form_post.html", {"request": request})


@app.post("/users/",name="表单提交用户名密码")
async def users(username: str = Form(...,description="用户名",example="wushiqian"),
                password: str = Form(...,description="密码",example="apple2882960")):
    return {"username": username, "password": password}
