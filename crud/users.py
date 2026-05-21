# 用户相关数据库操作

import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from models.users import User, UserToken
from schemas.users import UserUpdateRequest
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from utils import security


# 异常类
class UserAlreadyExistsError(Exception):
    pass
    # def __init__(self, username: str):
    #     super().__init__(f"用户已存在: {username}")
    #     self.username = username


# 创建用户
async def create_user(db: AsyncSession, username: str, password: str) -> User:
    # 密码加密处理
    user = User(username=username, password=security.get_hash_password(password))
    db.add(user)
    try:
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError as exc:
        await db.rollback()
        raise UserAlreadyExistsError(username) from exc


# 根据用户名查询用户
async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 根据用户ID查询用户
async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 查询所有用户
async def get_all_users(db: AsyncSession):
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()


# 生成 Token
async def create_token(db: AsyncSession, user_id: int) -> str:
    # 生成令牌 + 设置过期时间 → 查询数据库当前用户是否有 Token → 有：更新 Token → 无：创建 Token
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()
    return token


# 验证用户
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user


# 根据 Token 查询用户： 验证 Token → 查询用户
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if not user_token or user_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == user_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 更新用户信息
async def update_user(
    db: AsyncSession, username: str, user_data: UserUpdateRequest
) -> User:
    # update(User).where(User.username == username).values(字段=值，字段=值)
    # user_data 是一个 pydantic 类型，包含了用户需要更新的信息，得到字典 → ** 解包
    # 没有设置值的不更新
    query = (
        update(User)
        .where(User.username == username)
        .values(**user_data.model_dump(exclude_unset=True, exclude_none=True))
    )
    result = await db.execute(query)
    await db.commit()

    # 检查更新
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 获取更新后的用户信息
    update_user = await get_user_by_username(db, username)
    return update_user


# 修改密码：验证旧密码 → 新密码加密 → 更新密码
async def change_password(
    db: AsyncSession,
    old_password: str,
    new_password: str,
    user: User,
) -> User:
    if not security.verify_password(old_password, user.password):
        return False
    hash_new_password = security.get_hash_password(new_password)
    user.password = hash_new_password
    # 更新： 由 SQLAlchemy 真正接管这个 User 对象，确保可以 commit
    # 规避 session 过期或者关闭导致的不能提交问题
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True
