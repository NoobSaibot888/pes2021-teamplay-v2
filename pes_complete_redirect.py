#!/usr/bin/env python3
"""
PES 2021 Complete Redirect System
Uses PES 2019 data to understand patterns and create complete redirect
"""

import os
import subprocess
import socket
import time

class PESCompleteRedirect:
    """Complete redirection system for PES to custom server"""
    
    def __init__(self):
        # PES 2019 server data (found by user) - this gives us patterns!
        self.pes2019_ips = [
            '34.209.179.167', '34.218.118.205', '35.165.128.235', 
            '35.197.63.107', '35.197.250.120', '35.198.57.112',
            '35.199.30.185', '35.204.253.149', '35.234.95.118',
            '35.240.164.139', '52.17.173.247', '52.18.94.153',
            '52.49.218.253', '52.208.162.2', '52.208.190.137',
            '54.214.158.254', '72.247.153.153', '104.125.7.33',
            '210.148.52.94', '210.148.52.95'
        ]
        
        self.pes2019_domains = [
            'srv01.codefusion.technology',
            'srv02.codefusion.technology', 
            'srv03.codefusion.technology',
            'support.codefusion.technology',
            'ntl.service.konami.net',
            'ntleu.service.konami.net',
            'pes19-x64-gate.cs.konami.net',
            'legal.konami.com',
            'pes2019-dl.akamaized.net',
            'pes19-x64-stun.cs.konami.net'
        ]
        
        # PES 2021 equivalents (discovered from our analysis)
        self.pes2021_domains = [
            'pes21-x64-gate.cs.konami.net',
            'pes21-x64-stun.cs.konami.net',
            'info.service.konami.net',
            'cs.konami.net',
            'ntl.service.konami.net',
            'ntleu.service.konami.net'
        ]
        
        # Our server endpoints
        self.local_server_ip = '127.0.0.1'
        self.server_ports = {
            'http': 80,
            'https': 443,
            'game': 8000,
            'p2p1': 5739,
            'p2p2': 5740
        }
    
    def create_complete_hosts_redirect(self):
        """Create complete hosts file redirect using all discovered data"""
        print("🔧 CREATING COMPLETE HOSTS REDIRECT")
        print("=" * 60)
        
        # Read current hosts file
        hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
        
        try:
            with open(hosts_path, 'r', encoding='utf-8') as f:
                current_hosts = f.read()
        except:
            current_hosts = ""
        
        # Build new hosts entries
        new_entries = []
        new_entries.append("\n# PES 2021 Custom Server Redirect - Complete")
        new_entries.append(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        new_entries.append("")
        
        # Redirect all PES 2021 domains
        new_entries.append("# PES 2021 Game Servers")
        for domain in self.pes2021_domains:
            new_entries.append(f"{self.local_server_ip} {domain}")
        
        # Also redirect PES 2019 domains (in case game uses them)
        new_entries.append("")
        new_entries.append("# PES 2019 Compatibility")
        for domain in self.pes2019_domains:
            new_entries.append(f"{self.local_server_ip} {domain}")
        
        # Add AWS endpoints from our analysis
        new_entries.append("")
        new_entries.append("# AWS Endpoints")
        new_entries.append(f"{self.local_server_ip} ec2-35-174-175-11.compute-1.amazonaws.com")
        new_entries.append(f"{self.local_server_ip} server-18-244-79-54.sof50.r.cloudfront.net")
        
        # Add discovered endpoints
        new_entries.append("")
        new_entries.append("# Additional Game Endpoints")
        additional_domains = [
            "cf-revalidation-1750743123.eu-west-1.elb.amazonaws.com",
            "pes21-dl.akamaized.net",
            "pes2021-dl.akamaized.net",
            "codefusion.technology",
            "legal.konami.com"
        ]
        
        for domain in additional_domains:
            new_entries.append(f"{self.local_server_ip} {domain}")
        
        new_entries.append("")
        new_entries.append("# End PES Custom Server Redirect")
        new_entries.append("")
        
        # Combine with existing hosts
        new_hosts_content = current_hosts + '\n'.join(new_entries)
        
        # Show what we're adding
        print("📝 ADDING THESE REDIRECTS:")
        for entry in new_entries:
            if entry.strip() and not entry.startswith('#'):
                print(f"   {entry}")
        
        print(f"\n💾 Total redirects: {len([e for e in new_entries if e.strip() and not e.startswith('#')])}")
        
        return new_hosts_content, hosts_path
    
    def create_ip_route_redirects(self):
        """Create IP-level redirects for discovered IPs"""
        print("\n🛤️ CREATING IP ROUTE REDIRECTS")
        print("=" * 60)
        
        # Create batch commands for IP redirects
        route_commands = []
        
        # Redirect known PES 2019 IPs (they might be reused in PES 2021)
        important_ips = [
            '35.197.63.107',    # Google Cloud (similar to our 35.174.175.11)
            '35.234.95.118',    # Google Cloud
            '52.208.162.2',     # AWS Ireland
            '54.214.158.254',   # AWS Oregon
        ]
        
        for ip in important_ips:
            # Route traffic to our local server
            route_commands.append(f'route add {ip} mask 255.255.255.255 {self.local_server_ip} metric 1')
        
        return route_commands
    
    def apply_complete_redirect(self):
        """Apply complete redirect system"""
        print("🚀 APPLYING COMPLETE PES REDIRECT SYSTEM")
        print("=" * 80)
        
        try:
            # 1. Create hosts redirect
            new_hosts, hosts_path = self.create_complete_hosts_redirect()
            
            # Write hosts file
            with open(hosts_path, 'w', encoding='utf-8') as f:
                f.write(new_hosts)
            
            print("✅ Hosts file updated successfully")
            
            # 2. Flush DNS cache
            print("\n🔄 Flushing DNS cache...")
            subprocess.run(['ipconfig', '/flushdns'], check=True, capture_output=True)
            print("✅ DNS cache flushed")
            
            # 3. Create route redirects (optional)
            route_commands = self.create_ip_route_redirects()
            
            print(f"\n📋 OPTIONAL: To redirect IP traffic, run these commands as Administrator:")
            for cmd in route_commands:
                print(f"   {cmd}")
            
            # 4. Test redirects
            print("\n🧪 TESTING REDIRECTS:")
            test_domains = [
                'pes21-x64-gate.cs.konami.net',
                'ntl.service.konami.net',
                'cs.konami.net'
            ]
            
            for domain in test_domains:
                try:
                    ip = socket.gethostbyname(domain)
                    if ip == self.local_server_ip:
                        print(f"   ✅ {domain} → {ip}")
                    else:
                        print(f"   ❌ {domain} → {ip} (should be {self.local_server_ip})")
                except Exception as e:
                    print(f"   ⚠️ {domain} → Error: {e}")
            
            print("\n🎯 REDIRECT COMPLETE!")
            print("=" * 80)
            print("🎮 NOW START YOUR CUSTOM SERVER:")
            print("   1. Run: start_full_server.bat")
            print("   2. Start PES 2021")
            print("   3. Try Team Play Lobby")
            print("=" * 80)
            
        except PermissionError:
            print("❌ Permission denied! Run as Administrator!")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        
        return True

def main():
    """Main function"""
    print("🔥 PES 2021 COMPLETE REDIRECT SYSTEM")
    print("Using PES 2019 data patterns for maximum compatibility")
    print()
    
    redirecter = PESCompleteRedirect()
    
    if redirecter.apply_complete_redirect():
        print("\n✅ SUCCESS! Redirect system is active!")
        input("\nPress Enter to continue...")
    else:
        print("\n❌ FAILED! Check permissions and try again.")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()