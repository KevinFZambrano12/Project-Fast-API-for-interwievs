from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.interviews import router as interviews_router

from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Interviewing Platform API",
        version="1.0.0",
        docs_url="/docs",       # Swagger
        redoc_url="/redoc"      # ReDoc
    )

    # --- CORS (important for frontend apps like React) ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Routers ---
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(interviews_router)

    # --- Health check (Cloud Run uses this) ---
    @app.get("/healthz", tags=["infra"])
    def health_check():
        return {"status": "ok"}

    return app


app = create_app()
