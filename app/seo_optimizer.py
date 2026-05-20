import re

STOP_WORDS = [
    "internet-famous",
    "hot sale",
    "dropshipping",
    "new",
    "amazon",
    "premium"
]

def clean_title(title: str) -> str:
    t = title or ""

    for w in STOP_WORDS:
        t = re.sub(w, "", t, flags=re.I)

    t = re.sub(r"\s+", " ", t).strip()

    return t


def ebay_title(title: str) -> str:
    t = clean_title(title)
    return t[:80]


def shopify_title(title: str) -> str:
    t = clean_title(title)
    return t[:70]


def bullet_points(product: dict):

    category = (
        product.get("raw", {})
        .get("categoryName", "General")
    )

    return [
        f"High quality {category.lower()} product",
        "Lightweight and durable",
        "Suitable for daily use",
        "Modern design",
        "Fast delivery"
    ]


def seo_tags(product: dict):

    tags = [
        product.get("vendor",""),
        "ai-selected",
        "trending",
        "bestseller"
    ]

    category = (
        product.get("raw", {})
        .get("categoryName")
    )

    if category:
        tags.append(category)

    return ",".join(
        sorted(
            set(
                [x for x in tags if x]
            )
        )
    )


if __name__=="__main__":

    test={
        "title":"Premium High-borosilicate Glass Tea Cup Internet-famous Double Layer Design With Real Flowers Inside",
        "vendor":"CJdropshipping",
        "raw":{"categoryName":"Drinkware"}
    }

    print("EBAY:")
    print(ebay_title(test["title"]))

    print()

    print("SHOPIFY:")
    print(shopify_title(test["title"]))

    print()

    print("BULLETS:")
    print(bullet_points(test))

    print()

    print("TAGS:")
    print(seo_tags(test))
