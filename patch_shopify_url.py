from pathlib import Path

p=Path("app/update_shopify_existing.py")
s=p.read_text(encoding="utf-8")

old=''').rstrip("/")'''

new=''')
if not shop_url.startswith(("http://","https://")):
    shop_url="https://" + shop_url

shop_url=shop_url.rstrip("/")'''

s=s.replace(old,new)

p.write_text(s,encoding="utf-8")

print("SHOPIFY URL FIXED")
