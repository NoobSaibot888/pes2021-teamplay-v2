#!/usr/bin/env python3
"""
Complete diagnosis of lobby sync between WordPress and PES
"""

import requests
import json
import time

def test_wordpress_api():
    """Test WordPress API"""
    print("🧪 TESTING WORDPRESS API...")
    print("=" * 50)
    
    api_url = "http://localhost:8080/wp-json/pes/v1/"
    
    try:
        # Test lobbies endpoint
        response = requests.get(f"{api_url}lobbies", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                lobbies = data.get('lobbies', [])
                print(f"✅ WordPress API: Found {len(lobbies)} lobbies")
                for lobby in lobbies:
                    print(f"   - {lobby.get('lobby_name', 'Unknown')} ({lobby.get('current_players', 0)}/{lobby.get('max_players', 0)})")
                return len(lobbies)
            else:
                print(f"⚠️ WordPress API no lobbies: {data}")
                return 0
        else:
            print(f"❌ WordPress API error: {response.status_code}")
            return 0
    except Exception as e:
        print(f"❌ WordPress API failed: {e}")
        return 0

def test_pes_server():
    """Test PES Server"""
    print("\n🎮 TESTING PES SERVER...")
    print("=" * 50)
    
    try:
        # Test server status
        response = requests.get("http://localhost/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ PES Server is running")
        else:
            print(f"❌ PES Server status error: {response.status_code}")
            return 0
    except Exception as e:
        print(f"❌ PES Server not accessible: {e}")
        return 0
    
    try:
        # Test lobbies endpoint
        response = requests.get("http://localhost/api/lobbies", timeout=5)
        if response.status_code == 200:
            data = response.json()
            lobbies = data.get('lobbies', [])
            total = data.get('total_lobbies', 0)
            print(f"📊 PES Server API: Found {total} lobbies")
            for lobby in lobbies:
                name = lobby.get('lobby_name', lobby.get('name', 'Unknown'))
                players = lobby.get('current_players', 0)
                max_players = lobby.get('max_players', 0)
                print(f"   - {name} ({players}/{max_players})")
            return total
        else:
            print(f"❌ PES lobbies error: {response.status_code}")
            return 0
    except Exception as e:
        print(f"❌ PES lobbies failed: {e}")
        return 0

def test_pes_game_message():
    """Test PES game message"""
    print("\n🎯 TESTING PES GAME MESSAGE...")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost/XME994-E1/info/info_en.txt", timeout=5)
        if response.status_code == 200:
            content = response.text
            print("📝 PES Game Message:")
            print("-" * 30)
            print(content)
            print("-" * 30)
            
            # Extract lobby count
            lines = content.split('\n')
            for line in lines:
                if 'Active Lobbies:' in line:
                    lobby_count = line.split(':')[-1].strip()
                    print(f"🔍 Extracted lobby count: {lobby_count}")
                    return int(lobby_count) if lobby_count.isdigit() else 0
            
            print("⚠️ Could not find lobby count in message")
            return 0
        else:
            print(f"❌ PES message error: {response.status_code}")
            return 0
    except Exception as e:
        print(f"❌ PES message failed: {e}")
        return 0

def main():
    """Main diagnosis"""
    print("🔍 LOBBY SYNC DIAGNOSIS")
    print("=" * 80)
    print("Testing all components to find sync issues...")
    print()
    
    # Test all components
    wp_lobbies = test_wordpress_api()
    pes_lobbies = test_pes_server() 
    game_lobbies = test_pes_game_message()
    
    # Summary
    print("\n📊 DIAGNOSIS SUMMARY")
    print("=" * 80)
    print(f"WordPress API Lobbies: {wp_lobbies}")
    print(f"PES Server API Lobbies: {pes_lobbies}")
    print(f"PES Game Message Lobbies: {game_lobbies}")
    print()
    
    # Analysis
    if wp_lobbies > 0 and pes_lobbies == 0:
        print("🔧 PROBLEM: PES Server not reading from WordPress API")
        print("SOLUTION: Restart PES server to load new code")
        print("RUN: restart_pes_server.bat")
    elif wp_lobbies == pes_lobbies and pes_lobbies == game_lobbies:
        print("✅ SUCCESS: All components synchronized!")
        print("WordPress → PES Server → PES Game working correctly")
    elif wp_lobbies == 0:
        print("🔧 PROBLEM: No lobbies in WordPress")
        print("SOLUTION: Create lobbies in WordPress interface")
        print("OPEN: http://localhost:8080/wordpress/wp-content/plugins/pes-teamplay-launcher-api/pes-lobby-interface.html")
    else:
        print("🔧 PROBLEM: Partial sync issue")
        print("Check server logs for detailed error messages")
    
    print("\n🎮 NEXT STEPS:")
    if wp_lobbies > 0 and game_lobbies > 0:
        print("1. Start PES 2021")
        print("2. Go to Team Play → Team Play Lobby")
        print("3. Check if message shows correct lobby count")
    else:
        print("1. Fix sync issues above")
        print("2. Restart PES server")
        print("3. Test again")

if __name__ == "__main__":
    main()