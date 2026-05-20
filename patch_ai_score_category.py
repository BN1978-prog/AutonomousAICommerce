from pathlib import Path

p=Path("app/suppliers/ai_product_score.py")
s=p.read_text(encoding="utf-8")

old='''    score = 50'''

new='''    score = 50

    category = (
        product.get("raw",{})
        .get("categoryName","")
        .lower()
    )

    category_bonus = {
        "beauty":15,
        "drinkware":15,
        "pet":15,
        "fitness":10,
        "kitchen":10,
        "home":10,
        "electronics":10
    }

    for k,v in category_bonus.items():
        if k in category:
            score += v
            reasons.append(f"good category: {k}")
'''

s=s.replace(old,new)

p.write_text(s,encoding="utf-8")

print("AI SCORE CATEGORY PATCHED")
