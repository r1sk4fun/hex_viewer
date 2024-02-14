@echo off
@cd /d "%~dp0\.."

IF NOT EXIST .venv (
    python -m venv .venv
)

call .\.venv\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pip3 install -r requirements.txt
cls
python .\src\app.py
