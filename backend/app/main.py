from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import init_db
from app.routers import plans, projects, timer, statistics, accounting, accounts


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await init_db()
    yield
    # Shutdown


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="FocusFlow - All-in-One Productivity Management System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(plans.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(timer.router, prefix="/api/v1")
app.include_router(statistics.router, prefix="/api/v1")
app.include_router(accounting.router, prefix="/api/v1")
app.include_router(accounts.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Welcome to FocusFlow API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
