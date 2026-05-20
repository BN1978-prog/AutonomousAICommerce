
def save_published_product_record(job: dict, result: dict) -> dict:
    import json
    from pathlib import Path
    from datetime import datetime

    sku = job.get("sku") or job.get("payload", {}).get("sku")
    channel = job.get("channel")
    product_id = result.get("product_id")

    if not sku or not channel or not product_id:
        return {
            "ok": False,
            "message": "missing sku, channel, or product_id"
        }

    record = {
        "sku": sku,
        "channel": channel,
        "product_id": product_id,
        "admin_graphql_api_id": result.get("admin_graphql_api_id"),
        "title": result.get("title"),
        "status": result.get("status"),
        "created_at": datetime.now().isoformat(),
        "job": job,
        "result": result
    }

    path = Path("data/published_products") / f"{sku}-{channel}.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")

    return {
        "ok": True,
        "path": str(path),
        "record": record
    }


def update_product_record_price(sku: str, channel: str, price, result: dict) -> dict:
    import json
    from pathlib import Path
    from datetime import datetime

    path = Path("data/published_products") / f"{sku}-{channel}.json"

    if not path.exists():
        return {
            "ok": False,
            "message": f"record not found: {path}"
        }

    record = json.loads(path.read_text(encoding="utf-8"))

    record["last_price_update"] = {
        "price": price,
        "updated_at": datetime.now().isoformat(),
        "result": result
    }

    record["current_price"] = price

    path.write_text(json.dumps(record, indent=2), encoding="utf-8")

    return {
        "ok": True,
        "path": str(path),
        "current_price": price
    }


def update_product_record_status(sku: str, channel: str, status: str, result: dict) -> dict:
    import json
    from pathlib import Path
    from datetime import datetime

    path = Path("data/published_products") / f"{sku}-{channel}.json"

    if not path.exists():
        return {
            "ok": False,
            "message": f"record not found: {path}"
        }

    record = json.loads(path.read_text(encoding="utf-8"))

    record["status"] = status
    record["last_status_update"] = {
        "status": status,
        "updated_at": datetime.now().isoformat(),
        "result": result
    }

    path.write_text(json.dumps(record, indent=2), encoding="utf-8")

    return {
        "ok": True,
        "path": str(path),
        "status": status
    }


def update_product_record_inventory(sku: str, channel: str, quantity: int, result: dict) -> dict:
    import json
    from pathlib import Path
    from datetime import datetime

    path = Path("data/published_products") / f"{sku}-{channel}.json"

    if not path.exists():
        return {
            "ok": False,
            "message": f"record not found: {path}"
        }

    record = json.loads(path.read_text(encoding="utf-8"))

    record["current_inventory"] = quantity
    record["last_inventory_update"] = {
        "quantity": quantity,
        "updated_at": datetime.now().isoformat(),
        "result": result
    }

    path.write_text(json.dumps(record, indent=2), encoding="utf-8")

    return {
        "ok": True,
        "path": str(path),
        "current_inventory": quantity
    }

