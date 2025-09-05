from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings):
    APP_DEBUG: bool = True
    APP_PORT: int = 3000
    APP_HOST: str = "0.0.0.0"
    POSTGRES_HOST: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    @computed_field
    @property
    def DATABASE_URL(self) -> str: # pylint: disable=invalid-name
        return (
        "postgresql+psycopg2://" +
        f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@" +
        f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    )

    class Config:
        env_file = ".env"

settings = Settings()
