import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/channel_self_healer.json")

REPAIR_MODULES = {
    "meta": "app.meta_token_refresh",
    "shopify": "app.shopify_token_auto_repair"
}

CHECK_PROVIDER_NAMES = [
    "shopify",
    "woocommerce",
    "ebay",
    "google_ads",
    "meta"
]

def reload_env_from_file():
    env_path = Path(".env")

    if not env_path.exists():
        return False

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip()

    return True

def run_module(module):
    proc = subprocess.run(
        [sys.executable, "-m", module],
        capture_output=True,
        text=True
    )

    return {
        "module": module,
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-3000:],
        "stderr": proc.stderr[-3000:]
    }

def parse_json(stdout):
    try:
        return json.loads(stdout)
    except Exception:
        return {}

def provider_problem(item):
    ok = item.get("ok")
    status = str(item.get("status", "")).lower()
    code = item.get("status_code")

    if not ok:
        return True

    if code in [400, 401, 403]:
        return True

    bad_words = [
        "invalid",
        "expired",
        "unauthorized",
        "forbidden",
        "needs_reauth",
        "needs_new",
        "token_invalid"
    ]

    return any(x in status for x in bad_words)

def get_problems(report):
    problems = []

    for item in report.get("results", []):
        provider = item.get("provider")

        if provider not in CHECK_PROVIDER_NAMES:
            continue

        if provider_problem(item):
            problems.append({
                "provider": provider,
                "status": item.get("status"),
                "status_code": item.get("status_code"),
                "can_auto_refresh": item.get("can_auto_refresh")
            })

    return problems

def main():
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "env_reloaded": False,
        "initial_token_check": None,
        "initial_problems": [],
        "repair_attempts": [],
        "final_token_check": None,
        "final_problems": [],
        "status": None
    }

    first = run_module("app.token_manager")
    first_json = parse_json(first["stdout"])

    report["initial_token_check"] = first
    report["initial_problems"] = get_problems(first_json)

    if not report["initial_problems"]:
        report["status"] = "all_channels_ok_no_repair_needed"
    else:
        report["env_reloaded"] = reload_env_from_file()

        retry = run_module("app.token_manager")
        retry_json = parse_json(retry["stdout"])
        retry_problems = get_problems(retry_json)

        report["after_env_reload_token_check"] = retry
        report["after_env_reload_problems"] = retry_problems

        for problem in retry_problems:
            provider = problem["provider"]
            repair_module = REPAIR_MODULES.get(provider)

            if repair_module:
                repair = run_module(repair_module)
                report["repair_attempts"].append({
                    "provider": provider,
                    "repair_module": repair_module,
                    "result": repair
                })
            else:
                report["repair_attempts"].append({
                    "provider": provider,
                    "repair_module": None,
                    "result": "no_dedicated_repair_module_available"
                })

        final = run_module("app.token_manager")
        final_json = parse_json(final["stdout"])

        report["final_token_check"] = final
        report["final_problems"] = get_problems(final_json)

        report["status"] = (
            "self_healed_ok"
            if not report["final_problems"]
            else "some_channels_still_need_manual_fix"
        )

    OUT.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
