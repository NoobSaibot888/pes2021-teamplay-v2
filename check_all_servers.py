#!/usr/bin/env python3
"""
Check if all required servers are running
"""

import requests
import socket

def check_port(host, port, name):
    """Check if port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            print(f"✅ {name} (port {port}): RUNNING")
            return True
        else:
            print(f"❌ {name} (port {port}): NOT RUNNING")
            return False
    except Exception as e:
        print(f"❌ {name} (port {port}): ERROR - {e}")
        return False

def main():
    print("🔍 CHECKING ALL REQUIRED SERVERS")
    print("=" * 50)
    
    # Check all required services
    services = [
        ("localhost", 8080, "XAMPP/WordPress"),
        ("localhost", 80, "PES Server"),
        ("localhost", 3306, "MySQL (XAMPP)"),
    ]
    
    all_running = True
    for host, port, name in services:
        running = check_port(host, port, name)
        if not running:
            all_running = False
    
    print("\n📋 STARTUP GUIDE:")
    print("=" * 50)
    print("1. Start XAMPP Control Panel")
    print("2. Start Apache (port 8080)")
    print("3. Start MySQL") 
    print("4. Verify WordPress: http://localhost:8080/wordpress")
    print("5. Start PES Server: restart_pes_server.bat")
    print("6. Test everything: python diagnose_lobby_sync.py")
    
    if all_running:
        print("\n✅ ALL SERVICES RUNNING - Ready to test!")
    else:
        print("\n❌ SOME SERVICES NOT RUNNING - Fix startup issues first")

if __name__ == "__main__":
    main()