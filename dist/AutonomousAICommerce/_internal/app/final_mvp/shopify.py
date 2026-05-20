import os
import httpx
from typing import Dict, Any

class ShopifyDraftService:
    def __init__(self):
        self.store_url = os.getenv("SHOPIFY_STORE_URL", "").rstrip("/")
        self.token = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
        self.api_version = os.getenv("SHOPIFY_API_VERSION", "2025-01")
        self.dry_run = os.getenv("DRY_RUN", "true").lower() == "true"

    def configured(self) -> bool:
        return bool(self.store_url and self.token)

    async def create_draft_product(self, title: str, description: str, price: float) -> Dict[str, Any]:
        if self.dry_run or not self.configured():
            return {
                "dry_run": True,
                "created": False,
                "message": "Simulated Shopify draft product. Set Shopify keys and DRY_RUN=false for live draft.",
                "product": {"title": title, "description": description, "price": price, "status": "draft"},
            }

        url = f"{self.store_url}/admin/api/{self.api_version}/products.json"
        payload = {
            "product": {
                "title": title,
                "body_html": description,
                "status": "draft",
                "variants": [{"price": str(price)}],
            }
        }
        headers = {"X-Shopify-Access-Token": self.token, "Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return {"dry_run": False, "created": True, "response": response.json()}
