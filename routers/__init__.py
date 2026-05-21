"""
Author: 花生
description: 接口实现流程
1. 模块化路由 → API 接口规范文档
2. 定义模型类 → 数据库表(数据库设计文档)
3. 在 CRUD 文件夹里面创建文件，封装操作数据库的方法
4. 在路由处理函数里面调用 CRUD 封装好的方法，响应结果
"""

from fastapi import APIRouter

# 引入模块路由
from routers.favorite import router as favorite_router
from routers.news import router as news_router
from routers.users import router as users_router

# 创建 APIRouter 实例
api_router = APIRouter(prefix="/api")

# prefix 路由前缀(API 接口规范文档)
# tags 分组 标签


# 注册各模块路由
api_router.include_router(news_router, prefix="/news", tags=["新闻"])
api_router.include_router(users_router, prefix="/user", tags=["用户"])
api_router.include_router(favorite_router, prefix="/favorite", tags=["收藏"])
