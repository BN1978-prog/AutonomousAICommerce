from pathlib import Path

p=Path("app/update_shopify_existing.py")
s=p.read_text(encoding="utf-8")

s=s.replace(
'''token = (
    os.getenv("SHOPIFY_ADMIN_TOKEN")
    or os.getenv("SHOPIFY_ACCESS_TOKEN")
)''',
'''token = (os.getenv("SHOPIFY_ACCESS_TOKEN","") or "").strip()'''
)

p.write_text(s,encoding="utf-8")
print("SHOPIFY TOKEN FIXED")
