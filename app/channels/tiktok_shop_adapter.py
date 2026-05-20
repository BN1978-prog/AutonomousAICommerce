from app.channels.base import BaseChannelAdapter


class TikTokShopAdapter(BaseChannelAdapter):
    channel_name = "tiktok_shop"

    def capabilities(self) -> dict:
        return {"create_draft": True, "publish": True, "update_price": True, "update_inventory": True, "disable_product": True, "read_orders": True, "read_performance": True}

    def status(self) -> dict:
        return {"enabled": False, "status": "not_configured", "marketplace_type": "social_commerce", "capabilities": self.capabilities()}

    def validate_product(self, product: dict) -> dict: return {"ok": False}
    def create_draft(self, product: dict) -> dict: return {"ok": False}
    def publish(self, product_id: str) -> dict: return {"ok": False}
    def update_price(self, sku: str, price: float) -> dict: return {"ok": False}
    def disable_product(self, product_id: str) -> dict: return {"ok": False}
