from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_router
from app.core.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle.
    """
    create_tables()
    yield


app = FastAPI(
    title="ScamShield API",
    description=(
        "ScamShield — Intelligent Scam Detection and Digital Trust "
        "Platform by Team Obsidian."
    ),
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "project": "ScamShield",
        "team": "OBSIDIAN",
        "status": "online",
        "version": "0.2.0",
        "message": "ScamShield API is running.",
    }


app.include_router(
    api_router,
    prefix="/api/v1",
)
