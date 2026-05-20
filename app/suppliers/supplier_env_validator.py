import os

BAD_PLACEHOLDERS = [
    "your_",
    "example.com",
    "ВСТАВЬ",
    "INSERT_",
    "TODO",
]

def validate_supplier_env():
    url = os.getenv("SUPPLIER_API_URL", "")
    key = os.getenv("SUPPLIER_API_KEY", "")

    issues = []

    if not url:
        issues.append("SUPPLIER_API_URL is missing")

    for bad in BAD_PLACEHOLDERS:
        if bad.lower() in url.lower():
            issues.append(f"SUPPLIER_API_URL contains placeholder: {bad}")

        if bad.lower() in key.lower():
            issues.append(f"SUPPLIER_API_KEY contains placeholder: {bad}")

    return issues
