from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class WorkerState:
    enabled: bool = False
    dry_run: bool = True
    last_run_at: str | None = None
    cycle_count: int = 0
    last_action: str = "idle"

    def to_dict(self):
        return asdict(self)

    def mark_cycle(self, action: str):
        self.last_run_at = datetime.utcnow().isoformat() + "Z"
        self.cycle_count += 1
        self.last_action = action

worker_state = WorkerState()
