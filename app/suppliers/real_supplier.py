import os
import re
from pathlib import Path

import httpx


def extract_products(data, path):
    current = data
    for part in path.split("."):
        current = current[part]
    return current


def save_env_value(name, value):
    env_path = Path(".env")
    env = env_path.read_text(encoding="utf-8")
    if re.search(rf"^{name}=.*", env, flags=re.MULTILINE):
        env = re.sub(rf"^{name}=.*", f"{name}={value}", env, flags=re.MULTILINE)
    else:
        env += f"\n{name}={value}\n"
    env_path.write_text(env, encoding="utf-8")
    os.environ[name] = value


def refresh_cj_access_token():
    api_url = os.getenv("CJ_API_URL") or os.getenv("SUPPLIER_API_URL")
    email = os.getenv("CJ_EMAIL", "")
    api_token = os.getenv("CJ_API_TOKEN", "")

    auth_url = api_url.rstrip("/") + "/authentication/getAccessToken"
    response = httpx.post(
        auth_url,
        json={"email": email, "password": api_token},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    token = (data.get("data") or {}).get("accessToken")
    refresh = (data.get("data") or {}).get("refreshToken")

    if not token:
        raise ValueError("CJ access token was not returned")

    save_env_value("CJ_ACCESS_TOKEN", token)
    save_env_value("SUPPLIER_API_KEY", token)

    if refresh:
        save_env_value("CJ_REFRESH_TOKEN", refresh)

    return token


def fetch_real_supplier_products():
    url = os.getenv("SUPPLIER_API_URL", "").rstrip("/")
    endpoint = os.getenv("SUPPLIER_PRODUCTS_ENDPOINT", "product/list").strip("/")
    products_path = os.getenv("SUPPLIER_PRODUCTS_PATH", "data.list")

    token = refresh_cj_access_token()

    headers = {
        "CJ-Access-Token": token
    }

    response = httpx.get(
        url + "/" + endpoint,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    products = extract_products(data, products_path)

    if not isinstance(products, list):
        raise ValueError("Supplier products response is not a list")

    return products
