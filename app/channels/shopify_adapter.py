import os
from app.channels.base import BaseChannelAdapter

class ShopifyAdapter(BaseChannelAdapter):
    channel_name = "shopify"

    def capabilities(self) -> dict:
        return {
            "create_draft": True,
            "publish": True,
            "update_price": True,
            "update_inventory": False,
            "disable_product": True,
            "read_orders": False,
            "read_performance": False
        }

    def _missing_config(self):
        missing = []

        if not os.getenv("SHOPIFY_STORE_URL"):
            missing.append("SHOPIFY_STORE_URL")

        if not os.getenv("SHOPIFY_ADMIN_TOKEN"):
            missing.append("SHOPIFY_ADMIN_TOKEN")

        return missing

    def status(self) -> dict:
        missing = self._missing_config()

        return {
            "enabled": len(missing) == 0,
            "status": "configured_preview" if not missing else "not_configured",
            "mode": "adapter_layer",
            "missing_config": missing,
            "capabilities": self.capabilities()
        }

    def validate_product(self, product: dict) -> dict:
        warnings = []

        if not product.get("title"):
            warnings.append("missing_title")

        if not product.get("sku"):
            warnings.append("missing_sku")

        if not product.get("price"):
            warnings.append("missing_price")

        return {
            "ok": len(warnings) == 0,
            "warnings": warnings,
            "product": product
        }

    def create_draft(self, product: dict) -> dict:
        if self._missing_config():
            return {
                "ok": False,
                "message": "Shopify API not configured. Draft creation blocked."
            }

        return {
            "ok": False,
            "message": "Shopify API configured, but live draft creation not implemented yet."
        }

    def publish(self, product: dict) -> dict:
        import os
        import requests

        if self._missing_config():
            return {
                "ok": False,
                "message": "Shopify API not configured. Publish blocked."
            }

        store = os.getenv("SHOPIFY_STORE_URL")
        token = os.getenv("SHOPIFY_ADMIN_TOKEN")

        url = f"https://{store}/admin/api/2024-01/products.json"

        payload = {
            "product": {
                "title": product.get("title"),
                "body_html": product.get("description", ""),
                "vendor": product.get("brand", ""),
                "product_type": product.get("category", ""),
                "status": "draft",
                "variants": [
                    {
                        "price": str(product.get("price", 0)),
                        "sku": product.get("sku")
                    }
                ]
            }
        }

        try:
            r = requests.post(
                url,
                headers={
                    "X-Shopify-Access-Token": token,
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=30
            )

            try:
                data = r.json()
            except Exception:
                data = {"raw": r.text}

            if r.status_code not in [200, 201]:
                return {
                    "ok": False,
                    "status_code": r.status_code,
                    "error": data
                }

            return {
                "ok": True,
                "status_code": r.status_code,
                "product_id": data["product"]["id"],
                "title": data["product"]["title"],
                "admin_graphql_api_id": data["product"].get("admin_graphql_api_id"),
                "status": data["product"].get("status")
            }

        except Exception as e:
            return {
                "ok": False,
                "message": str(e)
            }

    def update_price(self, sku: str, price: float) -> dict:
        if self._missing_config():
            return {
                "ok": False,
                "message": "Shopify API not configured. Price update blocked."
            }

        return {
            "ok": False,
            "message": "Shopify API configured, but live price update not implemented yet."
        }

    def update_inventory(self, sku: str, inventory: int) -> dict:
        return {
            "ok": False,
            "message": "Shopify inventory update not supported yet."
        }

    def disable_product(self, product_id: str) -> dict:
        if self._missing_config():
            return {
                "ok": False,
                "message": "Shopify API not configured. Disable blocked."
            }

        return {
            "ok": False,
            "message": "Shopify API configured, but live disable not implemented yet."
        }


    def update_product_price(self, product_id: int, price: float) -> dict:
        import os
        import requests

        store = os.getenv("SHOPIFY_STORE_URL")
        token = os.getenv("SHOPIFY_ADMIN_TOKEN")

        headers = {
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json"
        }

        product_url = f"https://{store}/admin/api/2024-01/products/{product_id}.json"

        product_response = requests.get(product_url, headers=headers, timeout=30)
        product_data = product_response.json()

        if product_response.status_code != 200:
            return {
                "ok": False,
                "status_code": product_response.status_code,
                "error": product_data
            }

        variants = product_data.get("product", {}).get("variants", [])

        if not variants:
            return {
                "ok": False,
                "message": "No variants found for product"
            }

        variant_id = variants[0]["id"]

        variant_url = f"https://{store}/admin/api/2024-01/variants/{variant_id}.json"

        update_response = requests.put(
            variant_url,
            headers=headers,
            json={
                "variant": {
                    "id": variant_id,
                    "price": str(price)
                }
            },
            timeout=30
        )

        update_data = update_response.json()

        if update_response.status_code not in [200, 201]:
            return {
                "ok": False,
                "status_code": update_response.status_code,
                "error": update_data
            }

        return {
            "ok": True,
            "status_code": update_response.status_code,
            "product_id": product_id,
            "variant_id": variant_id,
            "new_price": update_data["variant"]["price"]
        }


    def archive_product(self, product_id: int) -> dict:
        import os
        import requests

        store = os.getenv("SHOPIFY_STORE_URL")
        token = os.getenv("SHOPIFY_ADMIN_TOKEN")

        url = f"https://{store}/admin/api/2024-01/products/{product_id}.json"

        r = requests.put(
            url,
            headers={
                "X-Shopify-Access-Token": token,
                "Content-Type": "application/json"
            },
            json={
                "product": {
                    "id": product_id,
                    "status": "draft"
                }
            },
            timeout=30
        )

        data = r.json()

        if r.status_code not in [200, 201]:
            return {
                "ok": False,
                "status_code": r.status_code,
                "error": data
            }

        return {
            "ok": True,
            "status_code": r.status_code,
            "product_id": product_id,
            "status": data["product"].get("status")
        }

    def execute_publish_preview(self, job: dict) -> dict:
        return {
            "ok": True,
            "status": "published_preview",
            "channel": self.channel_name,
            "message": "Simulated Shopify publish success via ShopifyAdapter.",
            "external_id": f"preview-{job.get('job_id')}"
        }




