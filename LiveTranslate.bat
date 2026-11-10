@echo off
rem Launch LiveTranslate from the local virtualenv (no console window).
rem Run install.bat first if .venv is missing.
cd /d "%~dp0"
start "" "%~dp0.venv\Scripts\pythonw.exe" "main.py"