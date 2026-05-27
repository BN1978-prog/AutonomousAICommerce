from pathlib import Path

p=Path("app/meta_live_executor.py")
text=p.read_text(encoding="utf-8")

insert='''
# load .env
env_path = Path(".env")
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

'''

anchor='''ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")'''

if "# load .env" not in text:
    text=text.replace(anchor, insert + anchor)

p.write_text(text,encoding="utf-8")

print("env loader added to meta live executor")
