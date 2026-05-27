import json
from pathlib import Path

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

master = read_json("app/logs/master_system_health.json")
dashboard = read_json("app/logs/system_status_dashboard.json")
alerts = read_json("app/logs/alerts.json")
crm = read_json("app/logs/crm_final_gate.json")
smtp = read_json("app/logs/smtp_config_validator.json")
niche = read_json("app/logs/niche_exclusion_summary.json")
global_channels = read_json("app/logs/global_channel_status_summary.json")

print("========== AUTONOMOUS AI COMMERCE STATUS ==========")
print("SYSTEM:", dashboard.get("system_status"))
print("STATUS:", dashboard.get("status"))
print("SAFE:", dashboard.get("safe_to_continue"))
print("LIVE MONEY SPENDING:", dashboard.get("live_money_spending"))
print("MASTER HEALTH:", master.get("status"))
print("FAILED CHECKS:", master.get("failed_count"))
print("ALERTS:", alerts.get("alerts_count"))
print("CRITICAL:", alerts.get("critical_count"))
print("GOOGLE:", dashboard.get("google_status"))
print("META:", dashboard.get("meta_activation"))
print("REAL SALES:", dashboard.get("real_sales_mode"))
print("QUEUE:", dashboard.get("purchase_queue_size"))
print("CRM:", crm.get("status"))
print("SMTP:", smtp.get("status"))
print("PET NICHE:", niche.get("status"))
print("EXCLUDED SKUS:", niche.get("excluded_skus"))
print("GLOBAL READY CHANNELS:", global_channels.get("env_ready_channels"))
print("GLOBAL NOT READY:", global_channels.get("not_ready_channels"))
print("===================================================")
