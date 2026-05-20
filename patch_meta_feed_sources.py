from pathlib import Path

p=Path("app/feeds/meta_feed.py")
s=p.read_text(encoding="utf-8")

old='''folders = [
        Path("data/published_products"),
        Path("data/products"),
        Path("data/catalog")
    ]'''

new='''folders = [
        Path("data/published_products"),
        Path("data/products"),
        Path("data/catalog"),
        Path("app/logs")
    ]'''

s=s.replace(old,new)

p.write_text(s,encoding="utf-8")
print("meta feed imports log source added")
