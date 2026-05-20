from datetime import datetime, timezone
from typing import Any

AUDIT_LOG: list[dict[str, Any]] = []

class AuditLogger:
    def log(self, event_type: str, payload: dict):
        AUDIT_LOG.append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "payload": payload,
        })

    def all(self):
        return AUDIT_LOG[-500:]
