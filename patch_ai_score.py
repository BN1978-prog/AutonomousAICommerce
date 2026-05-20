from pathlib import Path
import re

files = list(Path("app").rglob("*.py"))

for p in files:
    s = p.read_text(encoding="utf-8", errors="ignore")

    if "good keyword: premium" in s:

        s = s.replace(
            'reasons.append("good keyword: premium")',
            '''reasons.append("good keyword: premium")

    categories = [
        "Drinkware",
        "Pet",
        "Beauty",
        "Home",
        "Kitchen",
        "Fitness",
        "Electronics"
    ]

    title_lower = title.lower()

    for c in categories:
        if c.lower() in title_lower:
            score += 10
            reasons.append(f"good category: {c}")
'''
        )

        p.write_text(s, encoding="utf-8")
        print("patched:", p)

print("AI scoring upgraded")
