from __future__ import annotations

from app.schemas.product import ProductCategory, SupplierOffer
from app.suppliers.currency import CurrencyConverter
from app.suppliers.schemas import SupplierProduct


CATEGORY_MAP = {
    "home": ProductCategory.HOME,
    "pets": ProductCategory.PETS,
    "auto": ProductCategory.AUTO,
    "beauty": ProductCategory.BEAUTY,
    "electronics_accessories": ProductCategory.ELECTRONICS_ACCESSORIES,
}


class SupplierNormalizer:
    def __init__(self, converter: CurrencyConverter | None = None) -> None:
        self.converter = converter or CurrencyConverter()

    def to_offer(self, product: SupplierProduct, target_currency: str = "GBP") -> SupplierOffer:
        unit_cost = self.converter.convert(product.unit_cost.amount, product.unit_cost.currency, target_currency)
        shipping_cost = self.converter.convert(product.shipping_cost.amount, product.shipping_cost.currency, target_currency)
        risk = self._supplier_risk(product)
        return SupplierOffer(
            supplier_id=product.supplier_id,
            supplier_name=product.supplier_id.replace("_", " ").title(),
            country=product.country,
            product_url=str(product.product_url) if product.product_url else None,
            unit_cost=unit_cost,
            shipping_cost=shipping_cost,
            estimated_delivery_days=product.estimated_delivery_days,
            stock_available=product.stock_available,
            supplier_risk_score=risk,
        )

    def category(self, product: SupplierProduct) -> ProductCategory:
        return CATEGORY_MAP.get(product.category.lower(), ProductCategory.OTHER)

    def _supplier_risk(self, product: SupplierProduct) -> float:
        rating_risk = max(0.0, (5.0 - product.supplier_rating) / 5.0)
        delivery_risk = min(product.estimated_delivery_days / 60, 1.0)
        return_risk = min(product.return_rate_percent / 100, 1.0)
        stock_risk = 0.0 if product.stock_available >= 20 else 0.35
        restricted_risk = 1.0 if product.restricted else 0.0
        score = (
            rating_risk * 0.30
            + delivery_risk * 0.25
            + return_risk * 0.15
            + stock_risk * 0.10
            + restricted_risk * 0.20
        )
        return round(max(0.0, min(score, 1.0)), 4)
