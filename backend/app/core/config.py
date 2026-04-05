from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SnapBuy API"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./snapbuy.db"
    jwt_secret: str = "replace_me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 43200
    line_channel_access_token: str = ""
    line_channel_secret: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
