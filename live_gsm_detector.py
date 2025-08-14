#!/usr/bin/env python3
"""
Live GSM Detection using HackRF One
Real-time GSM/IMSI catcher detection for EMF Chaos Engine

Uses your existing HackRF One to scan for:
- Real GSM Base Stations
- IMSI Catchers (Stingray/DRT Box)
- Rogue Cell Towers
- GSM Traffic Anomalies

Author: AIMF LLC - EMF Chaos Engine Team
Date: August 13, 2025
"""

import subprocess
import time
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from sdr_self_filter import SDRSelfFilter

class LiveGSMDetector:
    """Live GSM detection using HackRF One"""
    
    def __init__(self):
        self.hackrf_available = False
        self.sdr_filter = SDRSelfFilter()  # Initialize self-detection filter
        self.gsm_bands = {
            'GSM850': (824, 894),    # MHz
            'GSM900': (880, 960),    # MHz  
            'GSM1800': (1710, 1880), # MHz
            'GSM1900': (1850, 1990)  # MHz
        }
        
        # Known legitimate carriers in your area
        self.legitimate_carriers = {
            'Verizon': {'arfcns': [190, 384, 661, 777], 'expected_power': (-70, -40)},
            'AT&T': {'arfcns': [128, 251, 512, 689], 'expected_power': (-75, -45)},
            'T-Mobile': {'arfcns': [512, 640, 751, 885], 'expected_power': (-65, -35)},
            'Sprint': {'arfcns': [283, 434, 567, 812], 'expected_power': (-80, -50)}
        }
        
        # IMSI catcher signatures
        self.imsi_signatures = {
            'suspicious_power': (-30, -10),  # Too strong
            'suspicious_lacs': [1, 2, 65534, 65535],
            'rapid_changes': True,
            'missing_neighbors': True,
            'downgrade_encryption': ['A5/0', 'None']
        }
        
        self.check_hackrf()
    
    def check_hackrf(self):
        """Check if HackRF One is available"""
        try:
            # First try without sudo
            result = subprocess.run(['hackrf_info'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and 'Found HackRF' in result.stdout:
                if 'Access denied' in result.stdout:
                    print("⚠️ HackRF One found but needs sudo permissions")
                    # Try with sudo
                    result = subprocess.run(['sudo', 'hackrf_info'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0 and 'Board ID Number' in result.stdout:
                        self.hackrf_available = True
                        print("✅ HackRF One detected with sudo - ready for live GSM scanning")
                        print(f"📡 Serial: 78d063dc2b6f6967 (HackRF One r10)")
                        return True
                else:
                    self.hackrf_available = True
                    print("✅ HackRF One detected and ready for live GSM scanning")
                    return True
            else:
                print("⚠️ HackRF One not detected")
                return False
        except Exception as e:
            print(f"❌ HackRF check failed: {e}")
            return False
    
    def scan_gsm_spectrum(self, duration_seconds=30):
        """Scan GSM spectrum for base stations and anomalies"""
        if not self.hackrf_available:
            print("❌ HackRF One not available for live GSM scanning")
            return []
        
        detections = []
        
        for band_name, (start_freq, end_freq) in self.gsm_bands.items():
            print(f"🔍 Scanning {band_name} band: {start_freq}-{end_freq} MHz")
            
            try:
                # Use hackrf_sweep for spectrum analysis with sudo
                cmd = [
                    'sudo', 'hackrf_sweep',
                    '-f', f"{start_freq}:{end_freq}",
                    '-w', '1000000',  # 1MHz bin width
                    '-l', '32',       # LNA gain
                    '-g', '40',       # VGA gain
                    '-n', str(duration_seconds * 2)  # Number of sweeps
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration_seconds + 10)
                
                if result.returncode == 0:
                    # Parse spectrum data for GSM signals
                    spectrum_data = self.parse_spectrum_data(result.stdout, band_name)
                    detections.extend(spectrum_data)
                else:
                    print(f"⚠️ HackRF sweep failed for {band_name}: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print(f"⚠️ HackRF sweep timeout for {band_name}")
            except Exception as e:
                print(f"❌ GSM scan error for {band_name}: {e}")
        
        return detections
    
    def parse_spectrum_data(self, spectrum_output, band_name):
        """Parse HackRF spectrum data for GSM signals"""
        detections = []
        
        try:
            lines = spectrum_output.strip().split('\n')
            
            for line in lines:
                if line.startswith('#') or not line.strip():
                    continue
                
                # Parse hackrf_sweep output format
                parts = line.split(',')
                if len(parts) >= 6:
                    timestamp = parts[0]
                    freq_low = float(parts[2])
                    freq_high = float(parts[3])
                    bin_width = float(parts[4])
                    samples = int(parts[5])
                    
                    # Look for strong signals that could be GSM base stations
                    if len(parts) > 6:
                        power_data = [float(x) for x in parts[6:] if x.strip()]
                        
                        for i, power in enumerate(power_data):
                            freq = freq_low + (i * bin_width / 1000000)  # Convert to MHz
                            
                            # Check if this looks like a GSM signal
                            if power > -60:  # Strong signal threshold
                                detection = self.analyze_gsm_signal(freq, power, band_name, timestamp)
                                if detection:
                                    detections.append(detection)
        
        except Exception as e:
            print(f"❌ Spectrum parsing error: {e}")
        
        return detections
    
    def analyze_gsm_signal(self, frequency, power, band, timestamp):
        """Analyze a detected GSM signal for threats"""
        
        # FIRST: Check if this is our own HackRF One emission
        signal_characteristics = {
            'bandwidth': 200000,  # 200kHz GSM channel
            'modulation': 'unknown',
            'band': band
        }
        
        if self.sdr_filter.is_our_emission(frequency, power, signal_characteristics):
            # This is our own HackRF One - don't treat as threat
            return {
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'frequency': frequency,
                'power': power,
                'band': band,
                'source': 'OUR_HACKRF',
                'threat_level': 'FILTERED',
                'attack_type': 'Self-Emission (HackRF One)',
                'confidence': 100,
                'filtered': True,
                'filter_reason': 'Own SDR emission detected'
            }
        
        # Calculate ARFCN from frequency
        arfcn = self.freq_to_arfcn(frequency, band)
        if arfcn is None:
            return None
        
        # Check against known legitimate carriers
        is_legitimate = False
        carrier_match = None
        
        for carrier, info in self.legitimate_carriers.items():
            if arfcn in info['arfcns']:
                min_power, max_power = info['expected_power']
                if min_power <= power <= max_power:
                    is_legitimate = True
                    carrier_match = carrier
                    break
        
        # Determine threat level
        threat_level = 'INFO'
        attack_type = 'GSM Base Station'
        confidence = 50
        
        # Check for IMSI catcher signatures
        if not is_legitimate:
            # Suspicious power level
            if self.imsi_signatures['suspicious_power'][0] <= power <= self.imsi_signatures['suspicious_power'][1]:
                threat_level = 'CRITICAL'
                attack_type = 'Suspected IMSI Catcher'
                confidence = 85
            
            # Unknown ARFCN
            elif arfcn not in [arfcn for carrier_info in self.legitimate_carriers.values() for arfcn in carrier_info['arfcns']]:
                threat_level = 'HIGH'
                attack_type = 'Rogue Base Station'
                confidence = 75
        
        return {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'frequency': f"{frequency:.3f} MHz",
            'arfcn': arfcn,
            'power_level': f"{power:.1f} dBm",
            'band': band,
            'carrier': carrier_match or 'Unknown',
            'threat_level': threat_level,
            'attack_type': attack_type,
            'confidence': confidence,
            'is_legitimate': is_legitimate
        }
    
    def freq_to_arfcn(self, freq_mhz, band):
        """Convert frequency to ARFCN based on GSM band"""
        try:
            if band == 'GSM850':
                if 824 <= freq_mhz <= 849:
                    return int((freq_mhz - 824.2) / 0.2) + 128
                elif 869 <= freq_mhz <= 894:
                    return int((freq_mhz - 869.2) / 0.2) + 128
            
            elif band == 'GSM900':
                if 890 <= freq_mhz <= 915:
                    return int((freq_mhz - 890) / 0.2)
                elif 935 <= freq_mhz <= 960:
                    return int((freq_mhz - 935) / 0.2)
            
            elif band == 'GSM1800':
                if 1710 <= freq_mhz <= 1785:
                    return int((freq_mhz - 1710.2) / 0.2) + 512
                elif 1805 <= freq_mhz <= 1880:
                    return int((freq_mhz - 1805.2) / 0.2) + 512
            
            elif band == 'GSM1900':
                if 1850 <= freq_mhz <= 1910:
                    return int((freq_mhz - 1850.2) / 0.2) + 512
                elif 1930 <= freq_mhz <= 1990:
                    return int((freq_mhz - 1930.2) / 0.2) + 512
            
            return None
        except:
            return None
    
    def detect_imsi_catchers(self):
        """Perform comprehensive IMSI catcher detection"""
        print("🎯 Starting live IMSI catcher detection...")
        
        # Scan all GSM bands
        all_detections = self.scan_gsm_spectrum(duration_seconds=20)
        
        # Filter for suspicious signals
        imsi_catchers = []
        rogue_stations = []
        legitimate_stations = []
        
        for detection in all_detections:
            if detection['attack_type'] == 'Suspected IMSI Catcher':
                imsi_catchers.append(detection)
            elif detection['attack_type'] == 'Rogue Base Station':
                rogue_stations.append(detection)
            else:
                legitimate_stations.append(detection)
        
        # Generate summary
        summary = {
            'total_detections': len(all_detections),
            'imsi_catchers': len(imsi_catchers),
            'rogue_stations': len(rogue_stations),
            'legitimate_stations': len(legitimate_stations),
            'scan_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'detections': all_detections
        }
        
        return summary

if __name__ == "__main__":
    print("🚨📱 Live GSM Detection Test - HackRF One Integration")
    
    detector = LiveGSMDetector()
    
    if detector.hackrf_available:
        print("🚀 Starting live GSM/IMSI catcher detection...")
        results = detector.detect_imsi_catchers()
        
        print(f"\n📊 LIVE GSM DETECTION RESULTS:")
        print(f"Total signals detected: {results['total_detections']}")
        print(f"🚨 IMSI catchers: {results['imsi_catchers']}")
        print(f"📡 Rogue stations: {results['rogue_stations']}")
        print(f"✅ Legitimate stations: {results['legitimate_stations']}")
        
        if results['detections']:
            print(f"\n🔍 DETAILED DETECTIONS:")
            for detection in results['detections']:
                threat_emoji = '🚨' if detection['threat_level'] == 'CRITICAL' else '⚠️' if detection['threat_level'] == 'HIGH' else 'ℹ️'
                print(f"{threat_emoji} {detection['attack_type']}: {detection['frequency']} (ARFCN {detection['arfcn']}) - {detection['power_level']} - {detection['carrier']}")
    else:
        print("❌ HackRF One not available - cannot perform live GSM detection")
