import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.marketplaces.listing_builder import MarketplaceListingBuilder
from app.marketplaces.mock_marketplace import MockMarketplaceClient
from app.marketplaces.schemas import ListingDraft, ListingStatus, MarketplaceName, PriceUpdateRequest
from app.schemas.product import ProductCandidate, SupplierOffer


@pytest.mark.asyncio
async def test_mock_marketplace_publish_update_and_order_flow():
    client = MockMarketplaceClient(MarketplaceName.SHOPIFY)
    draft = ListingDraft(
        sku="AI-test-product",
        title="Test Product",
        description="A reliable test product for marketplace publishing.",
        price=29.99,
        quantity=5,
        category="home",
    )

    listing = await client.publish_listing(draft)
    assert listing.status == ListingStatus.ACTIVE
    assert listing.listing_id.startswith("shopify_")

    updated = await client.update_price(PriceUpdateRequest(listing_id=listing.listing_id, new_price=31.49))
    assert updated.price == 31.49

    orders = await client.fetch_open_orders()
    assert len(orders) == 1
    assert orders[0].listing_id == listing.listing_id


@pytest.mark.asyncio
async def test_zero_quantity_listing_is_paused():
    client = MockMarketplaceClient(MarketplaceName.EBAY)
    draft = ListingDraft(
        sku="AI-zero-stock",
        title="Zero Stock Product",
        description="A product draft with no inventory available.",
        price=19.99,
        quantity=0,
    )
    listing = await client.publish_listing(draft)
    assert listing.status == ListingStatus.PAUSED
    assert listing.warnings


def test_listing_builder_uses_best_supplier_offer():
    product = ProductCandidate(
        title="Portable Pet Grooming Brush",
        category="pets",
        target_market="UK",
        expected_sale_price=24.99,
        demand_score=0.8,
        competition_score=0.4,
        offers=[
            SupplierOffer(supplier_id="expensive", supplier_name="A", country="DE", unit_cost=10, shipping_cost=4, estimated_delivery_days=5, stock_available=20, supplier_risk_score=0.1),
            SupplierOffer(supplier_id="cheap", supplier_name="B", country="CN", unit_cost=6, shipping_cost=2, estimated_delivery_days=9, stock_available=3, supplier_risk_score=0.2),
        ],
    )
    draft = MarketplaceListingBuilder().build_from_candidate(product, quantity=10)
    assert draft.supplier_product_id == "cheap"
    assert draft.quantity == 3
    assert draft.sku.startswith("AI-portable-pet")


def test_marketplace_api_publish_and_orders():
    api = TestClient(app)
    response = api.post("/marketplaces/shopify/listings", json={
        "sku": "AI-api-product",
        "title": "API Product",
        "description": "A complete product description for API listing tests.",
        "price": 42.5,
        "currency": "gbp",
        "quantity": 2,
        "category": "home",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["marketplace"] == "shopify"
    assert data["currency"] == "GBP"

    orders = api.get("/marketplaces/shopify/orders")
    assert orders.status_code == 200
    assert orders.json()[0]["listing_id"] == data["listing_id"]
