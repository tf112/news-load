# 收藏相关数据库操作
from models.favorite import Favorite
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


# 检查收藏状态： 当前用户是否收藏了该新闻
async def is_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    query = select(Favorite).where(
        Favorite.user_id == user_id, Favorite.news_id == news_id
    )
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None


# 添加收藏
async def add_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


# 取消收藏
async def remove_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    # 1. 查询当前用户是否收藏了该新闻
    query = delete(Favorite).where(
        Favorite.user_id == user_id, Favorite.news_id == news_id
    )
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0
