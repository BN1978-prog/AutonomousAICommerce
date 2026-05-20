import os

def _float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except Exception:
        return default

def _bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name, str(default)).lower()
    return value in ("1", "true", "yes", "on")

class Governor:
    def status(self):
        return {
            "dry_run": _bool("DRY_RUN", True),
            "autonomy_enabled": _bool("AUTONOMY_ENABLED", False),
            "emergency_stop": _bool("EMERGENCY_STOP", False),
            "max_daily_spend": _float("MAX_DAILY_SPEND", 250),
            "min_margin_percent": _float("MIN_MARGIN_PERCENT", 25),
            "max_risk_score": _float("MAX_RISK_SCORE", 45),
        }

    def allow_action(self, estimated_spend: float, margin_percent: float, risk_score: float):
        s = self.status()
        if s["emergency_stop"]:
            return False, "Emergency stop is enabled."
        if estimated_spend > s["max_daily_spend"]:
            return False, "Estimated spend exceeds daily budget."
        if margin_percent < s["min_margin_percent"]:
            return False, "Margin is below minimum."
        if risk_score > s["max_risk_score"]:
            return False, "Risk score is too high."
        if s["dry_run"]:
            return True, "Allowed as dry-run simulation."
        if not s["autonomy_enabled"]:
            return False, "Autonomy is disabled."
        return True, "Allowed."
