import json
import webbrowser
from pathlib import Path
from datetime import datetime

store_url = "{TRACKING_URL}"

posts = [
    {
        "platform": "Facebook / Instagram / Pinterest",
        "text": f"""Tired of your pet pushing the bowl around the floor?

This non-slip silicone feeding bowl keeps mealtime cleaner and easier. Perfect for cats and dogs.

Shop now: {store_url}

#petbowl #dogbowl #catbowl #petcare #petproducts"""
    },
    {
        "platform": "Facebook / Instagram / Pinterest",
        "text": f"""A simple way to keep indoor cats active and entertained.

This foldable cat tunnel gives them a place to run, hide and play.

See it in store: {store_url}

#cattoy #catlover #indoorcat #pettoys #catlife"""
    },
    {
        "platform": "Facebook / Instagram / Pinterest",
        "text": f"""Rainy walks do not have to be messy.

Keep your dog dry and comfortable with this lightweight dog raincoat.

Shop the look: {store_url}

#dograincoat #dogwalk #dogfashion #petcare #doglife"""
    }
]

out = Path("app/logs/daily_social_posts_ready.json")
out.write_text(json.dumps({
    "created_at": datetime.now().isoformat(),
    "store_url": store_url,
    "posts": posts
}, indent=2), encoding="utf-8")

Path("app/logs/post_to_copy.txt").write_text(posts[0]["text"], encoding="utf-8")

print("POSTS READY:", len(posts))
print("COPY THIS FILE:")
print("app/logs/post_to_copy.txt")

webbrowser.open("https://business.facebook.com/latest/home")
webbrowser.open("https://www.pinterest.com/pin-builder/")
webbrowser.open("https://www.tiktok.com/upload")
