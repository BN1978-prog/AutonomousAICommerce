import requests
from pathlib import Path

url="https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=1200"

p=Path("app/assets/product_images/dog_socks.jpg")
p.parent.mkdir(parents=True,exist_ok=True)

r=requests.get(url,timeout=30)
r.raise_for_status()

p.write_bytes(r.content)

print("Saved:",p)
