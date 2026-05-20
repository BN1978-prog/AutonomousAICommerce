def apply_pricing_rules(cost_price):
    cost = float(cost_price)

    markup_percent = 35
    min_profit = 5.00

    price_by_markup = cost * (1 + markup_percent / 100)
    price_by_min_profit = cost + min_profit

    final_price = max(price_by_markup, price_by_min_profit)

    return round(final_price, 2)
