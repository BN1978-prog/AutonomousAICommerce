import os
import httpx
from typing import Dict, Any

class ShopifyDraftService:
    def __init__(self):
        self.store_url = os.getenv("SHOPIFY_STORE_URL", "").rstrip("/")

        if self.store_url and not self.store_url.startswith(("http://", "https://")):
            self.store_url = "https://" + self.store_url

        self.token = (
            os.getenv("SHOPIFY_ADMIN_TOKEN")
            or os.getenv("SHOPIFY_ACCESS_TOKEN", "")
        )

        self.api_version = os.getenv("SHOPIFY_API_VERSION", "2025-01")
        self.dry_run = os.getenv("DRY_RUN", "true").lower() == "true"

    def configured(self) -> bool:
        return bool(self.store_url and self.token)

    def headers(self):
        return {
            "X-Shopify-Access-Token": self.token,
            "Content-Type": "application/json",
        }

    async def create_draft_from_payload(self, product_payload: Dict[str, Any]) -> Dict[str, Any]:
        product = product_payload.get("product", product_payload)
        product.setdefault("status", "draft")

        if self.dry_run or not self.configured():
            return {
                "dry_run": True,
                "created": False,
                "message": "Simulated Shopify draft product.",
                "product": product
            }

        url = f"{self.store_url}/admin/api/{self.api_version}/products.json"

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                url,
                json={"product": product},
                headers=self.headers()
            )

            response.raise_for_status()

            return {
                "dry_run": False,
                "created": True,
                "response": response.json()
            }
