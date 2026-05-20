from pathlib import Path

p=Path("app/update_shopify_existing.py")
s=p.read_text(encoding="utf-8")

# add import
if "from app.channels.shopify_config import ShopifyConfig" not in s:
    s=s.replace(
        "from app.pricing_ai import dynamic_price",
        "from app.pricing_ai import dynamic_price\nfrom app.channels.shopify_config import ShopifyConfig"
    )

# replace shop/token block roughly
start=s.find("shop_url = (")
end=s.find("headers = {", start)

new_block='''shop_url = "https://" + ShopifyConfig.get_store().strip().replace("https://","").replace("http://","").rstrip("/")
token = ShopifyConfig.get_token()

'''

s=s[:start]+new_block+s[end:]

p.write_text(s,encoding="utf-8")
print("update_shopify_existing now uses ShopifyConfig")
