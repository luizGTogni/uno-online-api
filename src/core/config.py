from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_DEBUG: bool = True
    APP_PORT: int = 3000
    APP_HOST: str = "0.0.0.0"
    DATABASE_URL: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
