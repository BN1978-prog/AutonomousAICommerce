from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Autonomous AI Commerce System"
    env: str = "development"
    database_url: str = "sqlite:///./commerce.db"

    openai_api_key: str | None = None
    shopify_store_domain: str | None = None
    shopify_admin_access_token: str | None = None

    max_daily_spend: float = 250
    min_net_margin_percent: float = 25
    max_supplier_risk: int = 60
    max_country_risk: int = 70
    emergency_stop: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
