from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings with safe defaults for local development."""

    app_name: str = "Autonomous AI Commerce System"
    environment: str = Field(default="development")
    database_url: str = Field(default="sqlite:///./commerce.db")

    default_currency: str = Field(default="GBP", min_length=3, max_length=3)
    min_margin_percent: float = Field(default=25.0, ge=0.0, le=95.0)
    max_daily_spend: float = Field(default=250.0, ge=0.0)
    max_order_value: float = Field(default=50.0, ge=0.0)
    max_supplier_risk_score: float = Field(default=0.35, ge=0.0, le=1.0)
    max_return_risk_score: float = Field(default=0.30, ge=0.0, le=1.0)
    enable_autonomous_purchase: bool = False

    # Optional live Shopify connector settings. If missing, Shopify adapter runs in safe sandbox mode.
    shopify_store_domain: str | None = None
    shopify_admin_access_token: str | None = None
    shopify_api_version: str = "2025-01"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
