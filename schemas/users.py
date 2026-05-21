# 用户数据验证模型
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserRequest(BaseModel):
    username: str
    password: str = Field(..., min_length=6, max_length=20, description="密码")


# user_info 对应类：基础类 + Info类 (id、用户名)
class userInfoBase(BaseModel):
    """用信息基础数据类型"""

    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(
        None,
        max_length=10,
        description="性别",
    )
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")


class UserInfoResponse(userInfoBase):
    id: int
    username: str
    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,  # alias 字段名兼容
        from_attributes=True,  # 允许从 ORM 对象属性中取值
    )


# 返回 data 的数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,  # alias 字段名兼容
        from_attributes=True,  # 允许从 ORM 对象属性中取值
    )


# 更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None


# 更新用户密码的模型类
class UserPasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    new_password: str = Field(
        ...,
        min_length=6,
        alias="newPassword",
        description="新密码",
    )
