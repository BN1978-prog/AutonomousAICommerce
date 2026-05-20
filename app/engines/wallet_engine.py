import json
from pathlib import Path
from datetime import datetime, date
from uuid import uuid4

WALLET_DIR = Path("data/wallet")
WALLET_FILE = WALLET_DIR / "wallet.json"
LEDGER_FILE = WALLET_DIR / "ledger.jsonl"

DEFAULT_WALLET = {
    "currency": "GBP",
    "available_balance": 0.0,
    "reserved_balance": 0.0,
    "total_income": 0.0,
    "total_expense": 0.0,
    "daily_spend_limit": 75.0,
    "min_reserve": 0.0,
    "auto_mode": True,
    "updated_at": None
}


def _ensure_wallet():
    WALLET_DIR.mkdir(parents=True, exist_ok=True)

    if not WALLET_FILE.exists():
        wallet = DEFAULT_WALLET.copy()
        wallet["updated_at"] = datetime.now().isoformat()
        WALLET_FILE.write_text(json.dumps(wallet, indent=2), encoding="utf-8")

    if not LEDGER_FILE.exists():
        LEDGER_FILE.write_text("", encoding="utf-8")


def get_wallet() -> dict:
    _ensure_wallet()
    return json.loads(WALLET_FILE.read_text(encoding="utf-8"))


def save_wallet(wallet: dict) -> dict:
    wallet["updated_at"] = datetime.now().isoformat()
    WALLET_FILE.write_text(json.dumps(wallet, indent=2), encoding="utf-8")
    return wallet


def record_transaction(tx_type: str, amount: float, source: str = None, note: str = None, metadata: dict = None) -> dict:
    _ensure_wallet()

    tx = {
        "id": str(uuid4()),
        "type": tx_type,
        "amount": round(float(amount), 2),
        "source": source,
        "note": note,
        "metadata": metadata or {},
        "created_at": datetime.now().isoformat()
    }

    with LEDGER_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(tx) + "\n")

    return tx


def get_ledger(limit: int = 50) -> dict:
    _ensure_wallet()

    lines = LEDGER_FILE.read_text(encoding="utf-8").splitlines()
    items = []

    for line in lines[-limit:]:
        if line.strip():
            items.append(json.loads(line))

    return {
        "ok": True,
        "transactions": items,
        "count": len(items)
    }


def get_today_spend() -> float:
    _ensure_wallet()

    today = date.today().isoformat()
    total = 0.0

    for line in LEDGER_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue

        tx = json.loads(line)

        if tx.get("type") in ["spend", "withdraw"] and str(tx.get("created_at", "")).startswith(today):
            total += float(tx.get("amount", 0))

    return round(total, 2)


def deposit(amount: float, source: str = "manual", note: str = None) -> dict:
    wallet = get_wallet()
    amount = round(float(amount), 2)

    if amount <= 0:
        return {"ok": False, "message": "amount must be positive"}

    wallet["available_balance"] = round(wallet["available_balance"] + amount, 2)

    tx = record_transaction("deposit", amount, source, note)
    save_wallet(wallet)

    return {"ok": True, "wallet": wallet, "transaction": tx}


def withdraw(amount: float, destination: str = "manual", note: str = None) -> dict:
    wallet = get_wallet()
    amount = round(float(amount), 2)

    if amount <= 0:
        return {"ok": False, "message": "amount must be positive"}

    if amount > wallet["available_balance"]:
        return {
            "ok": False,
            "message": "insufficient available balance",
            "available_balance": wallet["available_balance"],
            "requested": amount
        }

    wallet["available_balance"] = round(wallet["available_balance"] - amount, 2)

    tx = record_transaction("withdraw", amount, destination, note)
    save_wallet(wallet)

    return {"ok": True, "wallet": wallet, "transaction": tx}


