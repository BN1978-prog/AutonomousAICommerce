import requests
from pathlib import Path

IMAGES = {
    "CJJJCWMY00923.jpg":
    "https://images.unsplash.com/photo-1545249390-6bdfa286032f?w=1200",

    "PET-BOWL-001.jpg":
    "https://images.unsplash.com/photo-1583512603806-077998240c7a?w=1200"
}

out = Path("app/assets/product_images")
out.mkdir(parents=True, exist_ok=True)

for filename, url in IMAGES.items():
    try:
        print(f"Downloading {filename}")

        r = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent":"Mozilla/5.0"
            }
        )

        r.raise_for_status()

        file = out / filename
        file.write_bytes(r.content)

        print(f"Saved: {file}")

    except Exception as e:
        print(f"FAILED {filename}: {e}")

print("Done")
