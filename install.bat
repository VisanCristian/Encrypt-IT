@echo off

REM Stop on errors
SETLOCAL ENABLEDELAYEDEXPANSION

REM Check Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH
    echo Please install Python3 first or add it in PATH
    exit /b 1
)

REM Create virtual environment if not exists
IF NOT EXIST ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
IF EXIST "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) ELSE (
    echo requirements.txt not found!
    exit /b 1
)

echo Setup complete!
echo You can run the program with:
echo   .venv\Scripts\activate
echo   python main.py
pause
