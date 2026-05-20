import os
from app.channels.base_adapter import BaseChannelAdapter


class WooCommerceAdapter(BaseChannelAdapter):
    channel_name = "woocommerce"

    def token_check(self):
        required = [
            "WOOCOMMERCE_STORE_URL",
            "WOOCOMMERCE_CONSUMER_KEY",
            "WOOCOMMERCE_CONSUMER_SECRET"
        ]

        missing = [x for x in required if not os.getenv(x)]

        return {
            "ok": len(missing) == 0,
            "channel": self.channel_name,
            "configured": len(missing) == 0,
            "missing": missing
        }
