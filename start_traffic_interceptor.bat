@echo off
title PES 2021 Traffic Interceptor - HARDCORE MODE
color 0E
echo.
echo ========================================
echo   PES 2021 TRAFFIC INTERCEPTOR
echo   ADVANCED PROTOCOL ANALYSIS
echo ========================================
echo.

echo This is the MOST ADVANCED network analysis tool!
echo.
echo What this tool does:
echo - Real-time traffic capture on all PES ports
echo - Deep packet analysis and pattern recognition
echo - Binary protocol reverse engineering
echo - Automatic protocol detection
echo - Live hex dump analysis
echo.

echo Monitored ports:
echo - TCP 80  (HTTP)
echo - TCP 443 (HTTPS)
echo - TCP 8000 (Game server)
echo - UDP 5739 (P2P communication)
echo - UDP 5740 (P2P communication)
echo - UDP 3478 (STUN server)
echo.

echo This tool will capture EVERYTHING that PES sends!
echo Perfect for understanding the exact protocol.
echo.

pause
echo.

echo Starting ADVANCED TRAFFIC INTERCEPTOR...
echo.

cd /d "%~dp0"
python pes_traffic_interceptor.py

echo.
echo Traffic analysis completed.
pause