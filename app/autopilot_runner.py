import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime, timezone

OUT=Path("app/logs/autopilot_run_report.json")

steps=[
    "app.token_manager",
    "app.oauth_reauth_required",
    "app.shopify_registry_hydrator",
    "app.registry_quality_report",
    "app.feed_mass_regenerator",
    "app.feed_channel_validation",
    "app.real_sales_collector",
    "app.shopify_order_address_collector",
    "app.autonomous_order_router",
    "app.supplier_purchase_executor",
    "app.cj_supplier_readiness",
    "app.cj_order_draft_creator",
    "app.cj_payload_builder",
    "app.cj_customer_address_validator",
    "app.sales_cleanup",
    "app.real_sales_mode",
    "app.traffic_mode",
    "app.google_ads_readiness",
    "app.meta_ads_readiness",
    "app.meta_token_validation",
    "app.paid_ads_status",
    "app.traffic_readiness",
    "app.multi_market_scanner",
    "app.global_arbitrage_engine",
    "app.global_execution_plan",
    "app.real_traffic_launcher",
    "app.campaign_executor",
    "app.ad_campaign_executor",
    "app.meta_campaign_live_creator",
    "app.meta_campaign_registry_sync",
    "app.google_campaign_live_creator",
    "app.click_tracking_init",
    "app.event_collector_state",
    "app.meta_test_event",
    "app.event_learning_sync",
    "app.seo_quality_score",
    "app.hunter_feedback_engine",
    "app.hunter_registry_sync",
    "app.hunter_action_plan",
    "app.hunter_action_executor",
    "app.dynamic_product_score",
    "app.dynamic_score_sync",
    "app.tier_summary",
    "app.tier_strategy_apply",
    "app.autonomous_loop_health",
    "app.channel_validation_checkpoint",
    "app.final_system_checkpoint",
    "app.external_platform_blockers",
    "app.global_commerce_control_panel"
]

results=[]

print("AUTOPILOT START")

for step in steps:

    print("="*60)
    print("RUN:",step)

    started_at=datetime.now(timezone.utc).isoformat()

    proc=subprocess.run(
        [sys.executable,"-m",step],
        capture_output=True,
        text=True
    )

    result={
        "step":step,
        "ok":proc.returncode==0,
        "returncode":proc.returncode,
        "started_at":started_at,
        "finished_at":datetime.now(timezone.utc).isoformat(),
        "stdout":proc.stdout[-3000:],
        "stderr":proc.stderr[-3000:]
    }

    results.append(result)

    if proc.stdout:
        print(proc.stdout)

    if proc.stderr:
        print("STDERR:")
        print(proc.stderr)

    if proc.returncode!=0:
        print("AUTOPILOT STOPPED AT:",step)
        break

OUT.write_text(
    json.dumps(results,indent=2),
    encoding="utf-8"
)

ok=sum(1 for x in results if x["ok"])

print("="*60)
print("AUTOPILOT COMPLETE")
print("STEPS OK:",ok,"/",len(steps))
print("REPORT:",OUT)

mode_path=Path("app/logs/real_sales_mode.json")

if mode_path.exists():
    mode=json.loads(mode_path.read_text(encoding="utf-8"))
    print("REAL SALES MODE:",mode.get("mode"))
    print("SAFE TO UPDATE ROI:",mode.get("safe_to_update_roi"))




















