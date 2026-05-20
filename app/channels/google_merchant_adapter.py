from app.channels.base import BaseChannelAdapter


class GoogleMerchantAdapter(BaseChannelAdapter):
    channel_name = "google_merchant"

    def capabilities(self) -> dict:
        return {"create_draft": False, "publish": True, "update_price": True, "update_inventory": True, "disable_product": True, "read_orders": False, "read_performance": True}

    def status(self) -> dict:
        return {"enabled": False, "status": "not_configured", "marketplace_type": "product_feed", "capabilities": self.capabilities()}

    def validate_product(self, product: dict) -> dict: return {"ok": False}
    def create_draft(self, product: dict) -> dict: return {"ok": False}
    def publish(self, product_id: str) -> dict: return {"ok": False}
    def update_price(self, sku: str, price: float) -> dict: return {"ok": False}
    def disable_product(self, product_id: str) -> dict: return {"ok": False}
