# 数据库配置文件

import os

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# # 数据库配置


class Settings(BaseSettings):
    """
    Author: 花生
    description: 应用配置，优先读取环境变量，否则使用默认值
    return {*}
    """

    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = os.getenv("DB_PORT", 3306)
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str = os.getenv("DB_PASSWORD", "root")
    db_name: str = os.getenv("DB_NAME", "news_app")
    # 应用配置
    app_name: str = os.getenv("APP_NAME", "News App")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"

    @property
    def DATABASE_URL(self) -> str:
        """构造异步数据连接字符串"""
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"
        )

    class Config:
        # 自动从 .env 获取配置
        env_file = ".env"
        env_file_encoding = "utf-8"


# 实例化全局配置对象
settings = Settings()


# 创建异步数据库引擎
async_engine = create_async_engine(
    settings.DATABASE_URL, echo=settings.debug, pool_size=10, max_overflow=20
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    # bind=async_engine, class_=async_engine, expire_on_commit=False
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# 依赖注入：获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
