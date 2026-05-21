# 收藏数据验证模型

from pydantic import BaseModel, ConfigDict, Field


class FavoriteCheckResponseBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    is_favorite: bool = Field(..., description="是否收藏", alias="isFavorite")


# 添加收藏的请求提类型
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., description="新闻ID", alias="newsId")
