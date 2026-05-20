from __future__ import annotations

from app.schemas.product import ProductCandidate, ProductCategory, SupplierOffer
from app.suppliers.schemas import SupplierProduct


def map_category(category: str) -> ProductCategory:
    normalized = category.lower().strip().replace(" ", "_")
    aliases = {
        "pet": ProductCategory.PETS,
        "pets": ProductCategory.PETS,
        "home": ProductCategory.HOME,
        "kitchen": ProductCategory.HOME,
        "auto": ProductCategory.AUTO,
        "car": ProductCategory.AUTO,
        "beauty": ProductCategory.BEAUTY,
        "electronics": ProductCategory.ELECTRONICS_ACCESSORIES,
        "electronics_accessories": ProductCategory.ELECTRONICS_ACCESSORIES,
    }
    return aliases.get(normalized, ProductCategory.OTHER)


def supplier_product_to_candidate(
    product: SupplierProduct,
    expected_sale_price: float,
    target_market: str,
    currency: str,
    demand_score: float,
    competition_score: float,
    platform_fee_percent: float,
    payment_fee_percent: float,
    estimated_ad_cost: float,
) -> ProductCandidate:
    supplier_risk = max(0.0, min(1.0, 1 - (product.supplier_rating / 5)))
    return_risk = max(0.0, min(1.0, product.return_rate_percent / 100))
    offer = SupplierOffer(
        supplier_id=product.supplier_id,
        supplier_name=product.supplier_id,
        country=product.country,
        product_url=str(product.product_url) if product.product_url else None,
        unit_cost=product.unit_cost.amount,
        shipping_cost=product.shipping_cost.amount,
        estimated_delivery_days=product.estimated_delivery_days,
        stock_available=product.stock_available,
        supplier_risk_score=round(supplier_risk, 3),
    )
    return ProductCandidate(
        title=product.title[:140],
        category=map_category(product.category),
        target_market=target_market,
        currency=currency,
        expected_sale_price=round(expected_sale_price, 2),
        platform_fee_percent=platform_fee_percent,
        payment_fee_percent=payment_fee_percent,
        estimated_ad_cost=estimated_ad_cost,
        estimated_refund_rate=round(max(0.02, return_risk), 3),
        return_risk_score=round(return_risk, 3),
        demand_score=demand_score,
        competition_score=competition_score,
        offers=[offer],
    )
