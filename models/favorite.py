# 收藏数据模型
from datetime import datetime
from sqlalchemy import UniqueConstraint, Index, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from models.news import News
from models.users import User


class Base(DeclarativeBase):
    pass


# 收藏表 ORM 模型
class Favorite(Base):
    __tablename__ = "favorite"

    # 创建索引
    __table_args__ = (
        UniqueConstraint(
            "news_id", "user_id", name="user_news_unique"
        ),  # UniqueConstraint  唯一约束
        Index("fk_favorite_user_idx", "user_id"),
        Index("fk_favorite_news_idx", "news_id"),
    )
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="收藏ID"
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(User.id), nullable=False, comment="用户ID"
    )
    news_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(News.id), nullable=False, comment="新闻ID"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), comment="收藏时间"
    )

    def __repr__(self):
        return f"Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, created_at={self.created_at})"
