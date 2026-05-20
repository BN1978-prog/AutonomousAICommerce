from __future__ import annotations

from abc import ABC, abstractmethod
from app.marketplaces.schemas import ListingDraft, ListingResult, MarketplaceFees, MarketplaceOrder, PriceUpdateRequest


class MarketplaceClient(ABC):
    """Common contract for all marketplace adapters.

    Real adapters should use official APIs where available. Browser automation should only be
    used for internal/admin workflows that do not violate platform terms.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_fees(self, category: str, market: str) -> MarketplaceFees:
        raise NotImplementedError

    @abstractmethod
    async def publish_listing(self, draft: ListingDraft) -> ListingResult:
        raise NotImplementedError

    @abstractmethod
    async def update_price(self, request: PriceUpdateRequest) -> ListingResult:
        raise NotImplementedError

    @abstractmethod
    async def pause_listing(self, listing_id: str, reason: str) -> ListingResult:
        raise NotImplementedError

    @abstractmethod
    async def fetch_open_orders(self) -> list[MarketplaceOrder]:
        raise NotImplementedError
