@echo off
title Enhanced PES 2021 TeamPlay Launcher - Web Integration
color 0B
echo.
echo ========================================
echo   ENHANCED PES 2021 TEAMPLAY LAUNCHER
echo   Web Integration Version 2.0
echo ========================================
echo.

echo 🎮 Features:
echo + WordPress API integration
echo + Web lobby interface
echo + Real-time match monitoring
echo + Automatic PES launching
echo + Full 11vs11 coordination
echo.

echo 📋 How to use:
echo 1. Register your player name
echo 2. Open web lobby interface
echo 3. Create or join lobbies via web
echo 4. Start match monitoring
echo 5. PES launches automatically when match ready
echo.

echo 🌐 Web Lobby URL:
echo http://localhost:8080/wordpress/wp-content/plugins/pes-teamplay-launcher-api/pes-lobby-interface.html
echo.

pause
echo.

echo Starting Enhanced Launcher...
echo.

cd /d "%~dp0"
python pes_launcher.py

echo.
echo Enhanced Launcher closed.
echo.
pause