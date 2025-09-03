@echo off
setlocal
pip install -r requirements.txt
pyinstaller --noconsole --onefile --name "AurantisSync" aurantis_sync_mvp.py
pause
