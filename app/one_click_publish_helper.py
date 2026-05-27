import webbrowser
from pathlib import Path

SRC = Path("app/logs/priority_publish_queue.txt")
OUT = Path("app/logs/next_post_to_publish.txt")

text = SRC.read_text(encoding="utf-8-sig")
text = text.replace("\ufeff", "").replace("ï»¿", "")

first = text.split("--- PRIORITY POST ---")[0].strip()

OUT.write_text(first, encoding="utf-8")

print("NEXT POST READY:", OUT)

webbrowser.open("https://business.facebook.com/latest/home")
webbrowser.open("https://www.instagram.com/")
webbrowser.open("https://www.pinterest.com/pin-builder/")
