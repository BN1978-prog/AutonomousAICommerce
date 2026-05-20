import json
from pathlib import Path

MOCK_FILE = Path(r"C:\Users\omen\AutonomousAICommerce\app\suppliers\mock_real_supplier.json")

def fetch_mock_real_supplier_products():
    return json.loads(MOCK_FILE.read_text(encoding="utf-8-sig"))
