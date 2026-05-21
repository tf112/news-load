# 根据 Token 查询用户，返回用户
from config.db_conf import get_db
from crud import users
from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user(
    authorization: str = Header(default=..., alias="Authorization"),
    db: AsyncSession = Depends(get_db),
):
    """验证 Token 并返回当前用户，兼容 Bearer 和纯 token 两种格式"""
    # 兼容两种格式：Bearer xxx 或 xxx
    if authorization.startswith("Bearer "):
        token = authorization[7:]  # 去掉 "Bearer " 前缀
    else:
        token = authorization

    user = await users.get_user_by_token(db, token)

    if not user:
        raise HTTPException(status_code=401, detail="用户不存在或密码错误")
    return user