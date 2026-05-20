from app.schemas.decision import ProfitBreakdown
from app.schemas.product import ProductCandidate, SupplierOffer


class ProfitEngine:
    """Deterministic profit calculator. No AI calls here by design."""

    @staticmethod
    def calculate(product: ProductCandidate, offer: SupplierOffer) -> ProfitBreakdown:
        sale_price = product.expected_sale_price
        platform_fee = sale_price * (product.platform_fee_percent / 100)
        payment_fee = sale_price * (product.payment_fee_percent / 100)
        expected_refund_cost = sale_price * product.estimated_refund_rate
        total_cost = (
            offer.unit_cost
            + offer.shipping_cost
            + platform_fee
            + payment_fee
            + product.estimated_ad_cost
            + expected_refund_cost
        )
        net_profit = sale_price - total_cost
        margin_percent = (net_profit / sale_price) * 100 if sale_price > 0 else 0
        invested = offer.unit_cost + offer.shipping_cost + product.estimated_ad_cost
        roi_percent = (net_profit / invested) * 100 if invested > 0 else 0
        return ProfitBreakdown(
            sale_price=round(sale_price, 2),
            supplier_cost=round(offer.unit_cost, 2),
            supplier_shipping=round(offer.shipping_cost, 2),
            platform_fee=round(platform_fee, 2),
            payment_fee=round(payment_fee, 2),
            ad_cost=round(product.estimated_ad_cost, 2),
            expected_refund_cost=round(expected_refund_cost, 2),
            net_profit=round(net_profit, 2),
            margin_percent=round(margin_percent, 2),
            roi_percent=round(roi_percent, 2),
        )
