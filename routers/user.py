from fastapi import APIRouter, Form
from starlette.requests import Request
from ext import templates

router = APIRouter()


@router.get("/index/")
def user_index():
    return {"user": " user index"}


@router.get("/list/")
def user_list(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user": "吴世芊"})


@router.get("/list/{user_id}")
def user_list(request: Request, user_id: str = None):
    return templates.TemplateResponse("index.html", {"request": request, "user_id": user_id})


@router.post("/user/")
async def files(request: Request,
                username: str = Form(...),
                password: str = Form(...)):
    print("username", username)
    print("password", password)
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "username": username
                                       })
@router.get("/login/")
async def login(request:Request):
    return templates.TemplateResponse("sigin.html",{"request":request})
