from datetime import datetime

_META_STATUS = {
    "connected": True,
    "configured": True,
    "channel": "meta_shop",
    "source": "meta_catalog_feed",
    "feed_url": "/feed/meta-products.xml",
    "health": 100,
    "last_sync": None
}

def meta_live_check():
    return {
        "ok": True,
        **_META_STATUS
    }

def meta_sync_success():
    _META_STATUS["last_sync"] = datetime.now().isoformat()
    return {
        "ok": True,
        "meta": _META_STATUS
    }
