from pathlib import Path

p = Path("app/suppliers/real_supplier.py")
s = p.read_text(encoding="utf-8")

insert = r'''
def refresh_cj_access_token_if_needed():
    api_url = os.getenv("CJ_API_URL") or os.getenv("SUPPLIER_API_URL")
    email = os.getenv("CJ_EMAIL", "")
    api_token = os.getenv("CJ_API_TOKEN", "")
    if not api_url or not email or not api_token:
        return

    auth_url = api_url.rstrip("/") + "/authentication/getAccessToken"
    response = httpx.post(auth_url, json={"email": email, "password": api_token}, timeout=30)
    data = response.json()
    token = (data.get("data") or {}).get("accessToken") or data.get("accessToken")
    refresh = (data.get("data") or {}).get("refreshToken") or data.get("refreshToken")

    if not token:
        return

    env_path = Path(".env")
    env = env_path.read_text(encoding="utf-8")
    import re
    env = re.sub(r"CJ_ACCESS_TOKEN=.*", "CJ_ACCESS_TOKEN=" + token, env)
    env = re.sub(r"SUPPLIER_API_KEY=.*", "SUPPLIER_API_KEY=" + token, env)
    if refresh:
        env = re.sub(r"CJ_REFRESH_TOKEN=.*", "CJ_REFRESH_TOKEN=" + refresh, env)
    env_path.write_text(env, encoding="utf-8")
    os.environ["CJ_ACCESS_TOKEN"] = token
    os.environ["SUPPLIER_API_KEY"] = token
'''

if "def refresh_cj_access_token_if_needed" not in s:
    s = s.replace("def extract_products", insert + "\n\ndef extract_products")

s = s.replace(
    "def fetch_real_supplier_products():",
    "def fetch_real_supplier_products():\n    refresh_cj_access_token_if_needed()"
)

p.write_text(s, encoding="utf-8")
print("PATCHED CJ TOKEN REFRESH")
