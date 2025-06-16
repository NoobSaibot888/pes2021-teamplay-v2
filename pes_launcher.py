#!/usr/bin/env python3
"""
Enhanced PES 2021 Launcher с Web Interface Integration
Connects web lobby management with PES game launching
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import time
import subprocess
import threading
import os
import sys
import webbrowser
from datetime import datetime

class EnhancedPESLauncher:
    """Enhanced PES Launcher с Web Integration"""
    
    def __init__(self):
        self.wordpress_api = "http://localhost:8080/wp-json/pes/v1/"
        self.web_lobby_url = "http://localhost:8080/wordpress/wp-content/plugins/pes-teamplay-launcher-api/pes-lobby-interface.html"
        self.player_id = None
        self.player_name = None
        self.monitoring = False
        
        # GUI Setup
        self.setup_gui()
        
        # Check connections
        self.check_all_connections()
    
    def setup_gui(self):
        """Setup enhanced launcher GUI"""
        self.root = tk.Tk()
        self.root.title("PES 2021 TeamPlay Launcher - Web Enhanced")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Header
        header = tk.Label(self.root, text="🎮 PES 2021 TeamPlay Launcher", 
                         font=("Arial", 18, "bold"), fg="blue")
        header.pack(pady=15)
        
        subtitle = tk.Label(self.root, text="Web-Enhanced Lobby Management", 
                           font=("Arial", 12), fg="gray")
        subtitle.pack()
        
        # Status frame
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(status_frame, text="🌐 Connection Status:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.status_label = tk.Label(status_frame, text="Checking connections...", fg="orange")
        self.status_label.pack(anchor="w", padx=20)
        
        # Player registration frame
        player_frame = tk.LabelFrame(self.root, text="🏷️ Player Registration", padx=10, pady=10)
        player_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(player_frame, text="Player Name:").pack(anchor="w")
        self.player_entry = tk.Entry(player_frame, width=40, font=("Arial", 12))
        self.player_entry.pack(anchor="w", pady=5)
        self.player_entry.bind('<Return>', self.register_player)
        
        register_btn = tk.Button(player_frame, text="✅ Register Player", 
                               command=self.register_player, bg="#28a745", fg="white",
                               font=("Arial", 10, "bold"))
        register_btn.pack(anchor="w", pady=5)
        
        # Web lobby frame
        web_frame = tk.LabelFrame(self.root, text="🌐 Web Lobby Management", padx=10, pady=10)
        web_frame.pack(pady=10, padx=20, fill="x")
        
        lobby_info = tk.Label(web_frame, 
                             text="Use the web interface for full lobby management:\n• Create & join lobbies\n• Team formation\n• Real-time coordination",
                             justify=tk.LEFT)
        lobby_info.pack(anchor="w", pady=5)
        
        web_btn = tk.Button(web_frame, text="🚀 Open Web Lobby Interface", 
                           command=self.open_web_lobby, bg="#007cba", fg="white",
                           font=("Arial", 12, "bold"))
        web_btn.pack(anchor="w", pady=10)
        
        # Match monitoring frame
        monitor_frame = tk.LabelFrame(self.root, text="⚡ Match Monitoring", padx=10, pady=10)
        monitor_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(monitor_frame, text="Match Status:").pack(anchor="w")
        self.match_status = tk.Label(monitor_frame, text="Not monitoring", fg="gray")
        self.match_status.pack(anchor="w", padx=10)
        
        self.monitor_btn = tk.Button(monitor_frame, text="🔍 Start Match Monitoring", 
                                   command=self.toggle_monitoring, state="disabled",
                                   bg="#17a2b8", fg="white")
        self.monitor_btn.pack(anchor="w", pady=5)
        
        # Manual actions frame
        manual_frame = tk.LabelFrame(self.root, text="🎮 Game Actions", padx=10, pady=10)
        manual_frame.pack(pady=10, padx=20, fill="x")
        
        pes_btn = tk.Button(manual_frame, text="🎯 Launch PES 2021", 
                          command=self.launch_pes_manual, bg="#dc3545", fg="white",
                          font=("Arial", 11, "bold"))
        pes_btn.pack(side="left", padx=5)
        
        test_btn = tk.Button(manual_frame, text="🧪 Test Connections", 
                           command=self.check_all_connections, bg="#ffc107", fg="black")
        test_btn.pack(side="left", padx=5)
        
        # Activity log frame
        log_frame = tk.LabelFrame(self.root, text="📋 Activity Log", padx=10, pady=5)
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.log_text = tk.Text(log_frame, height=6, width=70, font=("Consolas", 9))
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        # Footer
        footer = tk.Label(self.root, text="Enhanced PES TeamPlay Launcher v2.0 - Web Integration", 
                         font=("Arial", 8), fg="gray")
        footer.pack(side="bottom", pady=5)
    
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        print(f"LOG: {message}")
    
    def check_all_connections(self):
        """Check all required connections"""
        self.log("🔍 Checking all connections...")
        
        # Test WordPress API
        try:
            response = requests.get(f"{self.wordpress_api}status", timeout=5)
            if response.status_code == 200:
                wp_status = "✅ WordPress API: Online"
                wp_color = "green"
            else:
                wp_status = "❌ WordPress API: Error"
                wp_color = "red"
        except:
            wp_status = "❌ WordPress API: Offline"
            wp_color = "red"
        
        # Test PES Server
        try:
            response = requests.get("http://localhost/api/status", timeout=5)
            if response.status_code == 200:
                pes_status = "✅ PES Server: Online"
            else:
                pes_status = "❌ PES Server: Error"
        except:
            pes_status = "❌ PES Server: Offline"
        
        # Update status
        status_text = f"{wp_status} | {pes_status}"
        self.status_label.config(text=status_text, fg=wp_color)
        self.log(f"Connection check: {status_text}")
        
        if "✅" in wp_status and "✅" in pes_status:
            self.log("🎉 All systems ready for 11vs11 matches!")
            return True
        else:
            self.log("⚠️ Some systems offline - check XAMPP and PES server")
            return False
    
    def register_player(self, event=None):
        """Register player with enhanced features"""
        player_name = self.player_entry.get().strip()
        if not player_name:
            messagebox.showerror("Error", "Please enter player name")
            return
        
        try:
            # Register player via WordPress API
            data = {
                "name": player_name,
                "launcher_version": "2.0-web-enhanced",
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(f"{self.wordpress_api}player/register", 
                                   json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                self.player_id = result.get('player_id')
                self.player_name = player_name
                
                self.log(f"✅ Player registered: {player_name} (ID: {self.player_id})")
                self.monitor_btn.config(state="normal")
                messagebox.showinfo("Success", f"Player {player_name} registered!\n\nNow you can:\n1. Open web lobby\n2. Start monitoring\n3. Join matches")
            else:
                self.log(f"❌ Registration failed: {response.text}")
                messagebox.showerror("Error", "Player registration failed")
                
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Registration error: {e}")
            messagebox.showerror("Error", f"Connection error: {e}")
    
    def open_web_lobby(self):
        """Open web lobby interface"""
        self.log(f"🌐 Opening web lobby interface...")
        webbrowser.open(self.web_lobby_url)
        self.log("💡 Use web interface to create/join lobbies")
        
        if not self.player_id:
            messagebox.showinfo("Tip", "Register your player first, then use the web interface to join lobbies!")
    
    def toggle_monitoring(self):
        """Start/stop match monitoring"""
        if not self.monitoring:
            self.start_monitoring()
        else:
            self.stop_monitoring()
    
    def start_monitoring(self):
        """Start monitoring for pending matches"""
        if not self.player_id:
            messagebox.showerror("Error", "Please register player first")
            return
        
        self.monitoring = True
        self.monitor_btn.config(text="⏸️ Stop Monitoring", bg="#dc3545")
        self.match_status.config(text="🔍 Monitoring for matches...", fg="blue")
        
        self.log("🔍 Started monitoring for matches")
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_matches, daemon=True)
        monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop match monitoring"""
        self.monitoring = False
        self.monitor_btn.config(text="🔍 Start Match Monitoring", bg="#17a2b8")
        self.match_status.config(text="⏸️ Monitoring stopped", fg="gray")
        
        self.log("⏸️ Stopped monitoring")
    
    def monitor_matches(self):
        """Monitor for pending matches (runs in thread)"""
        while self.monitoring:
            try:
                # Check for pending matches
                response = requests.get(f"{self.wordpress_api}player/{self.player_id}/pending-matches", 
                                      timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('match_ready'):
                        self.handle_match_ready(data['match'])
                        break
                    elif data.get('match_pending'):
                        pending_info = data['match_pending']
                        players_count = pending_info.get('current_players', 0)
                        max_players = pending_info.get('max_players', 22)
                        
                        status_text = f"⏳ Match pending: {players_count}/{max_players} players"
                        self.root.after(0, lambda: self.match_status.config(text=status_text, fg="orange"))
                    else:
                        self.root.after(0, lambda: self.match_status.config(text="🔍 Waiting for match...", fg="blue"))
                
            except requests.exceptions.RequestException as e:
                self.log(f"⚠️ Monitoring error: {e}")
            
            time.sleep(5)  # Check every 5 seconds
    
    def handle_match_ready(self, match_data):
        """Handle match ready signal"""
        self.log("🎉 MATCH READY! Preparing to launch PES...")
        
        # Update GUI
        self.root.after(0, lambda: self.match_status.config(text="🚀 MATCH READY - Launching PES!", fg="green"))
        
        # Show match info
        players_count = len(match_data.get('players', []))
        match_info = f"🎮 Match ready with {players_count} players!\n\nPES will launch automatically."
        
        self.root.after(0, lambda: messagebox.showinfo("🎉 Match Ready", match_info))
        
        # Launch PES with match data
        self.launch_pes_with_match(match_data)
    
    def launch_pes_with_match(self, match_data):
        """Launch PES with match data"""
        try:
            self.log("🚀 Launching PES 2021 with match data...")
            
            # Launch PES
            self.launch_pes_manual()
            
            # TODO: Implement P2P coordination
            # For now, players coordinate manually in PES
            
            self.log("✅ PES launched! Coordinate P2P in Team Play lobby.")
            
        except Exception as e:
            self.log(f"❌ Error launching PES: {e}")
            messagebox.showerror("Error", f"Failed to launch PES: {e}")
    
    def launch_pes_manual(self):
        """Manual PES launch"""
        try:
            # Try to find PES executable
            pes_paths = [
                "C:/Program Files (x86)/Steam/steamapps/common/eFootball PES 2021/PES2021.exe",
                "C:/Program Files/Steam/steamapps/common/eFootball PES 2021/PES2021.exe",
                "PES2021.exe"
            ]
            
            pes_path = None
            for path in pes_paths:
                if os.path.exists(path):
                    pes_path = path
                    break
            
            if pes_path:
                self.log(f"🎯 Launching PES from: {pes_path}")
                subprocess.Popen([pes_path])
                self.log("✅ PES 2021 launched successfully")
            else:
                self.log("⚠️ PES executable not found in common locations")
                messagebox.showwarning("Warning", "PES 2021 executable not found!\n\nPlease launch PES manually.")
                
        except Exception as e:
            self.log(f"❌ Error launching PES: {e}")
            messagebox.showerror("Error", f"Failed to launch PES: {e}")
    
    def run(self):
        """Start launcher GUI"""
        self.log("🎮 Enhanced PES TeamPlay Launcher started")
        self.log("💡 Register player → Open web lobby → Start monitoring → Play!")
        self.root.mainloop()

def main():
    """Start Enhanced PES Launcher"""
    print("🚀 Starting Enhanced PES 2021 TeamPlay Launcher...")
    
    launcher = EnhancedPESLauncher()
    launcher.run()

if __name__ == "__main__":
    main()