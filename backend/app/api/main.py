from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import trip
from app.config import settings

app = FastAPI(
    title="智能旅行助手 API",
    description="基于多阶段规划编排的旅行规划服务",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trip.router, prefix="/api/trip", tags=["trip"])
