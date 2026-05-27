import json
from pathlib import Path

report = {
    "products":[
        {
            "id":17,
            "sku":"CJJJCWMY00923",
            "title":"Eco-Friendly Cat Scratcher Toy",
            "local_image":"app/assets/product_images/CJJJCWMY00923.jpg"
        },
        {
            "id":18,
            "sku":"PET-BOWL-001",
            "title":"Non-slip silicone pet feeding bowl",
            "local_image":"app/assets/product_images/PET-BOWL-001.jpg"
        }
    ],
    "status":"LOCAL_IMAGES_ASSIGNED"
}

Path("app/logs/local_product_images.json").write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print(json.dumps(report,indent=2))
