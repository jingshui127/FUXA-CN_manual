@echo off
chcp 65001 >nul
echo ========================================
echo   FUXA 汉化文档 - 完整版
echo ========================================
echo.
echo 正在打开浏览器...
echo.

cd /d "%~dp0"

start "" "FUXA汉化文档_完整版.html"

echo ✅ 文档已在浏览器中打开
echo.
echo ========================================
pause
