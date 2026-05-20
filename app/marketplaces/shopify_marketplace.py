from __future__ import annotations

import hashlib
import httpx

from app.core.config import get_settings
from app.marketplaces.base import MarketplaceClient
from app.marketplaces.schemas import ListingDraft, ListingResult, ListingStatus, MarketplaceFees, MarketplaceName, MarketplaceOrder, PriceUpdateRequest


class ShopifyMarketplaceClient(MarketplaceClient):
    """Shopify Admin connector.

    Safe behavior: when credentials are not configured, it returns deterministic sandbox
    listing results and performs no network request.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self._sandbox_counter = 0
        self._listings: dict[str, ListingResult] = {}

    @property
    def name(self) -> str:
        return MarketplaceName.SHOPIFY.value

    @property
    def configured(self) -> bool:
        return bool(self.settings.shopify_store_domain and self.settings.shopify_admin_access_token)

    async def get_fees(self, category: str, market: str) -> MarketplaceFees:
        return MarketplaceFees(platform_fee_percent=12.0, payment_fee_percent=2.9, fixed_fee=0.30)

    async def publish_listing(self, draft: ListingDraft) -> ListingResult:
        if not self.configured:
            self._sandbox_counter += 1
            result = ListingResult(
                marketplace=MarketplaceName.SHOPIFY,
                listing_id=f"SHOPIFY-SANDBOX-{self._sandbox_counter:06d}",
                status=ListingStatus.ACTIVE if draft.quantity > 0 else ListingStatus.PAUSED,
                public_url=f"https://shopify-sandbox.local/products/{hashlib.sha256(draft.sku.encode()).hexdigest()[:10]}",
                sku=draft.sku,
                price=round(draft.price, 2),
                currency=draft.currency,
                warnings=["Shopify credentials are not configured; created sandbox draft only."],
            )
            self._listings[result.listing_id] = result
            return result

        domain = str(self.settings.shopify_store_domain).replace("https://", "").replace("http://", "").rstrip("/")
        url = f"https://{domain}/admin/api/{self.settings.shopify_api_version}/products.json"
        payload = {
            "product": {
                "title": draft.title,
                "body_html": draft.description,
                "vendor": "Autonomous AI Commerce",
                "product_type": draft.category,
                "status": "draft",
                "tags": ", ".join(draft.tags),
                "variants": [
                    {
                        "sku": draft.sku,
                        "price": f"{draft.price:.2f}",
                        "inventory_quantity": draft.quantity,
                    }
                ],
                "images": [{"src": src} for src in draft.image_urls],
            }
        }
        headers = {"X-Shopify-Access-Token": str(self.settings.shopify_admin_access_token)}
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            product = response.json()["product"]
        result = ListingResult(
            marketplace=MarketplaceName.SHOPIFY,
            listing_id=str(product["id"]),
            status=ListingStatus.DRAFT,
            public_url=None,
            sku=draft.sku,
            price=round(draft.price, 2),
            currency=draft.currency,
            warnings=["Created Shopify draft product. Review and publish in Shopify admin before live sales."],
        )
        self._listings[result.listing_id] = result
        return result

    async def update_price(self, request: PriceUpdateRequest) -> ListingResult:
        existing = self._listings.get(request.listing_id)
        if existing is None:
            result = ListingResult(
                marketplace=MarketplaceName.SHOPIFY,
                listing_id=request.listing_id,
                status=ListingStatus.DRAFT,
                sku="unknown",
                price=round(request.new_price, 2),
                currency=request.currency,
                warnings=["Price update endpoint is sandboxed in this build."],
            )
        else:
            result = existing.model_copy(update={"price": round(request.new_price, 2), "currency": request.currency})
        self._listings[request.listing_id] = result
        return result

    async def pause_listing(self, listing_id: str, reason: str) -> ListingResult:
        existing = self._listings.get(listing_id)
        if existing is None:
            result = ListingResult(
                marketplace=MarketplaceName.SHOPIFY,
                listing_id=listing_id,
                status=ListingStatus.PAUSED,
                sku="unknown",
                price=0.01,
                currency="GBP",
                warnings=[f"Paused in sandbox connector: {reason}"],
            )
        else:
            result = existing.model_copy(update={"status": ListingStatus.PAUSED, "warnings": existing.warnings + [reason]})
        self._listings[listing_id] = result
        return result

    async def fetch_open_orders(self) -> list[MarketplaceOrder]:
        active = [item for item in self._listings.values() if item.status == ListingStatus.ACTIVE]
        if not active:
            return []
        first = active[0]
        return [
            MarketplaceOrder(
                marketplace=MarketplaceName.SHOPIFY,
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
