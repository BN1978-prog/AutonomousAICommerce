class BaseChannelAdapter:

    channel_name = "base"

    def token_check(self):
        return {
            "ok": False,
            "channel": self.channel_name,
            "message": "token_check not implemented"
        }

    def publish_product(self, product: dict):
        return {
            "ok": False,
            "channel": self.channel_name,
            "message": "publish_product not implemented"
        }

    def update_price(self, sku: str, price: float):
        return {
            "ok": False,
            "channel": self.channel_name,
            "message": "update_price not implemented"
        }

    def update_inventory(self, sku: str, quantity: int):
        return {
            "ok": False,
            "channel": self.channel_name,
            "message": "update_inventory not implemented"
        }

    def archive_product(self, sku: str):
        return {
            "ok": False,
            "channel": self.channel_name,
            "message": "archive_product not implemented"
        }

    def get_product_details(self, sku: str):
        return {
            "ok": False,
            "channel": self.channel_name,
            "message": "get_product_details not implemented"
        }