def can_spend(amount: float, reason: str = None) -> dict:
    wallet = get_wallet()
    amount = round(float(amount), 2)

    protected_available = round(wallet["available_balance"] - wallet.get("min_reserve", 0), 2)
    today_spend = get_today_spend()
    daily_limit = float(wallet.get("daily_spend_limit", 0))

    if amount <= 0:
        return {"ok": True, "allowed": True, "amount": amount, "reason": "no spend required"}

    if amount > protected_available:
        return {
            "ok": True,
            "allowed": False,
            "reason": "insufficient wallet balance",
            "amount": amount,
            "available_balance": wallet["available_balance"],
            "protected_available": protected_available
        }

    if daily_limit > 0 and today_spend + amount > daily_limit:
        return {
            "ok": True,
            "allowed": False,
            "reason": "daily spend limit exceeded",
            "amount": amount,
            "today_spend": today_spend,
            "daily_spend_limit": daily_limit
        }

    return {
        "ok": True,
        "allowed": True,
        "amount": amount,
        "reason": reason or "wallet check passed",
        "available_balance": wallet["available_balance"],
        "today_spend": today_spend,
        "daily_spend_limit": daily_limit
    }


def reserve(amount: float, reason: str = None, metadata: dict = None) -> dict:
    wallet = get_wallet()
    amount = round(float(amount), 2)

    check = can_spend(amount, reason)

    if not check.get("allowed"):
        return {
            "ok": False,
            "message": "wallet reserve denied",
            "check": check
        }

    if amount <= 0:
        return {
            "ok": True,
            "reserved": False,
            "message": "no reserve required",
            "wallet": wallet
        }

    wallet["available_balance"] = round(wallet["available_balance"] - amount, 2)
    wallet["reserved_balance"] = round(wallet["reserved_balance"] + amount, 2)

    tx = record_transaction("reserve", amount, "wallet_engine", reason, metadata)
    save_wallet(wallet)

    return {
        "ok": True,
        "reserved": True,
        "wallet": wallet,
        "transaction": tx
    }


def spend(amount: float, reason: str = None, metadata: dict = None) -> dict:
    wallet = get_wallet()
    amount = round(float(amount), 2)

    if amount <= 0:
        return {"ok": True, "spent": False, "message": "no spend required", "wallet": wallet}

    if amount > wallet["reserved_balance"]:
        return {
            "ok": False,
            "message": "insufficient reserved balance",
            "reserved_balance": wallet["reserved_balance"],
            "requested": amount
        }

    wallet["reserved_balance"] = round(wallet["reserved_balance"] - amount, 2)
    wallet["total_expense"] = round(wallet["total_expense"] + amount, 2)

    tx = record_transaction("spend", amount, "wallet_engine", reason, metadata)
    save_wallet(wallet)

    return {"ok": True, "spent": True, "wallet": wallet, "transaction": tx}


def release(amount: float, reason: str = None, metadata: dict = None) -> dict:
    wallet = get_wallet()
    amount = round(float(amount), 2)

    if amount <= 0:
        return {"ok": True, "released": False, "message": "no release required", "wallet": wallet}

    if amount > wallet["reserved_balance"]:
        amount = wallet["reserved_balance"]

    wallet["reserved_balance"] = round(wallet["reserved_balance"] - amount, 2)
    wallet["available_balance"] = round(wallet["available_balance"] + amount, 2)

    tx = record_transaction("release", amount, "wallet_engine", reason, metadata)
    save_wallet(wallet)

    return {"ok": True, "released": True, "wallet": wallet, "transaction": tx}


def record_income(amount: float, source: str = "manual", note: str = None, metadata: dict = None) -> dict:
    wallet = get_wallet()
    amount = round(float(amount), 2)

    if amount <= 0:
        return {"ok": False, "message": "amount must be positive"}

    wallet["available_balance"] = round(wallet["available_balance"] + amount, 2)
    wallet["total_income"] = round(wallet["total_income"] + amount, 2)

    tx = record_transaction("income", amount, source, note, metadata)
    save_wallet(wallet)

    return {"ok": True, "wallet": wallet, "transaction": tx}
