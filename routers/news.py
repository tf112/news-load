# 新闻相关API路由

from config.db_conf import get_db
from crud import news
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# 获取新闻分类列表
@router.get("/categories")
async def get_categories(
    skip: int = Query(default=0, description="请输入页码"),
    limit: int = Query(default=100, description="请输入分页大小"),
    # skip: int = 0,
    # limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "msg": "获取分类成功",
        "data": categories,
    }


# 获取新闻列表
@router.get("/list")
async def get_news_list(
    db: AsyncSession = Depends(get_db),
    category_id: int = Query(..., description="请输入分类ID", alias="categoryId"),
    page: int = Query(default=1, description="请输入页码"),
    page_size: int = Query(default=10, description="请输入分页大小", alias="pageSize"),
):
    # 思路：处理分页规则 → 查询新闻列表 → 计算总量 → 计算是否还有更多
    skip = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, skip, page_size)
    total = await news.get_new_count(db, category_id)
    hasMore = skip + len(news_list) < total
    return {
        "code": 200,
        "msg": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": hasMore,
        },
    }


# 获取新闻详情
@router.get("/detail")
async def read_news_detail(
    db: AsyncSession = Depends(get_db), news_id: int = Query(..., alias="id")
):
    # 获取新闻详情 + 浏览量+1 + 相关新闻
    detail = await news.get_news_detail(db, news_id)
    if not detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    views_res = await news.increase_news_views(db, news_id)
    if not views_res:
        raise HTTPException(status_code=404, detail="新闻不存在")

    related_news = await news.get_related_news(db, detail.category_id, news_id)

    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": detail.id,
            "title": detail.title,
            "content": detail.content,
            "image": detail.image,
            "author": detail.author,
            "publishTime": detail.publish_time,
            "categoryId": detail.category_id,
            "views": detail.views,
            "relatedNews": related_news,
        },
    }
