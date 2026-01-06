@echo off
chcp 65001 >nul
echo ========================================
echo   FUXA Documentation - Local Web Server
echo ========================================
echo.
echo Starting Web Server...
echo.
echo Please visit: http://localhost:8000
echo.
echo Press Ctrl+C to stop server
echo ========================================
echo.

cd /d "%~dp0"

python -m http.server 8000

pause
