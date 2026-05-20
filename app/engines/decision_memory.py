import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4

MEMORY_DIR = Path("data/brain")
DECISION_LOG = MEMORY_DIR / "decision_log.jsonl"


def _ensure_memory():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    if not DECISION_LOG.exists():
        DECISION_LOG.write_text("", encoding="utf-8")


def record_decision(entry: dict) -> dict:
    _ensure_memory()

    item = {
        "id": str(uuid4()),
        "created_at": datetime.now().isoformat(),
        **entry
    }

    with DECISION_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item) + "\n")

    return {
        "ok": True,
        "decision_id": item["id"],
        "recorded_at": item["created_at"]
    }


def get_decisions(limit: int = 50) -> dict:
    _ensure_memory()

    lines = DECISION_LOG.read_text(encoding="utf-8").splitlines()
    items = []

    for line in lines[-limit:]:
        if line.strip():
            items.append(json.loads(line))

    return {
        "ok": True,
        "count": len(items),
        "decisions": items
    }


def get_failed_decisions(limit: int = 50) -> dict:
    _ensure_memory()

    lines = DECISION_LOG.read_text(encoding="utf-8").splitlines()
    failed = []

    for line in lines:
        if not line.strip():
            continue

        item = json.loads(line)

        if item.get("ok") is False:
            failed.append(item)

    return {
        "ok": True,
        "count": len(failed[-limit:]),
        "failed_decisions": failed[-limit:]
    }


def summarize_memory() -> dict:
    _ensure_memory()

    lines = DECISION_LOG.read_text(encoding="utf-8").splitlines()

    total = 0
    success = 0
    failed = 0
    channels = {}
    rules = {}

    for line in lines:
        if not line.strip():
            continue

        item = json.loads(line)
        total += 1

        if item.get("ok"):
            success += 1
        else:
            failed += 1

        for channel in item.get("channels", []):
            channels[channel] = channels.get(channel, 0) + 1

        rule = item.get("rule")
        if rule:
            rules[rule] = rules.get(rule, 0) + 1

    return {
        "ok": True,
        "total_decisions": total,
        "success": success,
        "failed": failed,
        "channels": channels,
        "rules": rules
    }
