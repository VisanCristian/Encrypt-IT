@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Change to the script directory so .venv is created in the repo root
cd /d "%~dp0"

REM Prefer the Python launcher if available
where py >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
  set "PY=py -3"
) ELSE (
  set "PY=python"
)

REM Verify Python is available
%PY% --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
  echo Python is not installed or not in PATH.
  echo Please install Python 3 and ensure it is on PATH.
  exit /b 1
)

REM Create virtual environment if it does not exist
IF NOT EXIST ".venv" (
  echo Creating virtual environment...
  %PY% -m venv .venv
)

REM Use venv's python directly for pip commands
set "VENV_PY=.venv\Scripts\python.exe"

echo Upgrading pip...
"%VENV_PY%" -m pip install --upgrade pip

REM Install requirements
IF EXIST "requirements.txt" (
  echo Installing dependencies from requirements.txt...
  "%VENV_PY%" -m pip install -r requirements.txt
) ELSE (
  echo requirements.txt not found!
  exit /b 1
)

echo Setup complete!
echo To run the app in this shell:
echo   call .venv\Scripts\activate
echo   python main.py
pause
