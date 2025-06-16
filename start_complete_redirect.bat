@echo off
title PES 2021 Complete Redirect - USING PES 2019 DATA
color 0F
echo.
echo ========================================
echo   PES 2021 COMPLETE REDIRECT SYSTEM
echo   Using PES 2019 Server Data for Max Compatibility
echo ========================================
echo.

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script requires Administrator privileges!
    echo Right-click and select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

echo Administrator privileges confirmed!
echo.

echo This redirect system uses PES 2019 server data patterns
echo because Konami uses similar servers across PES versions.
echo.
echo What this does:
echo - Redirects ALL PES 2021 domains to localhost
echo - Redirects PES 2019 domains (for compatibility)
echo - Redirects AWS endpoints from analysis
echo - Creates comprehensive hosts file entries
echo - Tests all redirections
echo.

echo IMPORTANT: After this, you MUST start the custom server:
echo 1. Run this redirect script
echo 2. Run start_full_server.bat
echo 3. Start PES 2021 and try Team Play Lobby
echo.

pause
echo.

echo Starting Complete Redirect System...
echo.

cd /d "%~dp0"
python pes_complete_redirect.py

echo.
echo Redirect system completed.
echo.
echo NEXT STEPS:
echo 1. Start custom server: start_full_server.bat
echo 2. Start PES 2021
echo 3. Try Team Play Lobby
echo.
pause