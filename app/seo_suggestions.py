import json
from pathlib import Path

SEO = Path("app/logs/seo_action_report.json")
OUT = Path("app/logs/seo_suggestions.json")

items = json.loads(SEO.read_text(encoding="utf-8")) if SEO.exists() else []

suggestions = []

for item in items:
    sku = item["sku"]

    if sku == "PET-BOWL-001":
        title = "Non-Slip Pet Feeding Bowl for Cats and Dogs"
        description = "Practical non-slip pet feeding bowl designed for everyday use with cats and dogs. Easy to place, simple to clean, and suitable for daily feeding routines."
        tags = ["pet bowl", "dog bowl", "cat bowl", "pet feeding", "ai hunter pick"]
    else:
        title = "High-Scoring Trending Product for Everyday Use"
        description = "Selected by the autonomous product scoring system as a high-potential item. Suitable for testing in marketplace and Shopify promotion campaigns."
        tags = ["trending product", "high score", "promotion candidate", "shopify product"]

    suggestions.append({
        "sku": sku,
        "suggested_title": title,
        "suggested_description": description,
        "suggested_tags": tags,
        "auto_apply": False
    })

OUT.write_text(
    json.dumps(suggestions, indent=2),
    encoding="utf-8"
)

print("SEO SUGGESTIONS:", len(suggestions))
for x in suggestions:
    print(x["sku"], "=>", x["suggested_title"])
