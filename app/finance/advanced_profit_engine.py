from __future__ import annotations

from app.finance.schemas import AdvancedProfitBreakdown, CostAssumptions, FeeModel, ProfitScenario, ScenarioResult


class AdvancedProfitEngine:
    """Deterministic commercial calculator used before any autonomous action.

    It deliberately avoids LLM calls so results are repeatable and testable.
    """

    def calculate(
        self,
        *,
        sale_price: float,
        supplier_cost: float,
        supplier_shipping: float,
        fee_model: FeeModel,
        cost_assumptions: CostAssumptions,
    ) -> AdvancedProfitBreakdown:
        marketplace_fee = sale_price * fee_model.marketplace_fee_percent / 100 + fee_model.marketplace_fixed_fee
        payment_fee = sale_price * fee_model.payment_fee_percent / 100 + fee_model.payment_fixed_fee
        tax_estimate = sale_price * fee_model.vat_or_sales_tax_percent / 100
        currency_conversion_cost = supplier_cost * fee_model.currency_conversion_percent / 100
        expected_refund_cost = (sale_price * cost_assumptions.estimated_refund_rate) + (
            cost_assumptions.refund_processing_cost * cost_assumptions.estimated_refund_rate
        )
        subtotal_before_buffer = (
            supplier_cost
            + supplier_shipping
            + marketplace_fee
            + payment_fee
            + tax_estimate
            + currency_conversion_cost
            + cost_assumptions.estimated_ad_cost
            + cost_assumptions.packaging_cost
            + expected_refund_cost
        )
        risk_buffer = subtotal_before_buffer * cost_assumptions.buffer_percent / 100
        total_cost = subtotal_before_buffer + risk_buffer
        net_profit = sale_price - total_cost
        invested = supplier_cost + supplier_shipping + cost_assumptions.estimated_ad_cost + cost_assumptions.packaging_cost
        margin_percent = (net_profit / sale_price) * 100 if sale_price > 0 else 0.0
        roi_percent = (net_profit / invested) * 100 if invested > 0 else 0.0
        variable_rate = (
            fee_model.marketplace_fee_percent
            + fee_model.payment_fee_percent
            + fee_model.vat_or_sales_tax_percent
        ) / 100
        fixed_costs = (
            supplier_cost
            + supplier_shipping
            + fee_model.marketplace_fixed_fee
            + fee_model.payment_fixed_fee
            + currency_conversion_cost
            + cost_assumptions.estimated_ad_cost
            + cost_assumptions.packaging_cost
        )
        # Conservative: break-even includes refund and buffer approximately.
        denominator = max(0.01, 1 - variable_rate - cost_assumptions.estimated_refund_rate - (cost_assumptions.buffer_percent / 100))
        break_even_price = fixed_costs / denominator
        return AdvancedProfitBreakdown(
            sale_price=round(sale_price, 2),
            supplier_cost=round(supplier_cost, 2),
            supplier_shipping=round(supplier_shipping, 2),
            marketplace_fee=round(marketplace_fee, 2),
            payment_fee=round(payment_fee, 2),
            tax_estimate=round(tax_estimate, 2),
            currency_conversion_cost=round(currency_conversion_cost, 2),
            ad_cost=round(cost_assumptions.estimated_ad_cost, 2),
            packaging_cost=round(cost_assumptions.packaging_cost, 2),
            expected_refund_cost=round(expected_refund_cost, 2),
            risk_buffer=round(risk_buffer, 2),
            total_cost=round(total_cost, 2),
            net_profit=round(net_profit, 2),
            margin_percent=round(margin_percent, 2),
            roi_percent=round(roi_percent, 2),
            break_even_price=round(break_even_price, 2),
        )

    def scenarios(
        self,
        *,
        sale_price: float,
        supplier_cost: float,
        supplier_shipping: float,
        fee_model: FeeModel,
        cost_assumptions: CostAssumptions,
        scenarios: list[ProfitScenario] | None = None,
    ) -> list[ScenarioResult]:
        scenarios = scenarios or [
            ProfitScenario(name="base"),
            ProfitScenario(name="downside", sale_price_multiplier=0.9, refund_rate_multiplier=1.5, ad_cost_multiplier=1.25),
            ProfitScenario(name="upside", sale_price_multiplier=1.1, refund_rate_multiplier=0.8, ad_cost_multiplier=0.9),
        ]
        results: list[ScenarioResult] = []
        for scenario in scenarios:
            adjusted_assumptions = cost_assumptions.model_copy(
                update={
                    "estimated_refund_rate": min(1.0, cost_assumptions.estimated_refund_rate * scenario.refund_rate_multiplier),
                    "estimated_ad_cost": cost_assumptions.estimated_ad_cost * scenario.ad_cost_multiplier,
                }
            )
            results.append(
                ScenarioResult(
                    scenario=scenario.name,
                    profit=self.calculate(
                        sale_price=sale_price * scenario.sale_price_multiplier,
                        supplier_cost=supplier_cost,
                        supplier_shipping=supplier_shipping,
                        fee_model=fee_model,
                        cost_assumptions=adjusted_assumptions,
                    ),
                )
            )
        return results
