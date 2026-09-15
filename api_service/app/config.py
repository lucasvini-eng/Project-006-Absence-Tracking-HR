from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+psycopg2://ausencia_user:ausencia_pass@db:5432/ausencia_rh"
    )
    api_debug: bool = True

    class Config:
        env_prefix = ""
        env_file = ".env"
        extra = "ignore"


settings = Settings()
