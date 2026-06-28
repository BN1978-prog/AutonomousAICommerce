from pathlib import Path
import json
import os
from datetime import datetime, timezone

OUT = Path("app/logs/channel_health.json")

def _status(name, connected=False, state="not_configured", reason=""):
    return {
        "channel": name,
        "connected": bool(connected),
        "state": state,
        "reason": reason
    }

def build_channel_health(catalog=None):
    catalog = catalog or {}
    channels = []

    # Shopify
    if catalog.get("ok"):
        channels.append(_status("shopify", True, "connected", "catalog API OK"))
    elif catalog:
        channels.append(_status("shopify", False, "auth_failed", str(catalog.get("errors") or catalog.get("error") or "Shopify check failed")))
    elif os.getenv("SHOPIFY_ACCESS_TOKEN"):
        channels.append(_status("shopify", False, "unknown", "token exists but catalog was not checked"))
    else:
        channels.append(_status("shopify", False, "missing_token", "SHOPIFY_ACCESS_TOKEN missing"))

    # OpenAI
    channels.append(
        _status("openai", bool(os.getenv("OPENAI_API_KEY")),
                "connected" if os.getenv("OPENAI_API_KEY") else "missing_token",
                "OPENAI_API_KEY present" if os.getenv("OPENAI_API_KEY") else "OPENAI_API_KEY missing")
    )

    # Etsy
    if os.getenv("ETSY_ACCESS_TOKEN") and os.getenv("ETSY_SHOP_ID"):
        channels.append(_status("etsy", True, "connected", "access token and shop id present"))
    elif os.getenv("ETSY_CLIENT_ID") or os.getenv("ETSY_API_KEY"):
        channels.append(_status("etsy", False, "pending_oauth_or_approval", "Etsy app exists but OAuth/shop id not completed"))
    else:
        channels.append(_status("etsy", False, "not_configured", "Etsy credentials missing"))

    # Amazon
    if os.getenv("AMAZON_ACCESS_TOKEN") or os.getenv("AMAZON_REFRESH_TOKEN"):
        channels.append(_status("amazon", True, "configured", "Amazon token present"))
    else:
        channels.append(_status("amazon", False, "not_configured", "Amazon token missing"))

    # Meta
    channels.append(
        _status("meta", bool(os.getenv("META_ACCESS_TOKEN")),
                "configured" if os.getenv("META_ACCESS_TOKEN") else "not_configured",
                "META_ACCESS_TOKEN present" if os.getenv("META_ACCESS_TOKEN") else "META_ACCESS_TOKEN missing")
    )

    # Google Ads
    google_ok = bool(os.getenv("GOOGLE_ADS_REFRESH_TOKEN") or os.getenv("GOOGLE_ADS_ACCESS_TOKEN"))
    channels.append(
        _status("google_ads", google_ok,
                "configured" if google_ok else "not_configured",
                "Google Ads token present" if google_ok else "Google Ads token missing")
    )

    # eBay
    ebay_ok = bool(os.getenv("EBAY_REFRESH_TOKEN") or os.getenv("EBAY_ACCESS_TOKEN"))
    channels.append(
        _status("ebay", ebay_ok,
                "configured" if ebay_ok else "not_configured",
                "eBay token present" if ebay_ok else "eBay token missing")
    )

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "connected_channels": sum(1 for c in channels if c["connected"]),
        "channels": channels
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
