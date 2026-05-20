import os
from typing import Dict, Any, Optional
import httpx

class ShopifyClient:
    def __init__(self, store_url: str = "", access_token: str = "", api_version: str = "2025-01"):
        self.store_url = (store_url or "").rstrip("/")
        self.access_token = access_token or ""
        self.api_version = api_version or "2025-01"

    @classmethod
    def from_env(cls):
        return cls(
            store_url=os.getenv("SHOPIFY_STORE_URL", ""),
            access_token=os.getenv("SHOPIFY_ACCESS_TOKEN", ""),
            api_version=os.getenv("SHOPIFY_API_VERSION", "2025-01"),
        )

    def is_configured(self) -> bool:
        return bool(self.store_url and self.access_token)

    def status(self) -> Dict[str, Any]:
        return {
            "configured": self.is_configured(),
            "store_url_set": bool(self.store_url),
            "access_token_set": bool(self.access_token),
            "mode": "live-ready" if self.is_configured() else "sandbox/config-needed",
        }

    async def create_product_draft(self, title: str, description: str, price: float) -> Dict[str, Any]:
        if not self.is_configured():
            return {
                "dry_run": True,
                "message": "Shopify credentials not configured. Draft product simulated.",
                "product": {"title": title, "description": description, "price": price},
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
        headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
