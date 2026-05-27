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

run_step("refresh_shopify_token","python -m app.refresh_shopify_token")
run_step("shopify_crm_events","python -m app.shopify_crm_events")
run_step("crm_personalized_drafts","python -m app.crm_personalized_drafts")
run_step("crm_readiness_summary","python -m app.crm_readiness_summary")

run_step("etsy_connection_status","python -m app.etsy_connection_status")
run_step("etsy_autopilot","python -m app.etsy_autopilot")

run_step("exploration_engine_v2","python -m app.exploration_engine_v2")
run_step("build_priority_queue","python -m app.build_priority_queue")
run_step("publish_execution_plan","python -m app.publish_execution_plan")
run_step("action_executor","python -m app.action_executor")
run_step("social_content_generator","python -m app.social_content_generator")
run_step("social_content_enhancer","python -m app.social_content_enhancer")
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
