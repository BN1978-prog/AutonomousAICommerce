from app.suppliers.title_optimizer import optimize_title

def optimize_listing_text(product):
    title = optimize_title(product["title"])
    description = product["description"].strip()

    optimized_description = description

    if "Free UK delivery." not in optimized_description:
        optimized_description += "\n\nFree UK delivery."

    product["title"] = title
    product["description"] = optimized_description

    return product
