import traceback

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status

# 开发者模式：返回详细错误信息
# 生产模式：返回简化错误信息
DEBUG_MODE = True  # 当前保持开启


def _format_validation_message(exc: RequestValidationError) -> str:
    error = exc.errors()[0]
    field = error.get("loc", [])[-1]
    error_type = error.get("type")
    ctx = error.get("ctx", {})

    if field == "newPassword" and error_type == "string_too_short":
        return f"新密码长度不能少于{ctx.get('min_length', 6)}位"

    return error.get("msg", "请求参数错误")


# 处理 HTTPException 异常，返回 JSON 格式的响应
async def http_exception_handler(request: Request, exc: HTTPException):
    # HTTPException 通常是业务逻辑主动抛出的，data 保持 None
    if DEBUG_MODE:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "code": exc.status_code,
                "message": exc.detail,
                "data": None,
            },
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"},
        )


# 处理请求参数校验错误
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": "RequestValidationError",
            "errors": exc.errors(),
            "path": str(request.url),
        }
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 400,
            "message": _format_validation_message(exc),
            "data": error_data,
        },
    )


# 处理数据库完整性约束
async def integrity_error_handler(request: Request, exc: IntegrityError):
    error_msg = str(exc.orig)

    # 判断具体的约束错误类型
    if "user_news_unique" in error_msg:
        detail = "已收藏该新闻"
    elif "username_UNIQUE" in error_msg:
        detail = "用户名已存在"
    elif "Duplicate entry" in error_msg:
        detail = "数据已存在"
    elif "FOREIGN KEY" in error_msg:
        detail = "关键数据不存在"
    else:
        detail = "数据约束冲突，请检查输入数据"

    # 开发模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": "IntegrityError",
            "error_detail": error_msg,
            "path": str(request.url),
        }
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": 400, "message": detail, "data": error_data},
    )


# 处理 SQLAlchemy 数据库错误
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    # 开发模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),  # 格式化异常信息为字符串，方便日志记录和调试
            "path": str(request.url),
        }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "数据库操作错误，请检查日志",
            "data": error_data,
        },
    )


# 处理所有未捕获的异常
async def general_exception_handler(request: Request, exc: Exception):
    # 开发者模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),  # 格式化异常信息为字符串，方便日志记录和调试
            "path": str(request.url),
        }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"code": 500, "message": "服务器内部错误", "data": error_data},
    )
