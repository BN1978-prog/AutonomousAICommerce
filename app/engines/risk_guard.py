from datetime import datetime

RISK_CONFIG = {
    "max_single_action_amount": 100.0,
    "max_daily_spend": 500.0,
    "require_approval_above": 75.0,
    "enabled": True
}


class RiskGuard:

    def check(self, action: dict) -> dict:

        if not RISK_CONFIG["enabled"]:
            return {
                "ok": True,
                "allowed": True,
                "reason": "risk guard disabled"
            }

        amount = float(action.get("amount",0))

        if amount > RISK_CONFIG["max_single_action_amount"]:
            return {
                "ok": True,
                "allowed": False,
                "reason": "max_single_action_amount exceeded",
                "limit": RISK_CONFIG["max_single_action_amount"],
                "amount": amount
            }

        if amount > RISK_CONFIG["require_approval_above"]:
            return {
                "ok": True,
                "allowed": False,
                "approval_required": True,
                "reason": "manual approval required",
                "amount": amount
            }

        return {
            "ok": True,
            "allowed": True,
            "reason": "risk check passed",
            "checked_at": datetime.now().isoformat()
        }


def check_risk(action: dict):
    return RiskGuard().check(action)
