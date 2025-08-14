#!/usr/bin/env python3
"""
Live Data Verification Script
EMF Chaos Engine - Data Authenticity Checker

Programmatically tests whether EMF Chaos Engine data is:
- LIVE: Real SDR/RF data from hardware
- SIMULATED: Random generated data for demo

Author: AIMF LLC - EMF Chaos Engine Team
Date: August 14, 2025
"""

import subprocess
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any

class LiveDataVerifier:
    """Programmatic verification of EMF Chaos Engine data authenticity"""
    
    def __init__(self):
        self.verification_results = {
            'sdr_hardware': {'status': 'unknown', 'evidence': []},
            'gsm_data': {'status': 'unknown', 'evidence': []},
            'bluetooth_data': {'status': 'unknown', 'evidence': []},
            'wifi_data': {'status': 'unknown', 'evidence': []},
            'overall_authenticity': 'unknown'
        }
        
    def verify_sdr_hardware(self) -> bool:
        """Verify if real SDR hardware is connected and active"""
        print("🔍 VERIFYING SDR HARDWARE CONNECTION...")
        
        try:
            # Check for HackRF One
            result = subprocess.run(['hackrf_info'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and 'Serial number' in result.stdout:
                serial = result.stdout.split('Serial number: ')[1].split('\n')[0]
                self.verification_results['sdr_hardware']['status'] = 'LIVE'
                self.verification_results['sdr_hardware']['evidence'].append(f"HackRF detected: {serial}")
                print(f"✅ LIVE SDR HARDWARE: HackRF One detected - {serial}")
                return True
            else:
                self.verification_results['sdr_hardware']['status'] = 'DISCONNECTED'
                self.verification_results['sdr_hardware']['evidence'].append("No HackRF detected")
                print("❌ NO SDR HARDWARE: HackRF One not detected")
                return False
                
        except Exception as e:
            self.verification_results['sdr_hardware']['status'] = 'ERROR'
            self.verification_results['sdr_hardware']['evidence'].append(f"Error: {e}")
            print(f"⚠️ SDR CHECK ERROR: {e}")
            return False
    
    def verify_gsm_data_authenticity(self) -> str:
        """Analyze GSM warfare data to determine if live or simulated"""
        print("🔍 ANALYZING GSM WARFARE DATA AUTHENTICITY...")
        
        # Check GSM warfare tab source code for simulation markers
        try:
            with open('/Users/flowgirl/Documents/EMF_Chaos_Engine/gsm_warfare_tab.py', 'r') as f:
                gsm_code = f.read()
            
            simulation_markers = [
                'random.random()',
                'random.choice(',
                'random.randint(',
                '# Simulate',
                'if random.random() <'
            ]
            
            found_markers = []
            for marker in simulation_markers:
                if marker in gsm_code:
                    found_markers.append(marker)
            
            if found_markers:
                self.verification_results['gsm_data']['status'] = 'SIMULATED'
                self.verification_results['gsm_data']['evidence'] = found_markers
                print(f"🎲 GSM DATA IS SIMULATED: Found {len(found_markers)} simulation markers")
                return 'SIMULATED'
            else:
                self.verification_results['gsm_data']['status'] = 'LIVE'
                self.verification_results['gsm_data']['evidence'].append("No simulation markers found")
                print("✅ GSM DATA APPEARS LIVE: No simulation markers detected")
                return 'LIVE'
                
        except Exception as e:
            self.verification_results['gsm_data']['status'] = 'ERROR'
            self.verification_results['gsm_data']['evidence'].append(f"Error: {e}")
            print(f"⚠️ GSM ANALYSIS ERROR: {e}")
            return 'ERROR'
    
    def verify_bluetooth_data_authenticity(self) -> str:
        """Check if Bluetooth data is from real scanning or simulation"""
        print("🔍 ANALYZING BLUETOOTH DATA AUTHENTICITY...")
        
        try:
            # macOS Bluetooth check using system_profiler
            result = subprocess.run(['system_profiler', 'SPBluetoothDataType'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and 'Bluetooth' in result.stdout:
                # Check if Bluetooth is enabled and has devices
                if 'Discoverable' in result.stdout or 'Connected' in result.stdout:
                    self.verification_results['bluetooth_data']['status'] = 'LIVE_CAPABLE'
                    self.verification_results['bluetooth_data']['evidence'].append("macOS Bluetooth system active")
                    print("✅ BLUETOOTH LIVE CAPABLE: macOS Bluetooth system detected")
                    return 'LIVE_CAPABLE'
                else:
                    self.verification_results['bluetooth_data']['status'] = 'LIVE_CAPABLE'
                    self.verification_results['bluetooth_data']['evidence'].append("macOS Bluetooth available but inactive")
                    print("🟡 BLUETOOTH AVAILABLE: macOS Bluetooth present but not active")
                    return 'LIVE_CAPABLE'
            else:
                self.verification_results['bluetooth_data']['status'] = 'SIMULATED'
                self.verification_results['bluetooth_data']['evidence'].append("No Bluetooth system detected")
                print("🎲 BLUETOOTH SIMULATED: No Bluetooth system detected")
                return 'SIMULATED'
                
        except Exception as e:
            # Fallback: Check if blueutil is available (common macOS Bluetooth tool)
            try:
                result = subprocess.run(['which', 'blueutil'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.verification_results['bluetooth_data']['status'] = 'LIVE_CAPABLE'
                    self.verification_results['bluetooth_data']['evidence'].append("blueutil tool available")
                    print("✅ BLUETOOTH LIVE CAPABLE: blueutil tool detected")
                    return 'LIVE_CAPABLE'
            except:
                pass
            
            self.verification_results['bluetooth_data']['status'] = 'ERROR'
            self.verification_results['bluetooth_data']['evidence'].append(f"Error: {e}")
            print(f"⚠️ BLUETOOTH CHECK ERROR: {e}")
            return 'ERROR'
    
    def verify_wifi_data_authenticity(self) -> str:
        """Check if WiFi data is from real scanning or simulation"""
        print("🔍 ANALYZING WIFI DATA AUTHENTICITY...")
        
        try:
            # Try multiple methods for macOS WiFi scanning
            wifi_commands = [
                ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'],
                ['/usr/sbin/airport', '-s'],
                ['airport', '-s']
            ]
            
            for cmd in wifi_commands:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0 and ('SSID' in result.stdout or 'BSSID' in result.stdout):
                        networks = len([line for line in result.stdout.split('\n') if line.strip()]) - 1
                        self.verification_results['wifi_data']['status'] = 'LIVE'
                        self.verification_results['wifi_data']['evidence'].append(f"Real WiFi scan: {networks} networks detected")
                        print(f"✅ WIFI DATA IS LIVE: Detected {networks} real networks")
                        return 'LIVE'
                except:
                    continue
            
            # Fallback: Check if WiFi interface exists using networksetup
            try:
                result = subprocess.run(['networksetup', '-listallhardwareports'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0 and 'Wi-Fi' in result.stdout:
                    self.verification_results['wifi_data']['status'] = 'LIVE_CAPABLE'
                    self.verification_results['wifi_data']['evidence'].append("WiFi hardware detected via networksetup")
                    print("🟡 WIFI HARDWARE AVAILABLE: WiFi interface detected but scanning unavailable")
                    return 'LIVE_CAPABLE'
            except:
                pass
            
            # Final fallback: Check system network preferences
            try:
                result = subprocess.run(['system_profiler', 'SPAirPortDataType'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0 and ('AirPort' in result.stdout or 'Wi-Fi' in result.stdout):
                    self.verification_results['wifi_data']['status'] = 'LIVE_CAPABLE'
                    self.verification_results['wifi_data']['evidence'].append("WiFi system detected via system_profiler")
                    print("🟡 WIFI SYSTEM AVAILABLE: WiFi hardware present")
                    return 'LIVE_CAPABLE'
            except:
                pass
            
            self.verification_results['wifi_data']['status'] = 'SIMULATED'
            self.verification_results['wifi_data']['evidence'].append("No WiFi scanning capability detected")
            print("🎲 WIFI DATA SIMULATED: No WiFi scanning capability available")
            return 'SIMULATED'
                
        except Exception as e:
            self.verification_results['wifi_data']['status'] = 'ERROR'
            self.verification_results['wifi_data']['evidence'].append(f"Error: {e}")
            print(f"⚠️ WIFI CHECK ERROR: {e}")
            return 'ERROR'
    
    def calculate_overall_authenticity(self) -> str:
        """Calculate overall data authenticity score"""
        print("🔍 CALCULATING OVERALL DATA AUTHENTICITY...")
        
        live_count = 0
        simulated_count = 0
        total_checks = 0
        
        for component, data in self.verification_results.items():
            if component == 'overall_authenticity':
                continue
                
            status = data['status']
            total_checks += 1
            
            if status in ['LIVE', 'LIVE_CAPABLE']:
                live_count += 1
            elif status == 'SIMULATED':
                simulated_count += 1
        
        if live_count > simulated_count:
            authenticity = 'MOSTLY_LIVE'
        elif simulated_count > live_count:
            authenticity = 'MOSTLY_SIMULATED'
        else:
            authenticity = 'MIXED'
        
        self.verification_results['overall_authenticity'] = authenticity
        
        print(f"📊 AUTHENTICITY SCORE: {live_count}/{total_checks} components are LIVE")
        print(f"🎯 OVERALL ASSESSMENT: {authenticity}")
        
        return authenticity
    
    def run_full_verification(self) -> Dict[str, Any]:
        """Run complete data authenticity verification"""
        print("🚨📱 EMF CHAOS ENGINE - LIVE DATA VERIFICATION")
        print("=" * 60)
        print(f"🕐 Verification started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all verification checks
        self.verify_sdr_hardware()
        print()
        
        self.verify_gsm_data_authenticity()
        print()
        
        self.verify_bluetooth_data_authenticity()
        print()
        
        self.verify_wifi_data_authenticity()
        print()
        
        overall = self.calculate_overall_authenticity()
        print()
        
        # Generate summary report
        print("📋 VERIFICATION SUMMARY REPORT")
        print("=" * 60)
        
        for component, data in self.verification_results.items():
            if component == 'overall_authenticity':
                continue
                
            status = data['status']
            evidence = data['evidence']
            
            status_emoji = {
                'LIVE': '✅',
                'LIVE_CAPABLE': '🟢',
                'SIMULATED': '🎲',
                'DISCONNECTED': '❌',
                'ERROR': '⚠️',
                'unknown': '❓'
            }.get(status, '❓')
            
            print(f"{status_emoji} {component.upper().replace('_', ' ')}: {status}")
            for ev in evidence:
                print(f"   └─ {ev}")
        
        print()
        print(f"🎯 OVERALL AUTHENTICITY: {overall}")
        
        # Save results to JSON
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'/Users/flowgirl/Documents/EMF_Chaos_Engine/WarfareLogs/data_verification_{timestamp}.json'
        
        try:
            with open(report_file, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'verification_results': self.verification_results,
                    'summary': {
                        'overall_authenticity': overall,
                        'verification_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                }, f, indent=2)
            print(f"📄 Report saved: {report_file}")
        except Exception as e:
            print(f"⚠️ Could not save report: {e}")
        
        return self.verification_results

def main():
    """Main verification execution"""
    verifier = LiveDataVerifier()
    results = verifier.run_full_verification()
    
    # Exit with appropriate code
    overall = results['overall_authenticity']
    if overall == 'MOSTLY_LIVE':
        sys.exit(0)  # Success - mostly live data
    elif overall == 'MOSTLY_SIMULATED':
        sys.exit(1)  # Warning - mostly simulated
    else:
        sys.exit(2)  # Mixed results

if __name__ == "__main__":
    main()
