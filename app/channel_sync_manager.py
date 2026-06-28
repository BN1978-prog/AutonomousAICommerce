
def ensure_env_file():
    import os
    from pathlib import Path

    env_path = Path(".env")
    if env_path.exists():
        return

    keys = [
        "OPENAI_API_KEY",
        "SHOPIFY_STORE_URL",
        "SHOPIFY_SHOP_DOMAIN",
        "SHOPIFY_ACCESS_TOKEN",
        "SHOPIFY_ADMIN_TOKEN",
        "SHOPIFY_API_VERSION",
        "META_ACCESS_TOKEN",
        "META_APP_ID",
        "META_APP_SECRET",
        "META_PAGE_ID",
        "GOOGLE_ADS_REFRESH_TOKEN",
        "GOOGLE_ADS_ACCESS_TOKEN",
        "GOOGLE_ADS_CLIENT_ID",
        "GOOGLE_ADS_CLIENT_SECRET",
        "AMAZON_REFRESH_TOKEN",
        "AMAZON_ACCESS_TOKEN",
        "AMAZON_LWA_CLIENT_ID",
        "AMAZON_LWA_CLIENT_SECRET",
        "AMAZON_SELLER_ID",
        "AMAZON_MARKETPLACE_ID",
        "ETSY_API_KEY",
        "ETSY_CLIENT_ID",
        "ETSY_CLIENT_SECRET",
        "ETSY_REDIRECT_URI",
        "ETSY_ACCESS_TOKEN",
        "ETSY_REFRESH_TOKEN",
        "ETSY_SHOP_ID",
        "EBAY_REFRESH_TOKEN",
        "EBAY_ACCESS_TOKEN",
        "WOOCOMMERCE_URL",
        "WOOCOMMERCE_CONSUMER_KEY",
        "WOOCOMMERCE_CONSUMER_SECRET",
    ]

    lines = []
    for k in keys:
        v = os.getenv(k)
        if v:
            safe = str(v).replace("\n", "").replace("\r", "")
            lines.append(f"{k}={safe}")

    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")



import subprocess

COMMANDS = [
    "python -m app.refresh_shopify_token",
    "python -m app.shopify_token_auto_repair",
    "python -m app.google_ads_token_refresher",
    "python -m app.meta_token_refresh",
    "python -m app.meta_page_token_refresh",
    "python -m app.amazon_token_refresher",
    "python -m app.etsy_connection_status",
    "python -m app.etsy_autopilot",
    "python -m app.channel_self_healer"
]

def sync_all_channels():
    ensure_env_file()
    for cmd in COMMANDS:
        print("[SYNC]", cmd)
        subprocess.run(cmd, shell=True)
