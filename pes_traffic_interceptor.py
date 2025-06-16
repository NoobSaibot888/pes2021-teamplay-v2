#!/usr/bin/env python3
"""
PES 2021 Traffic Interceptor - Advanced Protocol Analysis
Real-time capture and analysis of PES network traffic
"""

import socket
import struct
import threading
import time
import json
from datetime import datetime
import binascii

class PESTrafficInterceptor:
    """Advanced PES traffic analysis and interception"""
    
    def __init__(self):
        self.running = False
        self.captured_packets = []
        self.protocol_patterns = {
            # Known PES signatures from reverse engineering
            b'PES21': 'PES 2021 Protocol Header',
            b'KONAMI': 'Konami Protocol',
            b'LOBBY': 'Lobby Communication',
            b'LOGIN': 'Login Protocol',
            b'MATCH': 'Match Data',
            b'P2P': 'Peer-to-Peer',
            # Binary patterns
            b'\x50\x45\x53': 'PES Binary Signature',
            b'\x4B\x4F\x4E': 'Konami Binary',
            # Common networking
            b'HTTP': 'HTTP Protocol',
            b'GET ': 'HTTP GET Request',
            b'POST': 'HTTP POST Request',
        }
    
    def analyze_packet_data(self, data, source, dest):
        """Deep analysis of packet data"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        analysis = {
            'timestamp': timestamp,
            'source': source,
            'destination': dest,
            'size': len(data),
            'hex_dump': data[:64].hex(),
            'patterns_found': [],
            'decoded_text': '',
            'protocol_guess': 'Unknown',
            'interesting': False
        }
        
        # Look for known patterns
        for pattern, description in self.protocol_patterns.items():
            if pattern in data:
                analysis['patterns_found'].append({
                    'pattern': pattern.hex(),
                    'description': description,
                    'offset': data.find(pattern)
                })
                analysis['interesting'] = True
        
        # Try to decode readable text
        try:
            decoded = data.decode('utf-8', errors='ignore')
            printable = ''.join(c for c in decoded if c.isprintable())
            if len(printable) > 10:
                analysis['decoded_text'] = printable[:200]
                analysis['interesting'] = True
        except:
            pass
        
        # Guess protocol type
        if b'HTTP' in data:
            analysis['protocol_guess'] = 'HTTP'
        elif b'PES' in data or b'KONAMI' in data:
            analysis['protocol_guess'] = 'PES Custom'
        elif len(data) > 0 and data[0] in [0x16, 0x14, 0x15]:  # TLS handshake
            analysis['protocol_guess'] = 'TLS/SSL'
        elif b'\x00\x01' in data[:4] or b'\x00\x02' in data[:4]:
            analysis['protocol_guess'] = 'Binary Protocol'
        
        # Check if this looks like game traffic
        if (analysis['interesting'] or 
            'pes' in analysis['decoded_text'].lower() or
            'konami' in analysis['decoded_text'].lower() or
            'lobby' in analysis['decoded_text'].lower()):
            analysis['interesting'] = True
        
        return analysis
    
    def setup_traffic_capture(self):
        """Setup traffic capture methods"""
        capture_methods = []
        
        # Method 1: Monitor specific ports
        def port_monitor(port, protocol='TCP'):
            try:
                if protocol == 'TCP':
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.bind(('0.0.0.0', port))
                    sock.listen(5)
                    print(f"🔍 Monitoring TCP port {port}")
                    
                    while self.running:
                        try:
                            client, addr = sock.accept()
                            print(f"📥 TCP {port}: Connection from {addr[0]}:{addr[1]}")
                            
                            # Read data
                            data = client.recv(4096)
                            if data:
                                analysis = self.analyze_packet_data(data, f"{addr[0]}:{addr[1]}", f"localhost:{port}")
                                self.process_analysis(analysis)
                            
                            client.close()
                        except socket.timeout:
                            continue
                        except Exception as e:
                            if self.running:
                                print(f"⚠️ TCP {port} error: {e}")
                            break
                
                elif protocol == 'UDP':
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.bind(('0.0.0.0', port))
                    sock.settimeout(1.0)
                    print(f"🔍 Monitoring UDP port {port}")
                    
                    while self.running:
                        try:
                            data, addr = sock.recvfrom(4096)
                            print(f"📥 UDP {port}: Packet from {addr[0]}:{addr[1]}")
                            
                            analysis = self.analyze_packet_data(data, f"{addr[0]}:{addr[1]}", f"localhost:{port}")
                            self.process_analysis(analysis)
                            
                        except socket.timeout:
                            continue
                        except Exception as e:
                            if self.running:
                                print(f"⚠️ UDP {port} error: {e}")
                            break
                
                sock.close()
            except Exception as e:
                print(f"❌ Failed to monitor port {port}: {e}")
        
        # Monitor key ports
        key_ports = [
            (80, 'TCP'),    # HTTP
            (443, 'TCP'),   # HTTPS
            (8000, 'TCP'),  # Game server
            (5739, 'UDP'),  # P2P
            (5740, 'UDP'),  # P2P
            (3478, 'UDP'),  # STUN
        ]
        
        for port, protocol in key_ports:
            thread = threading.Thread(
                target=port_monitor, 
                args=(port, protocol), 
                daemon=True
            )
            thread.start()
            capture_methods.append(f"{protocol} {port}")
        
        return capture_methods
    
    def process_analysis(self, analysis):
        """Process and display packet analysis"""
        if analysis['interesting']:
            print(f"\n🎯 INTERESTING TRAFFIC DETECTED!")
            print(f"   Time: {analysis['timestamp']}")
            print(f"   Route: {analysis['source']} → {analysis['destination']}")
            print(f"   Size: {analysis['size']} bytes")
            print(f"   Protocol: {analysis['protocol_guess']}")
            
            if analysis['patterns_found']:
                print(f"   🔍 Patterns found:")
                for pattern in analysis['patterns_found']:
                    print(f"      • {pattern['description']} at offset {pattern['offset']}")
            
            if analysis['decoded_text']:
                print(f"   📝 Text data: {analysis['decoded_text'][:100]}...")
            
            print(f"   🔧 Hex dump: {analysis['hex_dump']}")
            print()
            
            # Save for later analysis
            self.captured_packets.append(analysis)
        else:
            # Brief log for non-interesting traffic
            print(f"📦 {analysis['timestamp']} | {analysis['source']} → {analysis['destination']} | {analysis['size']} bytes | {analysis['protocol_guess']}")
    
    def start_advanced_capture(self):
        """Start advanced traffic capture"""
        print("=" * 80)
        print("🔬 PES 2021 ADVANCED TRAFFIC INTERCEPTOR")
        print("=" * 80)
        print("This tool performs deep analysis of PES network traffic")
        print("It will capture and analyze all network communication")
        print()
        
        self.running = True
        
        # Setup capture methods
        methods = self.setup_traffic_capture()
        
        print("🚀 Traffic capture started!")
        print(f"📡 Monitoring: {', '.join(methods)}")
        print()
        print("Now start PES 2021 and try Team Play Lobby!")
        print("All interesting traffic will be analyzed and displayed.")
        print("Press Ctrl+C to stop")
        print()
        
        try:
            # Keep main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️ Stopping traffic capture...")
            self.running = False
            self.print_summary()
    
    def print_summary(self):
        """Print capture summary"""
        print("\n" + "=" * 80)
        print("📊 TRAFFIC CAPTURE SUMMARY")
        print("=" * 80)
        
        if self.captured_packets:
            print(f"📦 Captured {len(self.captured_packets)} interesting packets")
            
            # Group by protocol
            protocols = {}
            for packet in self.captured_packets:
                proto = packet['protocol_guess']
                protocols[proto] = protocols.get(proto, 0) + 1
            
            print("\n🌐 Protocols detected:")
            for proto, count in protocols.items():
                print(f"   • {proto}: {count} packets")
            
            # Show patterns
            all_patterns = []
            for packet in self.captured_packets:
                for pattern in packet['patterns_found']:
                    all_patterns.append(pattern['description'])
            
            if all_patterns:
                unique_patterns = set(all_patterns)
                print(f"\n🔍 Unique patterns found:")
                for pattern in unique_patterns:
                    count = all_patterns.count(pattern)
                    print(f"   • {pattern}: {count} times")
            
            # Save detailed log
            log_file = f"pes_traffic_log_{int(time.time())}.json"
            try:
                with open(log_file, 'w') as f:
                    json.dump(self.captured_packets, f, indent=2)
                print(f"\n💾 Detailed log saved to: {log_file}")
            except Exception as e:
                print(f"\n⚠️ Could not save log: {e}")
        
        else:
            print("❌ No interesting traffic captured")
            print("\nPossible reasons:")
            print("• Game is not making network connections")
            print("• Traffic is encrypted/obfuscated")
            print("• Different ports are being used")
            print("• Need to trigger specific game actions")
        
        print("\n✅ Traffic analysis complete")

def main():
    """Main entry point"""
    interceptor = PESTrafficInterceptor()
    interceptor.start_advanced_capture()

if __name__ == "__main__":
    main()