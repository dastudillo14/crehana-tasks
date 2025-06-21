import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.infrastructure.database import init_db, close_db
from src.api.routes import task_list_router, task_router
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for application lifespan events."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


# Create FastAPI app using settings
app = FastAPI(
    title=settings.APP_NAME,
    description="A clean architecture API for managing task lists and tasks",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    debug=settings.DEBUG
)

# Include routers
app.include_router(task_list_router)
app.include_router(task_router)


@app.get("/")
async def root():
    """Root endpoint for the API."""
    return JSONResponse({
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    })


@app.get("/health")
async def health():
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "service": "task-management-api"
    })


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 