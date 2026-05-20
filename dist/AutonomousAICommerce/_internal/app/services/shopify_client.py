import httpx
from app.config import settings

class ShopifyClient:
    def __init__(self):
        self.domain = settings.shopify_store_domain
        self.token = settings.shopify_admin_access_token

    async def create_product_draft(self, listing: dict) -> dict:
        if not self.domain or not self.token:
            return {
                "status": "SKIPPED",
                "reason": "Shopify credentials are not configured.",
                "listing": listing,
            }

        # Shopify Admin API integration placeholder.
        # Implement with the current Admin GraphQL API in production.
        return {
            "status": "TODO",
            "reason": "Connect Shopify Admin API here.",
            "listing": listing,
        }
