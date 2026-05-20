from __future__ import annotations

import os
import sys
import webbrowser
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

import uvicorn


def base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


if __name__ == "__main__":
    os.chdir(base_dir())
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False, log_level="info")
