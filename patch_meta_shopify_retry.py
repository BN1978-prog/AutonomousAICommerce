from pathlib import Path

p=Path("app/feeds/meta_shopify_feed.py")
s=p.read_text(encoding="utf-8")

s=s.replace(
'''    r = requests.get(url, headers=headers, timeout=30)

    if r.status_code != 200:
        print("SKIP", sku, r.status_code)
        continue''',
'''    r = None

    for attempt in range(3):
        try:
            r = requests.get(url, headers=headers, timeout=15)
            break
        except requests.exceptions.RequestException as e:
            print("RETRY", sku, attempt + 1, str(e)[:120])

    if r is None:
        print("SKIP", sku, "timeout")
        continue

    if r.status_code != 200:
        print("SKIP", sku, r.status_code)
        continue'''
)

p.write_text(s,encoding="utf-8")
print("META SHOPIFY FEED RETRY PATCHED")
