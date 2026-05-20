from __future__ import annotations


class CurrencyConverter:
    """Deterministic offline converter for tests and MVP.

    Production version should replace rates with a trusted FX provider and persist
    the rate timestamp used for every decision.
    """

    def __init__(self, rates_to_gbp: dict[str, float] | None = None) -> None:
        self.rates_to_gbp = rates_to_gbp or {
            "GBP": 1.0,
            "USD": 0.80,
            "EUR": 0.86,
            "CNY": 0.11,
            "TRY": 0.025,
            "JPY": 0.0053,
        }

    def convert(self, amount: float, source_currency: str, target_currency: str) -> float:
        source = source_currency.upper()
        target = target_currency.upper()
        if source not in self.rates_to_gbp:
            raise ValueError(f"Unsupported source currency: {source}")
        if target not in self.rates_to_gbp:
            raise ValueError(f"Unsupported target currency: {target}")
        amount_gbp = amount * self.rates_to_gbp[source]
        converted = amount_gbp / self.rates_to_gbp[target]
        return round(converted, 2)
