import os, base64, hashlib
from pathlib import Path
from urllib.parse import urlencode
from secrets import token_urlsafe

for line in Path(".env").read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k,v=line.split("=",1)
        os.environ[k.strip()] = v.strip()

client_id=os.getenv("ETSY_CLIENT_ID") or os.getenv("ETSY_API_KEY")
redirect_uri=os.getenv("ETSY_REDIRECT_URI","http://localhost:8080/callback")

verifier=token_urlsafe(64)
challenge=base64.urlsafe_b64encode(
    hashlib.sha256(verifier.encode()).digest()
).decode().rstrip("=")

Path("app/logs/etsy_pkce_verifier.txt").write_text(verifier, encoding="utf-8")

params={
    "response_type":"code",
    "redirect_uri":redirect_uri,
    "scope":"listings_r listings_w shops_r transactions_r",
    "client_id":client_id,
    "state":"aicommerce_etsy_auth",
    "code_challenge":challenge,
    "code_challenge_method":"S256"
}

print("Open this URL:")
print("https://www.etsy.com/oauth/connect?" + urlencode(params))
print()
print("After approval, copy the code= value from redirect URL into .env:")
print("ETSY_AUTH_CODE=...")
