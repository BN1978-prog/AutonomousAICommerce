from __future__ import annotations

from pydantic import BaseModel, Field

from app.marketplaces.schemas import ListingResult
from app.suppliers.schemas import SupplierProduct
from app.schemas.decision import AdvancedCommerceDecision
from app.listings.schemas import GeneratedListing


class SemiAutoRunRequest(BaseModel):
    keywords: str = Field(min_length=2, max_length=160)
    target_market: str = Field(default="UK", min_length=2, max_length=64)
    marketplace: str = Field(default="shopify", pattern="^(shopify|mock|ebay)$")
    max_products: int = Field(default=3, ge=1, le=10)
    current_daily_spend: float = Field(default=0.0, ge=0.0)
    publish_drafts: bool = Field(default=True, description="Creates marketplace draft listings when controls allow it.")


class SemiAutoProductResult(BaseModel):
    supplier_product: SupplierProduct
    decision: AdvancedCommerceDecision
    generated_listing: GeneratedListing | None = None
    listing_result: ListingResult | None = None
    action: str
    warnings: list[str] = Field(default_factory=list)


class SemiAutoRunResult(BaseModel):
    mode: str
    dry_run: bool
    autonomy_enabled: bool
    results: list[SemiAutoProductResult]
    summary: dict[str, int | float | str]
