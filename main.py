# 应用入口文件

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from routers import api_router
from utils.exception_handlers import register_exception_handlers

# 创建 Bearer 安全方案（仅用于 Swagger UI 显示）
swagger_security = HTTPBearer(
    scheme_name="Bearer Token",
    description="输入 Token（无需 Bearer 前缀）",
    auto_error=False,  # 不自动报错，由 auth.py 处理
)

app = FastAPI(
    title="头条项目 API",
    description="后端接口文档",
    version="1.0.0",
    dependencies=[Depends(swagger_security)],  # 全局安全依赖
)

# 注册全局异常处理
register_exception_handlers(app)

# 注册路由
app.include_router(api_router)

# 允许跨域请求地址
CORS_URLS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://192.168.1.99:5173",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_URLS,  # 允许的源，开发阶段可以设置为 "*"，生产环境可以设置为具体的域名
    allow_credentials=True,  # 允许携带 cookie
    allow_methods=["*"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头
)
