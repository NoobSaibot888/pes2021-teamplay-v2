@echo off
title PES 2021 Enhanced Server V2 - FOR REAL PES GAME
color 0C
echo.
echo ========================================
echo   PES 2021 ENHANCED SERVER V2
echo   FOR REAL PES GAME - Port 80
echo   PHASE 6: Complete Game Integration
echo ========================================
echo.

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This requires Administrator privileges!
    echo Port 80 needs admin access for PES game compatibility.
    echo.
    echo Right-click this file and select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

echo Administrator privileges confirmed!
echo.

echo 🎮 PES GAME INTEGRATION FEATURES:
echo + Message interception for PES 2021
echo + Enhanced "servers online" message
echo + 11vs11 lobby functionality
echo + Real-time player coordination
echo + Enhanced database with match tracking
echo + Session management for players
echo + WordPress integration maintained
echo.

echo 🎯 CRITICAL PES ENDPOINTS:
echo - /XME994-E1/info/info_en.txt (PES reads this!)
echo - /XME994-E1/info/info_us.txt (PES reads this!)
echo - /api/status (Enhanced server info)
echo - /api/lobbies (Active 11vs11 lobbies)
echo.

echo 🔧 WHAT THIS DOES FOR PES GAME:
echo 1. Intercepts PES "servers offline" message
echo 2. Shows custom "servers online" message
echo 3. Provides enhanced lobby system
echo 4. Tracks players and matches
echo 5. Coordinates 11vs11 team play
echo.

echo 📋 BEFORE STARTING PES 2021:
echo 1. Start this server (keep running)
echo 2. Start domain redirect: start_complete_redirect.bat
echo 3. Launch PES 2021
echo 4. Go to Team Play Lobby
echo 5. You should see enhanced message!
echo.

echo ⚠️  IMPORTANT FOR TESTING:
echo - This server runs on port 80 (PES requirement)
echo - phpMyAdmin will not work while this is running
echo - Use port 8081 version for development
echo - This version is specifically for PES game testing
echo.

pause
echo.

echo Starting PES Game Server on Port 80...
echo Ready for PES 2021 Team Play Lobby connection...
echo.

cd /d "%~dp0"

python enhanced_pes_server_v2_for_pes_game.py

echo.
echo PES Game Server stopped.
echo.
pause