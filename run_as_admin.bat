@echo off
REM Windows 11 Manager - Run as Administrator
REM This batch file will automatically request administrator privileges and run the launcher

echo.
echo ========================================
echo   Windows 11 Manager - Admin Launcher
echo ========================================
echo.

REM Check if colorama is installed for better color support
echo Checking for colorama (for better colors)...
python -c "import colorama" >nul 2>&1
if %errorLevel% neq 0 (
    echo Installing colorama for better color support...
    pip install colorama >nul 2>&1
    if %errorLevel% == 0 (
        echo Colorama installed successfully.
    ) else (
        echo Note: Could not install colorama. Colors may not display properly.
    )
) else (
    echo Colorama is already installed.
)

echo.
echo Requesting administrator privileges...
echo Please click "Yes" in the UAC dialog.
echo.

REM Check if already running as admin
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Already running as administrator.
    echo Starting Windows 11 Manager...
    echo.
    python launcher.py
) else (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process python -ArgumentList 'launcher.py' -Verb RunAs"
)

pause
