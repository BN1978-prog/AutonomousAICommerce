import os
from app.channels.base_adapter import BaseChannelAdapter


class EbayAdapter(BaseChannelAdapter):
    channel_name = "ebay"

    def token_check(self):
        required = [
            "EBAY_CLIENT_ID",
            "EBAY_CLIENT_SECRET",
            "EBAY_REFRESH_TOKEN"
        ]

        missing = [x for x in required if not os.getenv(x)]

        return {
            "ok": len(missing) == 0,
            "channel": self.channel_name,
            "configured": len(missing) == 0,
            "missing": missing
        }
