# 收藏相关API路由
from config.db_conf import get_db
from crud import favorite
from fastapi import APIRouter, Query
from fastapi.params import Depends
from models.users import User
from schemas.favorite import FavoriteAddRequest, FavoriteCheckResponseBase
from sqlalchemy.ext.asyncio import AsyncSession
from utils import auth, response

router = APIRouter()


# 检查收藏状态
@router.get("/check")
async def check_favorite(
    db: AsyncSession = Depends(get_db),
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(auth.get_current_user),
):
    is_favorite = await favorite.is_news_favorite(db, user.id, news_id)
    return response.success_response(
        message="检查收藏状态成功",
        data=FavoriteCheckResponseBase(is_favorite=is_favorite),
    )


# 添加收藏
@router.post("/add")
async def add_favorite(
    data: FavoriteAddRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth.get_current_user),
):
    is_favorite = await favorite.is_news_favorite(db, user.id, data.news_id)
    if is_favorite:
        return response.success_response(message="已收藏")
    result = await favorite.add_news_favorite(db, user_id=user.id, news_id=data.news_id)
    return response.success_response(message="添加收藏成功", data=result)


# 取消收藏
@router.delete("/remove")
async def remove_favorite(
    news_id: int = Query(..., alias="newsId"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth.get_current_user),
):
    result = await favorite.remove_news_favorite(db, user.id, news_id)
    return response.success_response(message="取消收藏成功", data=result)
