from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from app.marketplaces.base import MarketplaceClient
from app.marketplaces.schemas import (
    ListingDraft,
    ListingResult,
    ListingStatus,
    MarketplaceFees,
    MarketplaceName,
    MarketplaceOrder,
    PriceUpdateRequest,
)


@dataclass
class MockMarketplaceClient(MarketplaceClient):
    marketplace_name: MarketplaceName = MarketplaceName.MOCK
    _listings: dict[str, ListingResult] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.marketplace_name.value

    async def get_fees(self, category: str, market: str) -> MarketplaceFees:
        if category == "electronics_accessories":
            return MarketplaceFees(platform_fee_percent=13.5, payment_fee_percent=2.9, fixed_fee=0.30)
        return MarketplaceFees(platform_fee_percent=12.0, payment_fee_percent=2.9, fixed_fee=0.30)

    async def publish_listing(self, draft: ListingDraft) -> ListingResult:
        warnings: list[str] = []
        if draft.quantity == 0:
            warnings.append("Listing created as paused because quantity is zero.")
            status = ListingStatus.PAUSED
        else:
            status = ListingStatus.ACTIVE

        digest = hashlib.sha256(f"{self.name}:{draft.sku}:{draft.title}".encode()).hexdigest()[:12]
        result = ListingResult(
            marketplace=self.marketplace_name,
            listing_id=f"{self.name}_{digest}",
            status=status,
            public_url=f"https://example.test/{self.name}/listing/{digest}",
            sku=draft.sku,
            price=round(draft.price, 2),
            currency=draft.currency,
            warnings=warnings,
        )
        self._listings[result.listing_id] = result
        return result

    async def update_price(self, request: PriceUpdateRequest) -> ListingResult:
        existing = self._listings.get(request.listing_id)
        if existing is None:
            raise KeyError(f"Listing not found: {request.listing_id}")
        updated = existing.model_copy(update={"price": round(request.new_price, 2), "currency": request.currency})
        self._listings[request.listing_id] = updated
        return updated

    async def pause_listing(self, listing_id: str, reason: str) -> ListingResult:
        existing = self._listings.get(listing_id)
        if existing is None:
            raise KeyError(f"Listing not found: {listing_id}")
        updated = existing.model_copy(update={"status": ListingStatus.PAUSED, "warnings": existing.warnings + [reason]})
        self._listings[listing_id] = updated
        return updated

    async def fetch_open_orders(self) -> list[MarketplaceOrder]:
        active = [item for item in self._listings.values() if item.status == ListingStatus.ACTIVE]
        if not active:
            return []
        first = active[0]
        return [
            MarketplaceOrder(
                marketplace=self.marketplace_name,
                order_id=f"order_{first.listing_id}",
                listing_id=first.listing_id,
                sku=first.sku,
                quantity=1,
                sale_price=first.price,
                currency=first.currency,
                buyer_country="UK",
                shipping_address_hash=hashlib.sha256(first.listing_id.encode()).hexdigest()[:16],
            )
        ]
