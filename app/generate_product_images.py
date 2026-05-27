from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

out = Path("app/generated_images")
out.mkdir(parents=True, exist_ok=True)

items = [
    ("eco_cat_toy.png", "Eco Cat Toy"),
    ("pet_bowl.png", "Pet Bowl")
]

for filename, text in items:
    img = Image.new("RGB", (800, 800), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, 760, 760], outline=(80, 80, 80), width=8)
    draw.text((220, 370), text, fill=(20, 20, 20))
    img.save(out / filename)

print("Images created in app/generated_images")
