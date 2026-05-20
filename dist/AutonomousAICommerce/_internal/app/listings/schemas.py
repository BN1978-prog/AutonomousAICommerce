from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class ListingTone(str, Enum):
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    PREMIUM = "premium"

class MarketplaceFormat(str, Enum):
    SHOPIFY = "mock_shopify"
    EBAY = "mock_ebay"
    GENERIC = "generic"

class ListingGenerationRequest(BaseModel):
    product_title: str = Field(min_length=3, max_length=180)
    category: str = Field(min_length=2, max_length=80)
    key_features: List[str] = Field(default_factory=list, max_length=12)
    supplier_description: Optional[str] = Field(default=None, max_length=2000)
    target_market: str = Field(default="UK", min_length=2, max_length=80)
    marketplace: MarketplaceFormat = MarketplaceFormat.GENERIC
    tone: ListingTone = ListingTone.PROFESSIONAL
    brand: Optional[str] = Field(default=None, max_length=80)
    max_title_length: int = Field(default=80, ge=40, le=140)

class ListingQualityCheck(BaseModel):
    passed: bool
    warnings: List[str] = Field(default_factory=list)
    blocked_terms_found: List[str] = Field(default_factory=list)
    title_length: int
    description_length: int

class GeneratedListing(BaseModel):
    title: str
    description: str
    bullet_points: List[str]
    seo_keywords: List[str]
    tags: List[str]
    marketplace: MarketplaceFormat
    quality: ListingQualityCheck
