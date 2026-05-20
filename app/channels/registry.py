from app.channels.shopify_adapter import ShopifyAdapter
from app.channels.ebay_adapter import EbayAdapter
from app.channels.tiktok_adapter import TikTokShopAdapter
from app.channels.meta_adapter import MetaShopAdapter
from app.channels.woocommerce_adapter import WooCommerceAdapter
from app.channels.amazon_adapter import AmazonAdapter

class ChannelRegistry:
    def __init__(self):
        self._channels = {}

    def register(self, adapter):
        self._channels[adapter.channel_name] = adapter

    def get(self, channel):
        return self._channels.get(channel)

    def keys(self):
        return self._channels.keys()

    def all(self):
        return self._channels

    def list_channels(self):
        result = {}

        for name, adapter in self._channels.items():
            try:
                result[name] = adapter.status()
            except Exception:
                result[name] = {
                    "enabled": False,
                    "status": "error"
                }

        return result


def get_registry():
    registry = ChannelRegistry()

    registry.register(ShopifyAdapter())
    registry.register(EbayAdapter())
    registry.register(TikTokShopAdapter())
    registry.register(MetaShopAdapter())
    registry.register(WooCommerceAdapter())
    registry.register(AmazonAdapter())

    return registry




