from pathlib import Path

p=Path("app/woocommerce_validation.py")
text=p.read_text(encoding="utf-8-sig")

text=text.replace(
    'os.getenv("WOOCOMMERCE_STORE_URL")',
    'os.getenv("WOOCOMMERCE_URL") or os.getenv("WOOCOMMERCE_STORE_URL")'
)

p.write_text(text,encoding="utf-8")
print("woocommerce_validation now accepts WOOCOMMERCE_URL")
