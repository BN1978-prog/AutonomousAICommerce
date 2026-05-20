from app.listings.generator import AutoListingGenerator
from app.listings.schemas import ListingGenerationRequest, MarketplaceFormat


def test_listing_generator_creates_marketplace_safe_listing():
    request = ListingGenerationRequest(
        product_title="Portable Mini Desk Vacuum Cleaner",
        category="Home Office Accessories",
        key_features=["USB rechargeable", "compact design", "suitable for crumbs and dust"],
        target_market="UK",
        marketplace=MarketplaceFormat.EBAY,
        brand="CleanMate",
    )
    listing = AutoListingGenerator().generate(request)
    assert len(listing.title) <= 80
    assert "Portable" in listing.title
    assert len(listing.bullet_points) == 3
    assert listing.quality.passed is True
    assert "portable" in listing.seo_keywords


def test_listing_generator_blocks_dangerous_terms():
    request = ListingGenerationRequest(
        product_title="Replica Tactical Weapon",
        category="Collectibles",
        key_features=["counterfeit display item"],
        marketplace=MarketplaceFormat.GENERIC,
    )
    listing = AutoListingGenerator().generate(request)
    assert listing.quality.passed is False
    assert "counterfeit" in listing.quality.blocked_terms_found
    assert "weapon" in listing.quality.blocked_terms_found


def test_listing_generator_strips_html_and_has_defaults():
    request = ListingGenerationRequest(
        product_title="<b>Travel Cable Organizer</b>",
        category="Travel Accessories",
        marketplace=MarketplaceFormat.SHOPIFY,
    )
    listing = AutoListingGenerator().generate(request)
    assert "<b>" not in listing.title
    assert len(listing.bullet_points) >= 3
    assert listing.quality.description_length > 120
