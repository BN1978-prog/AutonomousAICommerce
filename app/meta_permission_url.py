from urllib.parse import urlencode

APP_ID="ВАШ_META_APP_ID"
REDIRECT_URI="https://www.facebook.com/connect/login_success.html"

params = {
    "client_id": APP_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": ",".join([
        "pages_show_list",
        "pages_read_engagement",
        "pages_manage_posts",
        "business_management",
        "instagram_basic",
        "instagram_content_publish"
    ]),
    "response_type":"token"
}

url = "https://www.facebook.com/v23.0/dialog/oauth?" + urlencode(params)

print(url)
