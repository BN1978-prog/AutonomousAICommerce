from fastapi import APIRouter
from app.production.settings import get_production_settings
from app.production.safety import safety_check
from app.production.logging_config import get_logger

router = APIRouter()
logger = get_logger("production")

@router.get("/status")
def production_status():
    s = get_production_settings()
    return {
        "production_layer": "installed",
        "settings": s.__dict__,
    }

@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "AutonomousAICommerce",
        "production_layer": True,
    }

@router.get("/config-check")
def config_check():
    s = get_production_settings()
    return {
        "database": "postgresql" if s.database_url.startswith("postgresql") else "sqlite",
        "shopify_configured": s.shopify_store_url_set and s.shopify_token_set,
        "openai_configured": s.openai_key_set,
        "supplier_mode": s.supplier_mode,
        "shipping_mode": s.shipping_mode,
        "dry_run": s.dry_run,
        "autonomy_enabled": s.autonomy_enabled,
    }

@router.get("/safety-check")
def check_safety():
    return safety_check()

@router.post("/log-test")
def log_test():
    logger.info("Production log test event")
    return {"logged": True}
