from app.main_STABLE_AI_SHOPIFY_PIPELINE import app

for route in app.routes:
    print(route.path, getattr(route, "methods", ""))
