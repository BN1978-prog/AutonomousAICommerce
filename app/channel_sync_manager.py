
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
    for cmd in COMMANDS:
        print("[SYNC]", cmd)
        subprocess.run(cmd, shell=True)
