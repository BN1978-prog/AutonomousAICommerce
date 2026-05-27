import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/social_post_plan.json")

posts = [
    {
        "sku": "PET-BOWL-001",
        "platforms": ["TikTok", "Instagram Reels", "Pinterest"],
        "title": "Non-slip silicone pet feeding bowl",
        "post": "Tired of your pet pushing the bowl around the floor? This non-slip silicone feeding bowl keeps mealtime cleaner and easier. Perfect for cats and dogs.",
        "hashtags": ["#petbowl", "#dogbowl", "#catbowl", "#petcare", "#petproducts"],
        "cta": "Shop now"
    },
    {
        "sku": "CJMY2126410",
        "platforms": ["TikTok", "Instagram Reels", "Pinterest"],
        "title": "Foldable Cat Tunnel Toy",
        "post": "A simple way to keep indoor cats active and entertained. This foldable cat tunnel gives them a place to run, hide and play.",
        "hashtags": ["#cattoy", "#catlover", "#indoorcat", "#pettoys", "#catlife"],
        "cta": "See it in store"
    },
    {
        "sku": "CJGD1113594",
        "platforms": ["TikTok", "Instagram Reels", "Pinterest"],
        "title": "British Style Dog Raincoat",
        "post": "Rainy walks do not have to be messy. Keep your dog dry and comfortable with this lightweight dog raincoat.",
        "hashtags": ["#dograincoat", "#dogwalk", "#dogfashion", "#petcare", "#doglife"],
        "cta": "Shop the look"
    }
]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "posts_ready": len(posts),
    "items": posts,
    "status": "SOCIAL_POST_PLAN_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
