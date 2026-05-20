import os
from app.channels.base import BaseChannelAdapter

class MetaShopAdapter(BaseChannelAdapter):
    channel_name = "meta_shop"

    def status(self) -> dict:
        missing = []
        if not os.getenv("META_ACCESS_TOKEN"):
            missing.append("META_ACCESS_TOKEN")
        if not os.getenv("META_CATALOG_ID"):
            missing.append("META_CATALOG_ID")

        return {
            "enabled": False,
            "status": "not_configured" if missing else "configured_preview",
            "marketplace_type": "social_commerce",
            "missing_config": missing,
            "capabilities": {
                "create_draft": True,
                "publish": True,
                "update_price": True,
                "update_inventory": True,
                "disable_product": True,
                "read_orders": False,
                "read_performance": True
            }
        }

    def validate_product(self, product: dict) -> dict:
        return {"ok": True, "warnings": []}

    def create_draft(self, product: dict) -> dict:
        return {"ok": False, "message": "Meta API not connected"}

    def publish(self, product: dict) -> dict:
        return {"ok": False, "message": "Meta API not connected"}

    def update_price(self, sku: str, price: float) -> dict:
        return {"ok": False}

    def update_inventory(self, sku: str, inventory: int) -> dict:
        return {"ok": False}

    def disable_product(self, product_id: str) -> dict:
        return {"ok": False}

    def execute_publish_preview(self, job: dict) -> dict:
        return {
            "ok": False,
            "status": "failed_preview",
            "channel": self.channel_name,
            "message": "Meta Shop adapter not connected yet"
        }
