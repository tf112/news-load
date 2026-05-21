# 成功响应函数
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(message: str = "success", data: object = None):

    content = {"code": 200, "message": message, "data": data}
    # 目标： 把任何的 FastAPI、Pydantic、ORM 对象，都要正常响应 → code、message、data
    return JSONResponse(content=jsonable_encoder(content))
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": "token",
    #         "userInfo": {
    #             "id": "new_user.id",
    #             "username": "new_user.username",
    #             "bio": "new_user.bio",
    #             "avatar": "new_user.avatar",
    #         },
    #     },
    # }
