# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run_server.py'],
    pathex=[],
    binaries=[],
    datas=[('app', 'app'), ('static', 'static'), ('.env', '.env')],
    hiddenimports=['fastapi', 'fastapi.staticfiles', 'fastapi.responses', 'uvicorn', 'starlette', 'pydantic', 'pydantic_settings', 'httpx', 'sqlalchemy', 'psycopg2', 'psycopg2_binary', 'dotenv', 'structlog', 'pythonjsonlogger', 'pythonjsonlogger', 'pythonjsonlogger.jsonlogger'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AutonomousAICommerce',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AutonomousAICommerce',
)
