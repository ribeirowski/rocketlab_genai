import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import health_router, agent_router, history_router, feedback_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Text-to-SQL Agent for e-commerce data analysis.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router.router, prefix="/api/v1")
    app.include_router(agent_router.router, prefix="/api/v1")
    app.include_router(history_router.router, prefix="/api/v1")
    app.include_router(feedback_router.router, prefix="/api/v1")
    
    @app.get("/", include_in_schema=False)
    async def root():
        return {
            "app": get_settings().APP_NAME,
            "version": get_settings().APP_VERSION,
            "status": "online",
            "docs": "/docs",
        }

    logger.info("Application started: %s v%s", settings.APP_NAME, settings.APP_VERSION)

    return app

app = create_app()