import os
from app.channels.base_adapter import BaseChannelAdapter


class EtsyAdapter(BaseChannelAdapter):
    channel_name = "etsy"

    def token_check(self):
        required = [
            "ETSY_API_KEY",
            "ETSY_ACCESS_TOKEN",
            "ETSY_SHOP_ID"
        ]

        missing = [x for x in required if not os.getenv(x)]

        return {
            "ok": len(missing) == 0,
            "channel": self.channel_name,
            "configured": len(missing) == 0,
            "missing": missing
        }
