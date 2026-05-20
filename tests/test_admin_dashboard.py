from fastapi.testclient import TestClient

from app.main import app
from app.dashboard.schemas import AutonomyControls


client = TestClient(app)


def test_dashboard_status_exposes_all_modules():
    response = client.get("/dashboard/status")
    assert response.status_code == 200
    data = response.json()
    assert data["modules"]["admin_dashboard"] == "online"
    assert data["modules"]["self_learning"] == "online"
    assert data["autonomy"]["dry_run"] is True


def test_dashboard_metrics_is_safe_default():
    response = client.get("/dashboard/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["estimated_daily_spend"] == 0.0
    assert data["risk_level"] == "low"


def test_emergency_stop_forces_autonomy_off():
    controls = AutonomyControls(enabled=True, emergency_stop=True).model_dump()
    response = client.put("/dashboard/controls", json=controls)
    assert response.status_code == 200
    data = response.json()
    assert data["emergency_stop"] is True
    assert data["enabled"] is False


def test_dashboard_html_loads():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "Autonomous AI Commerce Dashboard" in response.text
