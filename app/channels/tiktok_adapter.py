import os
from app.channels.base_adapter import BaseChannelAdapter


class TikTokAdapter(BaseChannelAdapter):
    channel_name = "tiktok"

    def token_check(self):
        required = [
            "TIKTOK_APP_KEY",
            "TIKTOK_APP_SECRET",
            "TIKTOK_ACCESS_TOKEN",
            "TIKTOK_SHOP_ID"
        ]

        missing = [x for x in required if not os.getenv(x)]

        return {
            "ok": len(missing)==0,
            "channel": self.channel_name,
            "configured": len(missing)==0,
            "missing": missing
        }


# совместимость со старым registry
class TikTokShopAdapter(TikTokAdapter):
    pass

