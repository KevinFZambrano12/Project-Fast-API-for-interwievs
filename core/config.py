from pydantic import BaseSettings

class Settings(BaseSettings):
    CORS_ORIGINS: list[str] = ["*"]  # or your domain
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
