from dotenv import load_dotenv
load_dotenv(override=True)

from app.channels.meta_adapter import validate_meta_config

print("=== META HEALTH ===")

result=validate_meta_config()

print(result)
