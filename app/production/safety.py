from app.production.settings import get_production_settings

def safety_check():
    s = get_production_settings()
    issues = []

    if s.app_env != "production":
        issues.append("APP_ENV is not production.")

    if not s.dry_run and not s.shopify_token_set:
        issues.append("DRY_RUN=false but Shopify token is not set.")

    if s.autonomy_enabled and s.dry_run:
        issues.append("AUTONOMY_ENABLED=true while DRY_RUN=true. This is safe but not live.")

    if s.autonomy_enabled and s.emergency_stop:
        issues.append("Autonomy enabled but emergency stop is active.")

    if s.max_daily_spend <= 0:
        issues.append("MAX_DAILY_SPEND must be greater than zero.")

    if s.min_margin_percent < 10:
        issues.append("MIN_MARGIN_PERCENT is dangerously low.")

    if s.max_risk_score > 70:
        issues.append("MAX_RISK_SCORE is too permissive.")

    ready_for_dry_run = len([i for i in issues if "DRY_RUN=false" in i]) == 0
    ready_for_live = (
        not s.dry_run
        and s.shopify_token_set
        and s.shopify_store_url_set
        and not s.emergency_stop
        and s.max_daily_spend > 0
        and s.min_margin_percent >= 20
        and s.max_risk_score <= 60
    )

    return {
        "ready_for_dry_run": ready_for_dry_run,
        "ready_for_live": ready_for_live,
        "issues": issues,
        "settings": s.__dict__,
    }
