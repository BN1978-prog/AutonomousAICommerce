def optimize_titles(product: dict, intelligence: dict) -> dict:
    source_title = product.get("title") or ""
    category = product.get("category") or "Pet Supplies"
    brand = product.get("brand") or "Generic"

    optimized = {}

    for marketplace, data in intelligence.get("marketplaces", {}).items():
        rules = data.get("rules", {})
        limit = rules.get("title_limit", 255)

        title = source_title

        if marketplace == "amazon":
            title = f"{brand} {source_title} - {category}"
        elif marketplace == "tiktok_shop":
            title = f"{source_title} | Trending Pet Essential"
        elif marketplace == "google_merchant":
            title = f"{source_title} - {brand} - {category}"
        elif marketplace == "etsy":
            title = f"{source_title} for Pets"
        elif marketplace == "meta_shop":
            title = f"{source_title} | Pet Accessories"

        title = title[:limit]

        optimized[marketplace] = {
            "title": title,
            "title_length": len(title),
            "title_limit": limit,
            "ok": len(title) <= limit
        }

    return {
        "ok": True,
        "source_title": source_title,
        "optimized_titles": optimized
    }


def optimize_seo(product: dict) -> dict:
    title = (product.get("title") or "").lower()
    category = product.get("category") or "Pet Supplies"

    keywords = []

    if "sock" in title:
        keywords += ["dog socks", "pet socks", "non slip dog socks", "paw protection"]

    if "harness" in title:
        keywords += ["pet harness", "dog harness", "cat harness", "no pull harness"]

    if "shampoo" in title:
        keywords += ["pet shampoo", "dog shampoo", "cat shampoo", "pet grooming"]

    if "brush" in title or "grooming" in title:
        keywords += ["pet grooming", "pet brush", "dog grooming", "cat grooming"]

    if not keywords:
        keywords = ["pet supplies", "pet accessories", category.lower()]

    keywords = list(dict.fromkeys(keywords))

    return {
        "ok": True,
        "title": product.get("title"),
        "category": category,
        "seo": {
            "keywords": keywords,
            "tags": keywords[:8],
            "search_terms": ", ".join(keywords),
            "short_description": f"{product.get('title')} for pets. Designed for comfort, daily use, and practical pet care.",
            "marketplace_fields": {
                "shopify_tags": keywords[:8],
                "ebay_keywords": keywords[:5],
                "amazon_search_terms": " ".join(keywords[:5]),
                "google_product_keywords": keywords[:6],
                "tiktok_hashtags": [f"#{k.replace(' ', '')}" for k in keywords[:5]]
            }
        }
    }
