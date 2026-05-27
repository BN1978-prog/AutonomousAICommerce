import os
from dotenv import load_dotenv

load_dotenv()

print("SHOPIFY_STORE_URL =", os.getenv("SHOPIFY_STORE_URL"))
print("SHOPIFY_SHOP_DOMAIN =", os.getenv("SHOPIFY_SHOP_DOMAIN"))
print("SHOPIFY_SHOP =", os.getenv("SHOPIFY_SHOP"))

token = os.getenv("SHOPIFY_ACCESS_TOKEN") or os.getenv("SHOPIFY_ADMIN_TOKEN")
print("TOKEN START =", token[:10] if token else None)
print("TOKEN LEN =", len(token) if token else 0)
