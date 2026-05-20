import json
from pathlib import Path
from datetime import datetime, timezone

TEST=Path("app/logs/meta_test_event.json")
STATE=Path("app/logs/event_collector_state.json")
OUT=Path("app/logs/event_collector_state.json")

test=json.loads(TEST.read_text(encoding="utf-8"))
state=json.loads(STATE.read_text(encoding="utf-8"))

if test.get("ok") and test.get("response",{}).get("events_received",0)>0:
    state["sources"]["meta_clicks"]=True
    state["event_learning_enabled"]=True
    state["reason"]="meta_events_received"
    state["last_meta_event_at"]=datetime.now(timezone.utc).isoformat()
    state["last_meta_event_id"]=test.get("event_id")

OUT.write_text(json.dumps(state,indent=2),encoding="utf-8")

print(json.dumps(state,indent=2))
