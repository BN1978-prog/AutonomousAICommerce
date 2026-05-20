from app.models import ProductCandidate

class PricingAgent:
    def recommend_price(self, product: ProductCandidate, target_margin_percent: float = 35) -> float:
        base_cost = product.supplier_price + product.shipping_cost
        platform_multiplier = 1 + (product.platform_fee_percent + product.payment_fee_percent) / 100
        refund_multiplier = 1 + product.estimated_refund_rate_percent / 100
        required_price = base_cost * platform_multiplier * refund_multiplier / (1 - target_margin_percent / 100)
        return round(max(required_price, product.estimated_sale_price), 2)
