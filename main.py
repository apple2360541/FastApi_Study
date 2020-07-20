from fastapi import FastAPI, status
from starlette.staticfiles import StaticFiles

from routers.cookie_header import app as cookie_demo
from routers.file import file
from routers.home import app as home
from routers.path_body import app as PathDemo
from routers.query import app as QueryDemo
from routers.response import app as response_demo
from routers.status_error import app as status_error
from routers.form_file import app as form_demo
from routers.json_decoder import app as json_demo
from routers.user import router as user
from routers.auth_security import app as security
from routers.depends import app as depends_demo

app = FastAPI(version="1.0.0")
app.include_router(home, prefix="", tags=["首页"])
app.include_router(QueryDemo, prefix="", tags=["查询参数demo"])
app.include_router(PathDemo, prefix="", tags=["路径和body参数"])
app.include_router(user, prefix="/user", tags=["用户"])
app.include_router(file, prefix="", tags=["文件处理"])
app.include_router(cookie_demo, prefix="/cookie", tags=["Cookie和Header"])
app.include_router(response_demo, prefix="/response", tags=["Response例子"])
app.include_router(status_error, prefix="/status", tags=["状态和错误处理"])
app.include_router(form_demo, prefix="/form", tags=["表单和file"])
app.include_router(json_demo, prefix="/json", tags=["JsonEncoder"])
app.include_router(depends_demo, prefix="/depends", tags=["依赖注入"])
app.include_router(security, prefix="/security", tags=["Security认证"])

app.mount("/static", StaticFiles(directory="static"), name="static")

from routers.error import UnicornException
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    print("unicor_exception_handler")
    return JSONResponse(status_code=418, content={"message": f"Oops!{exc.name} did something. There goes a rainbow..."})


# 覆盖默认的异常处理程序
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print("http_exception_handler")
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# 验证异常
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("validation_exception_handler")
    from fastapi.encoders import jsonable_encoder
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    )


from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG An Http error!:{exc}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception(request, exc):
    print(f"OMG The client sent invalid data!:{exc}")
    return await request_validation_exception_handler(request, exc)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
