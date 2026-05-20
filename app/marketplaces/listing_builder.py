from __future__ import annotations

import re
from app.schemas.product import ProductCandidate
from app.marketplaces.schemas import ListingDraft


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug[:48] or "product"


class MarketplaceListingBuilder:
    def build_from_candidate(self, product: ProductCandidate, quantity: int = 10) -> ListingDraft:
        best_offer = min(product.offers, key=lambda offer: offer.unit_cost + offer.shipping_cost)
        description = (
            f"{product.title}\n\n"
            f"Ships from supplier country: {best_offer.country}. "
            f"Estimated delivery: {best_offer.estimated_delivery_days} days.\n"
            "Quality and availability are monitored automatically before order fulfillment."
        )
        return ListingDraft(
            sku=f"AI-{_slug(product.title)}",
            title=product.title,
            description=description,
            price=round(product.expected_sale_price, 2),
            currency=product.currency,
            quantity=min(quantity, best_offer.stock_available),
            category=product.category.value,
            tags=[product.category.value, product.target_market.lower(), "ai-selected"],
            supplier_product_id=best_offer.supplier_id,
        )
