from dotenv import load_dotenv
import os

load_dotenv(override=True)

keys = [
    "EBAY_ACCESS_TOKEN",
    "EBAY_REFRESH_TOKEN",
    "EBAY_CLIENT_ID",
    "EBAY_CLIENT_SECRET",
    "EBAY_MARKETPLACE_ID",
]

print("=== EBAY ENV CHECK ===")
for k in keys:
    v = os.getenv(k)
    print(k, "OK" if v else "MISSING")
