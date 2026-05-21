# 新闻相关数据库操作

from models.news import Category, News
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


# 新闻列表
async def get_news_list(
    db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10
):
    # 查询指定分类下的所有新闻
    newsList = (
        select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    )
    result = await db.execute(newsList)
    return result.scalars().all()


# 获取新闻数据总量
async def get_new_count(db: AsyncSession, category_id: int):
    # 查询指定分类下的新闻数量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  # 只能有一个结果，否则报错


# 查询新闻详情
async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 增加浏览量
async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    # 更新 → 检测数据库是否真的命中了数据 → 命中了返回 True
    return result.rowcount > 0


# 同类新闻推荐
async def get_related_news(
    db: AsyncSession, category_id: int, news_id: int, limit: int = 5
):
    stmt = (
        select(News)
        .where(News.category_id == category_id, News.id != news_id)
        .order_by(
            News.views.desc(),  # 默认升序，使用 desc() 降序
            News.publish_time.desc(),  # 发布时间
        )
        .limit(limit)
    )
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    # 列表推导式，推出新闻核心数据，返回新闻列表
    return [
        {
            "id": news.id,
            "title": news.title,
            "content": news.content,
            "image": news.image,
            "author": news.author,
            "publishTime": news.publish_time,
            "categoryId": news.category_id,
            "views": news.views,
        }
        for news in related_news
    ]

    # return result.scalars().all()
