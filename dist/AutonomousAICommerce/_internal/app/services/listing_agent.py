from app.models import ProductCandidate

class ListingAgent:
    def generate_listing(self, product: ProductCandidate) -> dict:
        title = product.title.strip().title()

        description = (
            f"{title}\n\n"
            f"Category: {product.category}\n"
            f"Ships from: {product.source_country}\n"
            f"Estimated delivery: {product.delivery_days} days\n\n"
            "This listing should be reviewed for marketplace compliance before publishing."
        )

        tags = [
            product.category.lower().replace(" ", "-"),
            product.target_market.lower(),
            "fast-delivery" if product.delivery_days <= 7 else "standard-delivery",
        ]

        return {
            "title": title[:120],
            "description": description,
            "price": product.estimated_sale_price,
            "tags": tags,
            "status": "draft",
        }
