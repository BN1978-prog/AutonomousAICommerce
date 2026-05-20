from pathlib import Path

p = Path("app/suppliers/real_supplier.py")
s = p.read_text(encoding="utf-8")

s = s.replace(
    'products_path = os.getenv("SUPPLIER_PRODUCTS_PATH", "products")',
    'products_path = os.getenv("SUPPLIER_PRODUCTS_PATH", "data.list")\n    products_endpoint = os.getenv("SUPPLIER_PRODUCTS_ENDPOINT", "")'
)

s = s.replace(
    'response = httpx.get(url, headers=headers, timeout=30)',
    'if products_endpoint:\n        url = url.rstrip("/") + "/" + products_endpoint.strip("/")\n    response = httpx.get(url, headers=headers, timeout=30)'
)

p.write_text(s, encoding="utf-8")
print("PATCHED")
