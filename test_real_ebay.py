from dotenv import load_dotenv
load_dotenv(override=True)

from app.channels.ebay_gateway import ebay_create_inventory_item
import json

product = {
    "title":"Premium High-borosilicate Glass Tea Cup Internet-famous Double Layer Design With Real Flowers Inside",
    "description":"Real CJ imported product",
    "quantity":10,
    "imageUrls":["https://cf.cjdropshipping.com/quick/product/f31421ca-bfce-46d4-9fd7-9cbcba9f28e6.jpg"],
    "aspects":{
        "Brand":["Unbranded"],
        "Type":["CJdropshipping"],
        "Category":["Drinkware"]
    }
}

print(json.dumps(
    ebay_create_inventory_item(
        "TEST-REAL-DATA-001",
        product
    ),
    indent=2
))
