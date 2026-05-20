from __future__ import annotations

from .schemas import ShippingRate


class ShippingSelector:
    def choose_best(self, rates: list[ShippingRate], min_reliability: float = 0.9) -> ShippingRate:
        if not rates:
            raise ValueError("No shipping rates available")
        acceptable = [r for r in rates if r.reliability_score >= min_reliability]
        pool = acceptable or rates
        return sorted(pool, key=lambda r: (r.price, r.estimated_days, -r.reliability_score))[0]
