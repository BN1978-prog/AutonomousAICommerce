from pathlib import Path

p = Path("app/publish_ebay_from_imports.py")
s = p.read_text(encoding="utf-8")

old = """product={
            'title': sku,
            'description':'AI selected CJdropshipping product.',
            'quantity':10,
            'imageUrls':['https://i.ebayimg.com/images/g/0yAAAOSwD9BlrQqA/s-l1600.jpg'],
            'aspects':{
                'Brand':['Unbranded'],
                'Type':['General']
            }
        }"""

new = """product={
            'title': normalized.get('title') or sku,
            'description': normalized.get('description') or 'CJdropshipping product',
            'quantity': int(normalized.get('inventory',1)),
            'imageUrls':[normalized.get('image')] if normalized.get('image') else [],
            'aspects':{
                'Brand':['Unbranded'],
                'Type':[normalized.get('vendor','General')],
                'Category':[normalized.get('raw',{}).get('categoryName','General')]
            }
        }"""

s=s.replace(old,new)

p.write_text(s,encoding="utf-8")
print("EBAY REAL PRODUCT DATA PATCHED")
