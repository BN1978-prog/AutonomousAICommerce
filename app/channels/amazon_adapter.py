import os
from app.channels.base_adapter import BaseChannelAdapter


class AmazonAdapter(BaseChannelAdapter):
    channel_name = "amazon"

    def token_check(self):
        required = [
            "AMAZON_CLIENT_ID",
            "AMAZON_CLIENT_SECRET",
            "AMAZON_REFRESH_TOKEN",
            "AMAZON_SELLER_ID",
            "AMAZON_MARKETPLACE_ID"
        ]

        missing = [x for x in required if not os.getenv(x)]

        return {
            "ok": len(missing) == 0,
            "channel": self.channel_name,
            "configured": len(missing) == 0,
            "missing": missing
        }
