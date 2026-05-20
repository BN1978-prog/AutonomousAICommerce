import os

def validate_runtime_safety():
    dry_run = os.getenv("DRY_RUN", "true").lower() == "true"
    supplier_mode = os.getenv("SUPPLIER_MODE", "sandbox").lower()

    issues = []

    if not dry_run and supplier_mode in ["mock_real", "sandbox"]:
        issues.append(
            f"Unsafe live run blocked: DRY_RUN=false with SUPPLIER_MODE={supplier_mode}"
        )

    return issues
