from pathlib import Path

p=Path("app/feeds/meta_feed.py")
s=p.read_text(encoding="utf-8")

old='''                data = json.loads(file.read_text(encoding="utf-8"))
                products.append(data)'''

new='''                data = json.loads(file.read_text(encoding="utf-8"))

                if isinstance(data, list):
                    products.extend([x for x in data if isinstance(x, dict)])

                elif isinstance(data, dict):
                    # imported_skus.json style: {"SKU": {"product_id": ...}}
                    if all(isinstance(v, dict) for v in data.values()):
                        for sku, meta in data.items():
                            item = dict(meta)
                            item.setdefault("sku", sku)
                            products.append(item)
                    else:
                        products.append(data)'''

s=s.replace(old,new)

p.write_text(s,encoding="utf-8")
print("meta feed JSON loader fixed")
