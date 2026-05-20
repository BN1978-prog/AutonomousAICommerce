from pathlib import Path
import re

p=Path("app/publish_ebay_from_imports.py")
s=p.read_text(encoding="utf-8")

pattern=r"product\s*=\s*\{.*?'imageUrls':\s*\[.*?\].*?\}"

replacement="""product={
            'title': normalized.get('title') or sku,
            'description': normalized.get('description') or 'CJdropshipping product',
            'quantity': int(normalized.get('inventory',1)),
            'imageUrls': [normalized.get('image')] if normalized.get('image') else [],
            'aspects': {
                'Brand':['Unbranded'],
                'Type':[normalized.get('vendor','General')],
                'Category':[normalized.get('raw',{}).get('categoryName','General')]
            }
        }"""

s2 = re.sub(
    pattern,
    replacement,
    s,
    flags=re.S
)

p.write_text(s2,encoding="utf-8")
print("REAL EBAY PRODUCT PATCH APPLIED")
