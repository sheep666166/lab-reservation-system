from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import asyncio
from app.services import reservation_service
from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.api.files import router as files_router
from app.api.lab import router as lab_router
from app.api.ai import router as ai_router
from app.api.reservation import router as reservation_router
from app.api.equipment import router as equipment_router
from app.database import Base, engine
from app.services import kb_service
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from app.common.exceptions import (
    BusinessException,
    bussiness_excpetion_hadler,
    http_excpetion_hadler,
    validation_excpetion_hadler,
    global_excpetion_hadler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
     try:
        await asyncio.to_thread(kb_service.warm_up)   # to_thread：别阻塞事件循环
     except Exception:
        logger.exception("向量库预热失败，服务继续启动")
     task = asyncio.create_task(
        reservation_service.run_expire_scan()
    )  # 启动项目开启异步的扫描任务
     yield
     task.cancel()  # 关闭项目同时取消异步任务
app  = FastAPI(lifespan=lifespan)
Base.metadata.create_all(bind=engine)
# 注册异常处理器
app.add_exception_handler(BusinessException, bussiness_excpetion_hadler)
app.add_exception_handler(HTTPException, http_excpetion_hadler)
app.add_exception_handler(RequestValidationError, validation_excpetion_hadler)
app.add_exception_handler(Exception, global_excpetion_hadler)
from starlette.middleware.cors import CORSMiddleware

origins = [
	"http://localhost:5173",
	"http://127.0.0.1:5173",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,        # 允许的前端源，不要直接写 ["*"]
	allow_credentials=True,       # ✅ 关键：允许前端携带 Authorization token
	allow_methods=["*"],          # 允许所有请求方法 GET POST PUT DELETE OPTIONS
	allow_headers=["*"],          # 允许所有请求头（包含Authorization）
)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(files_router)
app.include_router(lab_router)
app.include_router(equipment_router)
app.include_router(reservation_router)
app.include_router(ai_router)
from fastapi.staticfiles import StaticFiles

from app.config import UPLOAD_DIR

# 挂载静态资源：/uploads/xxx.jpg → uploads/xxx.jpg
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
@app.get("/")
def root():
    return {"message": "Hello FastAPI"}