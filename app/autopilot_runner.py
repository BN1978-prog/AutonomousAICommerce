from app.send_telegram_alert import send_alert
import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

LOG = Path("app/logs/autopilot_run.json")
LOG.parent.mkdir(parents=True, exist_ok=True)

result = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "smart_autopilot_with_exploration_and_crm",
    "steps": []
}


def run_step(name, command, allow_codes=None):
    if allow_codes is None:
        allow_codes=[0]

    p=subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    status="OK" if p.returncode in allow_codes else "ERROR"

    if name=="daily_publish_guard" and p.returncode==10:
        status="SKIPPED_ALREADY_PUBLISHED_TODAY"

    result["steps"].append({
        "name":name,
        "returncode":p.returncode,
        "status":status,
        "stdout":p.stdout,
        "stderr":p.stderr
    })

    return p.returncode


def shopify_catalog_ok():
    try:
        import requests
        r = requests.get(
            "http://127.0.0.1:8000/dashboard/shopify/catalog-health",
            timeout=5
        )
        return r.ok and bool(r.json().get("ok"))
    except Exception:
        return False


run_step("railway_health_check","python -m app.railway_health_check")
run_step("token_manager","python -m app.token_manager")
run_step("refresh_ebay_token","python -m app.refresh_ebay_token", allow_codes=[0,1])
run_step("google_ads_token_refresher","python -m app.google_ads_token_refresher")
run_step("meta_token_refresh","python -m app.meta_token_refresh")
run_step("meta_page_token_refresh","python -m app.meta_page_token_refresh")
run_step("amazon_token_refresher","python -m app.amazon_token_refresher")
run_step("shopify_crm_events","python -m app.shopify_crm_events")
run_step("real_sales_collector","python -m app.real_sales_collector")
run_step("cj_paid_order_fulfillment","python -m app.cj_paid_order_fulfillment")
run_step("crm_personalized_drafts","python -m app.crm_personalized_drafts")
run_step("crm_readiness_summary","python -m app.crm_readiness_summary")

run_step("etsy_connection_status","python -m app.etsy_connection_status")
run_step("etsy_autopilot","python -m app.etsy_autopilot")

run_step("real_trend_discovery","python -m app.real_trend_discovery")
run_step("autonomous_trend_filter","python -m app.autonomous_trend_filter")
run_step("exploration_engine_v2","python -m app.exploration_engine_v2")
run_step("build_priority_queue","python -m app.build_priority_queue")
run_step("publish_execution_plan","python -m app.publish_execution_plan")
run_step("trend_listing_validator","python -m app.trend_listing_validator")
run_step("cj_trend_bridge","python -m app.cj_trend_bridge")
run_step("supplier_candidate_filter","python app/filter_supplier_candidates.py")
run_step("seo_product_optimizer","python -m app.seo_product_optimizer")
run_step("profit_checked_products","python -m app.profit_checked_products")
run_step("action_executor","python -m app.action_executor")
run_step("social_content_generator","python -m app.social_content_generator")
run_step("social_content_enhancer","python -m app.social_content_enhancer")
run_step("auto_publish_or_fallback","python -m app.auto_publish_or_fallback")
run_step("meta_ad_drafts_from_content","python -m app.meta_ad_drafts_from_content")
run_step("google_ad_drafts_from_content","python -m app.google_ad_drafts_from_content")
run_step("campaign_hub","python -m app.campaign_hub")
run_step("campaign_approval_queue","python -m app.campaign_approval_queue")

guard=run_step(
    "daily_publish_guard",
    "python -m app.daily_publish_guard",
    allow_codes=[0,10]
)

run_step("system_status_report","python -m app.system_status_report")

run_step("daily_summary","python -m app.daily_summary")

run_step("auto_scaling_score","python -m app.auto_scaling_score")

run_step("product_guardrails","python -m app.product_guardrails")

run_step("roi_simulation","python -m app.roi_simulation")

run_step("ceo_dashboard","python -m app.ceo_dashboard")
run_step("auto_launch_engine","python -m app.auto_launch_engine")

run_step("auto_spend_executor","python -m app.auto_spend_executor")

run_step("spend_history_tracker","python -m app.spend_history_tracker")

run_step("negative_roi_auto_pause","python -m app.negative_roi_auto_pause")

run_step("hourly_budget_monitor","python -m app.hourly_budget_monitor")

run_step("emergency_stop_validator","python -m app.emergency_stop_validator")

run_step("live_spend_permission_gate","python -m app.live_spend_permission_gate")

run_step("live_backend_router","python -m app.live_backend_router")

run_step("meta_live_campaign_builder","python -m app.meta_live_campaign_builder")

run_step("google_live_campaign_builder","python -m app.google_live_campaign_builder")

run_step("live_campaign_registry","python -m app.live_campaign_registry")

run_step("live_api_execution_gate","python -m app.live_api_execution_gate")

run_step("live_execution_reporter","python -m app.live_execution_reporter")

run_step("live_mode_final_lock","python -m app.live_mode_final_lock")
run_step("meta_long_lived_token","python -m app.meta_long_lived_token")
run_step("meta_live_executor","python -m app.meta_live_executor")

run_step("google_live_executor","python -m app.google_live_executor")

run_step("live_execution_consolidator","python -m app.live_execution_consolidator")

run_step("live_spend_audit_ledger","python -m app.live_spend_audit_ledger")
run_step("live_spend_audit_reader","python -m app.live_spend_audit_reader")
run_step("send_daily_summary","python -m app.send_daily_summary")

run_step("send_telegram_summary","python -m app.send_telegram_summary")



LOG.write_text(
    json.dumps(result,indent=2),
    encoding="utf-8"
)

print(json.dumps(result,indent=2))
















run_step("customer_fulfillment_support_status","python -m app.customer_fulfillment_support_status")








run_step("env_backup_sync","powershell Copy-Item .env .env.backup -Force")


run_step("env_channel_recovery","python -m app.env_channel_recovery")
if not shopify_catalog_ok():
    run_step("refresh_shopify_token","python -m app.refresh_shopify_token")
else:
    result["steps"].append({
        "name": "refresh_shopify_token",
        "returncode": 0,
        "status": "SKIPPED_SHOPIFY_ALREADY_OK",
        "stdout": "Shopify catalog-health ok; refresh skipped",
        "stderr": ""
    })
run_step("railway_env_sync","python -m app.railway_env_sync")
run_step("listing_publish_execution_plan_real","python -m app.listing_publish_execution_plan_real")
run_step("marketplace_listing_publisher","python -m app.marketplace_listing_publisher")
run_step("draft_listing_activation_plan","python -m app.draft_listing_activation_plan")
run_step("draft_listing_activator","python -m app.draft_listing_activator")
run_step("marketplace_order_autobuy","python -m app.marketplace_order_autobuy")
run_step("autonomous_fulfillment_status","python -m app.autonomous_fulfillment_status")




