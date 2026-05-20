from pathlib import Path

p=Path("app/feeds/meta_feed.py")
s=p.read_text(encoding="utf-8")

if 'if __name__ == "__main__":' not in s:
    s += '''

def main():
    out_dir = Path("data/catalog")
    out_dir.mkdir(parents=True, exist_ok=True)

    xml = generate_meta_products_xml()
    out = out_dir / "meta-products.xml"
    out.write_bytes(xml)

    print("META FEED GENERATED:", out)
    print("SIZE:", out.stat().st_size)


if __name__ == "__main__":
    main()
'''

p.write_text(s,encoding="utf-8")
print("meta_feed main added")
