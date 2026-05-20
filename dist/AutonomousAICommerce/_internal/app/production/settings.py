import os
from dataclasses import dataclass

def bool_env(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() in ("1", "true", "yes", "on")

def float_env(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except Exception:
        return default

@dataclass
class ProductionSettings:
    app_env: str
    dry_run: bool
    autonomy_enabled: bool
    emergency_stop: bool
    database_url: str
    max_daily_spend: float
    max_single_order_spend: float
    min_margin_percent: float
    max_risk_score: float
    shopify_store_url_set: bool
    shopify_token_set: bool
    openai_key_set: bool
    supplier_mode: str
    shipping_mode: str

def get_production_settings() -> ProductionSettings:
    return ProductionSettings(
        app_env=os.getenv("APP_ENV", "local"),
        dry_run=bool_env("DRY_RUN", True),
        autonomy_enabled=bool_env("AUTONOMY_ENABLED", False),
        emergency_stop=bool_env("EMERGENCY_STOP", False),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./commerce.db"),
        max_daily_spend=float_env("MAX_DAILY_SPEND", 250),
        max_single_order_spend=float_env("MAX_SINGLE_ORDER_SPEND", 50),
        min_margin_percent=float_env("MIN_MARGIN_PERCENT", 25),
        max_risk_score=float_env("MAX_RISK_SCORE", 45),
        shopify_store_url_set=bool(os.getenv("SHOPIFY_STORE_URL", "")),
        shopify_token_set=bool(os.getenv("SHOPIFY_ACCESS_TOKEN", "")),
        openai_key_set=bool(os.getenv("OPENAI_API_KEY", "")),
        supplier_mode=os.getenv("SUPPLIER_MODE", "sandbox"),
        shipping_mode=os.getenv("SHIPPING_MODE", "sandbox"),
    )
