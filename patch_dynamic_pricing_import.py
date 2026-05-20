from pathlib import Path

p = Path("app/import_supplier_products.py")
s = p.read_text(encoding="utf-8")

if "from app.pricing_ai import dynamic_price" not in s:
    s = s.replace(
        "from app.suppliers.ai_product_score import score_product",
        "from app.suppliers.ai_product_score import score_product\nfrom app.pricing_ai import dynamic_price"
    )

old = '''        print("=== AI PRODUCT SCORE ===")
        print(score)

        if not score["approved"]:'''

new = '''        print("=== AI PRODUCT SCORE ===")
        print(score)

        pricing = dynamic_price(normalized.get("cost", 0), score.get("score", 50))
        normalized["price"] = pricing["price"]

        print("=== DYNAMIC PRICE ===")
        print(pricing)

        if not score["approved"]:'''

s = s.replace(old, new)

p.write_text(s, encoding="utf-8")
print("dynamic pricing patched into import")
