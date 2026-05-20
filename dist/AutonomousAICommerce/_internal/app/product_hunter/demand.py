from __future__ import annotations

import hashlib
from app.product_hunter.schemas import DemandSignal
from app.suppliers.schemas import SupplierProduct


class DemandEstimator:
    """Deterministic demand estimator for MVP.

    Production integrations can replace this with Google Trends, marketplace sold-data,
    social trend APIs and ad-platform conversion data. The deterministic design makes
    the module testable and stable.
    """

    CATEGORY_PRIORS = {
        "home": 0.68,
        "pet": 0.70,
        "pets": 0.70,
        "auto": 0.62,
        "beauty": 0.64,
        "electronics_accessories": 0.58,
        "kitchen": 0.66,
        "other": 0.50,
    }

    def estimate(self, product: SupplierProduct, target_market: str) -> list[DemandSignal]:
        category_key = product.category.lower().strip()
        category_score = self.CATEGORY_PRIORS.get(category_key, self.CATEGORY_PRIORS["other"])

        title_score = self._title_intent_score(product.title)
        market_fit = self._market_fit_score(product.country, target_market, product.estimated_delivery_days)
        stock_signal = min(product.stock_available / 100, 1.0)

        return [
            DemandSignal(source="category_prior", score=round(category_score, 3), confidence=0.70, notes=f"Category baseline for {product.category}"),
            DemandSignal(source="title_intent", score=round(title_score, 3), confidence=0.55, notes="Keyword intent and product specificity"),
            DemandSignal(source="market_fit", score=round(market_fit, 3), confidence=0.65, notes="Delivery and origin fit for target market"),
            DemandSignal(source="stock_depth", score=round(stock_signal, 3), confidence=0.60, notes="Stock depth proxy"),
        ]

    @staticmethod
    def aggregate(signals: list[DemandSignal]) -> float:
        weighted = sum(signal.score * signal.confidence for signal in signals)
        total_weight = sum(signal.confidence for signal in signals) or 1
        return round(max(0.0, min(weighted / total_weight, 1.0)), 3)

    @staticmethod
    def _title_intent_score(title: str) -> float:
        positive_terms = {"kit", "set", "portable", "smart", "organizer", "holder", "charger", "storage", "pet", "car", "kitchen"}
        words = {word.strip(".,-_/()[]").lower() for word in title.split()}
        hits = len(words.intersection(positive_terms))
        length_bonus = 0.08 if 4 <= len(words) <= 12 else 0.0
        hash_noise = int(hashlib.sha256(title.lower().encode()).hexdigest()[:2], 16) / 2550
        return min(0.45 + hits * 0.08 + length_bonus + hash_noise, 0.92)

    @staticmethod
    def _market_fit_score(origin_country: str, target_market: str, delivery_days: int) -> float:
        same_region_bonus = 0.12 if origin_country.lower() in {target_market.lower(), "uk", "united kingdom", "eu", "germany", "france", "spain"} else 0.0
        delivery_penalty = min(max(delivery_days - 7, 0) * 0.015, 0.35)
        return max(0.25, min(0.72 + same_region_bonus - delivery_penalty, 0.95))
