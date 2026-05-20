from dotenv import dotenv_values

env = dotenv_values(".env")

keys = [
    "SHOPIFY_STORE_URL",
    "SHOPIFY_CLIENT_ID",
    "SHOPIFY_CLIENT_SECRET",
    "SHOPIFY_ACCESS_TOKEN",
    "SHOPIFY_ADMIN_TOKEN",
    "SHOPIFY_API_VERSION"
]

for k in keys:
    v = env.get(k, "") or ""
    print(k, "=", "SET" if v else "EMPTY", "len", len(v), "prefix", v[:8])
