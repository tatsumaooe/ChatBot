@echo off
rem Double-click to start ChatBot and open it in your browser.
cd /d "%~dp0"
python -m model.server --open
pause
