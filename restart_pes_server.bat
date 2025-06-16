@echo off
title Restart PES Server - Load New Code
color 0D
echo.
echo ========================================
echo   RESTART PES SERVER
echo   Loading new WordPress integration code
echo ========================================
echo.

echo This will stop and restart the PES server to load the fixed code.
echo Make sure no other process is using port 80.
echo.

echo Current status:
curl http://localhost/api/status 2>nul | findstr "version" || echo "Server not running or not accessible"
echo.

echo Killing any existing Python processes on port 80...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :80') do (
    taskkill /F /PID %%a 2>nul
)

echo Waiting 3 seconds...
timeout /t 3 /nobreak >nul

echo.
echo Starting PES server with new code...
echo.

cd /d "%~dp0"
python enhanced_pes_server_v2_for_pes_game.py

echo.
echo Server stopped.
pause