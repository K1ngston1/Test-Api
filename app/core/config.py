from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "mysql"
    DB_PORT: int = 3306
    DB_NAME: str = "test_db"
    DB_USER: str = "admin"
    DB_PASSWORD: str = "admin123"

    AUTO_CREATE_TABLES: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()