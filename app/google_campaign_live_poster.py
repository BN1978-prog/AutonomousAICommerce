import json, os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from datetime import datetime, timezone

IN = Path("app/logs/google_campaign_live_creator.json")
GUARD = Path("app/logs/google_api_guard.json")
OUT = Path("app/logs/google_campaign_live_result.json")

data = json.loads(IN.read_text(encoding="utf-8"))
guard = json.loads(GUARD.read_text(encoding="utf-8"))

results, blocked = [], []

try:
    from google.ads.googleads.client import GoogleAdsClient
except Exception as e:
    OUT.write_text(json.dumps({
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "missing_google_ads_library",
        "error": str(e)
    }, indent=2), encoding="utf-8")
    print(OUT.read_text())
    raise SystemExit(0)

if not guard.get("google_live_api_enabled"):
    blocked.append({"reason": "google_live_api_enabled_false"})
else:
    customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "").replace("-", "")
    if not customer_id:
        blocked.append({"reason": "missing_GOOGLE_ADS_CUSTOMER_ID"})
    else:
        client = GoogleAdsClient.load_from_storage()
        budget_service = client.get_service("CampaignBudgetService")
        campaign_service = client.get_service("CampaignService")

        for p in data.get("payloads", [])[: int(guard.get("max_campaigns_per_run", 2))]:
            budget_amount = float(p.get("daily_budget", 0))
            if budget_amount > float(guard.get("max_daily_budget", 5)):
                blocked.append({**p, "reason": "budget_above_limit"})
                continue

            budget_op = client.get_type("CampaignBudgetOperation")
            budget = budget_op.create
            budget.name = p["campaign_name"] + "_BUDGET"
            budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
            budget.amount_micros = int(budget_amount * 1_000_000)

            budget_response = budget_service.mutate_campaign_budgets(
                customer_id=customer_id,
                operations=[budget_op]
            )
            budget_resource = budget_response.results[0].resource_name

            campaign_op = client.get_type("CampaignOperation")
            campaign = campaign_op.create
            campaign.name = p["campaign_name"]
            campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
            campaign.status = client.enums.CampaignStatusEnum.PAUSED
            campaign.manual_cpc.enhanced_cpc_enabled = False
            campaign.campaign_budget = budget_resource
            campaign.network_settings.target_google_search = True
            campaign.network_settings.target_search_network = True
            campaign.network_settings.target_content_network = False
            campaign.network_settings.target_partner_search_network = False

            campaign_response = campaign_service.mutate_campaigns(
                customer_id=customer_id,
                operations=[campaign_op]
            )

            results.append({
                "sku": p.get("sku"),
                "campaign_name": p["campaign_name"],
                "ok": True,
                "budget_resource": budget_resource,
                "campaign_resource": campaign_response.results[0].resource_name
            })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "google_live_api_create_paused_campaigns",
    "blocked": blocked,
    "results": results,
    "created": len(results),
    "status": "ok" if results else ("blocked" if blocked else "error")
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))

