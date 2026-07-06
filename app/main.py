"""FastAPI 主应用入口"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time

from app.core.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} 启动中...")
    # TODO: 初始化数据库连接、Redis连接、各平台SDK
    yield
    logger.info("🛑 应用关闭，清理资源...")


app = FastAPI(
    title="电商智能客服Agent",
    description="覆盖淘宝/拼多多/京东/抖音等主流平台的智能客服系统",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求耗时中间件
@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed = time.time() - start
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    if elapsed > 5:
        logger.warning(f"慢请求: {request.method} {request.url.path} 耗时 {elapsed:.2f}s")
    return response


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"未处理异常: {request.method} {request.url.path} - {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误", "error": str(exc) if settings.DEBUG else "Internal Server Error"},
    )


# ========== 路由注册 ==========

from app.api.health import router as health_router
from app.api.webhooks import router as webhook_router
from app.api.tools import router as tools_router
from app.api.risk import router as risk_router

app.include_router(health_router, tags=["健康检查"])
app.include_router(webhook_router, prefix="/webhook", tags=["平台Webhook"])
app.include_router(tools_router, prefix="/api/tools", tags=["Agent工具"])
app.include_router(risk_router, prefix="/api/risk", tags=["风控评估"])


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }
