from __future__ import annotations

from app.marketplaces.base import MarketplaceClient
from app.marketplaces.mock_marketplace import MockMarketplaceClient
from app.marketplaces.shopify_marketplace import ShopifyMarketplaceClient
from app.marketplaces.schemas import MarketplaceName


class MarketplaceRegistry:
    def __init__(self) -> None:
        self._clients: dict[MarketplaceName, MarketplaceClient] = {
            MarketplaceName.MOCK: MockMarketplaceClient(MarketplaceName.MOCK),
            MarketplaceName.SHOPIFY: ShopifyMarketplaceClient(),
            MarketplaceName.EBAY: MockMarketplaceClient(MarketplaceName.EBAY),
        }

    def get(self, name: MarketplaceName) -> MarketplaceClient:
        try:
            return self._clients[name]
        except KeyError as exc:
            raise ValueError(f"Unsupported marketplace: {name}") from exc

    def list_names(self) -> list[str]:
        return [key.value for key in self._clients]
