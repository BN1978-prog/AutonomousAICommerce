import os

class ShopifyConfig:

    @staticmethod
    def get_store():
        return (
            os.getenv("SHOPIFY_STORE_URL")
            or os.getenv("SHOPIFY_STORE_DOMAIN")
            or ""
        ).replace("https://","").strip()

    @staticmethod
    def get_token():
        return (
            os.getenv("SHOPIFY_ADMIN_TOKEN")
            or os.getenv("SHOPIFY_ACCESS_TOKEN")
            or os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")
            or ""
        ).strip()

    @staticmethod
    def headers():
        return {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": ShopifyConfig.get_token()
        }
