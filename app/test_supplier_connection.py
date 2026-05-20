import os
import httpx
from dotenv import load_dotenv
from app.suppliers.supplier_env_validator import validate_supplier_env

load_dotenv()

def main():
    url = os.getenv("SUPPLIER_API_URL")
    api_key = os.getenv("SUPPLIER_API_KEY")

    print("=== SUPPLIER CONNECTION TEST ===")

    issues = validate_supplier_env()
    if issues:
        print("Supplier config invalid:")
        for issue in issues:
            print(f"- {issue}")
        return

    if not url:
        print("SUPPLIER_API_URL missing")
        return

    print(f"URL: {url}")

    headers = {}

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = httpx.get(
            url,
            headers=headers,
            timeout=20
        )

        print(f"HTTP STATUS: {response.status_code}")

        preview = response.text[:500]
        print()
        print("=== RESPONSE PREVIEW ===")
        print(preview)

    except Exception as e:
        print()
        print("=== CONNECTION FAILED ===")
        print(str(e))

if __name__ == "__main__":
    main()
