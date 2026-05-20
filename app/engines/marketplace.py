def build_marketplace_intelligence(channels: dict) -> dict:
    rules = {
        "shopify": {
            "title_limit": 255,
            "requires_category": False,
            "requires_brand": False,
            "strict_compliance": False,
            "best_for": ["general_store", "pet_products", "testing"]
        },
        "ebay": {
            "title_limit": 80,
            "requires_category": True,
            "requires_brand": False,
            "strict_compliance": True,
            "best_for": ["pet_socks", "pet_harness", "accessories"]
        },
        "amazon": {
            "title_limit": 200,
            "requires_category": True,
            "requires_brand": True,
            "strict_compliance": True,
            "best_for": ["validated_products", "high_inventory", "stable_supply"]
        },
        "woocommerce": {
            "title_limit": 255,
            "requires_category": False,
            "requires_brand": False,
            "strict_compliance": False,
            "best_for": ["owned_store", "seo", "content_control"]
        },
        "etsy": {
            "title_limit": 140,
            "requires_category": True,
            "requires_brand": False,
            "strict_compliance": True,
            "best_for": ["niche", "handmade_style", "custom_pet_products"]
        },
        "walmart": {
            "title_limit": 200,
            "requires_category": True,
            "requires_brand": True,
            "strict_compliance": True,
            "best_for": ["retail_ready", "stable_supply", "high_inventory"]
        },
        "tiktok_shop": {
            "title_limit": 120,
            "requires_category": True,
            "requires_brand": False,
            "strict_compliance": True,
            "best_for": ["viral_products", "pet_socks", "pet_grooming"]
        },
        "meta_shop": {
            "title_limit": 150,
            "requires_category": True,
            "requires_brand": False,
            "strict_compliance": True,
            "best_for": ["social_commerce", "visual_products"]
        },
        "google_merchant": {
            "title_limit": 150,
            "requires_category": True,
            "requires_brand": True,
            "strict_compliance": True,
            "best_for": ["product_feed", "shopping_ads", "seo"]
        }
    }

    marketplace_status = {}

    if isinstance(channels, list):
        channels = {f"channel_{i}": c for i, c in enumerate(channels)}
    for name, channel in channels.items():
        marketplace_status[name] = {
            "enabled": channel.get("enabled"),
            "status": channel.get("status"),
            "marketplace_type": channel.get("marketplace_type"),
            "rules": rules.get(name, {})
        }

    return {
        "ok": True,
        "marketplaces": marketplace_status,
        "message": "Marketplace rules layer ready. API integrations can be added later."
    }

