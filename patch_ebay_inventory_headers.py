from pathlib import Path

p = Path("app/channels/ebay_gateway.py")
s = p.read_text(encoding="utf-8")

old = '''    r = requests.put(
        url,
        headers=h["headers"],
        json=payload,
        timeout=30
    )'''

new = '''    headers = h["headers"]
    headers["Content-Language"] = "en-US"
    headers["X-EBAY-C-MARKETPLACE-ID"] = "EBAY_US"

    r = requests.put(
        url,
        headers=headers,
        json=payload,
        timeout=30
    )'''

s = s.replace(old, new)

p.write_text(s, encoding="utf-8")
print("inventory marketplace headers patched")
