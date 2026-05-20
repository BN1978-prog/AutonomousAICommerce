import os
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / "project_scan_report.txt"

SKIP_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "env",
    "node_modules", "dist", "build", ".pytest_cache",
    ".mypy_cache", ".idea", ".vscode", "backups"
}

TEXT_EXT = {
    ".py", ".html", ".css", ".js", ".ts", ".tsx", ".jsx",
    ".json", ".yaml", ".yml", ".toml", ".md", ".txt",
    ".env", ".example"
}

KEYWORDS = [
    "FastAPI", "uvicorn", "dashboard", "shopify", "supplier",
    "automation", "autonomy", "dry_run", "api", "router",
    "database", "sqlite", "postgres", "secret", "token",
    "openai", "import", "workflow", "safety", "products",
    "orders", "profit"
]

def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)

def read_text(path: Path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return f"[READ ERROR] {e}"

def main():
    files = []
    for path in ROOT.rglob("*"):
        if should_skip(path):
            continue
        if path.is_file():
            files.append(path)

    with OUT.open("w", encoding="utf-8") as f:
        f.write("AUTONOMOUS AI COMMERCE - PROJECT SCAN REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Root: {ROOT}\n")
        f.write(f"Total files scanned: {len(files)}\n\n")

        f.write("PROJECT TREE\n")
        f.write("-" * 70 + "\n")
        for path in sorted(files):
            rel = path.relative_to(ROOT)
            f.write(f"{rel}\n")

        f.write("\n\nIMPORTANT FILE SUMMARIES\n")
        f.write("-" * 70 + "\n")

        for path in sorted(files):
            rel = path.relative_to(ROOT)
            ext = path.suffix.lower()

            if ext not in TEXT_EXT and path.name not in [".env", ".env.local"]:
                continue

            text = read_text(path)
            lower = text.lower()
            hits = [k for k in KEYWORDS if k.lower() in lower]

            if hits:
                f.write(f"\nFILE: {rel}\n")
                f.write(f"KEYWORDS: {', '.join(hits)}\n")
                f.write(f"LINES: {text.count(chr(10)) + 1}\n")

                lines = text.splitlines()
                for i, line in enumerate(lines, start=1):
                    if any(k.lower() in line.lower() for k in KEYWORDS):
                        clean = line.strip()
                        if len(clean) > 220:
                            clean = clean[:220] + "..."
                        f.write(f"  L{i}: {clean}\n")

        f.write("\n\nPYTHON ROUTES / FUNCTIONS / CLASSES\n")
        f.write("-" * 70 + "\n")

        for path in sorted(files):
            if path.suffix.lower() != ".py":
                continue

            text = read_text(path)
            rel = path.relative_to(ROOT)

            f.write(f"\nFILE: {rel}\n")
            for i, line in enumerate(text.splitlines(), start=1):
                s = line.strip()
                if (
                    s.startswith("def ")
                    or s.startswith("async def ")
                    or s.startswith("class ")
                    or "@app." in s
                    or "@router." in s
                ):
                    f.write(f"  L{i}: {s}\n")

        f.write("\n\nPOSSIBLE CONFIG / ENV REFERENCES\n")
        f.write("-" * 70 + "\n")

        for path in sorted(files):
            ext = path.suffix.lower()
            if ext not in TEXT_EXT and path.name not in [".env", ".env.local"]:
                continue

            text = read_text(path)
            rel = path.relative_to(ROOT)

            for i, line in enumerate(text.splitlines(), start=1):
                s = line.strip()
                if any(word in s.lower() for word in ["os.getenv", "dotenv", "api_key", "secret", "token", "password", ".env"]):
                    if len(s) > 220:
                        s = s[:220] + "..."
                    f.write(f"{rel}:L{i}: {s}\n")

    print(f"Scan complete: {OUT}")

if __name__ == "__main__":
    main()
