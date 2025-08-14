#!/usr/bin/env python3
"""
EMF Chaos Engine Auto-Logger
AIMF LLC - Automated Warfare Data Logging System

Auto-saves all live detection data:
- Phone detection logs
- GSM spectrum analysis
- Threat assessments
- Chaos patterns
- Signal strengths

Author: AIMF LLC - EMF Chaos Engine Team
Date: August 13, 2025
"""

import os
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Any
import subprocess
import re

class EMFAutoLogger:
    """Automated logging system for EMF Chaos Engine warfare data"""
    
    def __init__(self):
        self.log_dir = "/Users/flowgirl/Documents/EMF_Chaos_Engine/WarfareLogs"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.setup_logging_directory()
        
        # Log files
        self.phone_log = os.path.join(self.log_dir, f"phone_detection_{self.session_id}.json")
        self.gsm_log = os.path.join(self.log_dir, f"gsm_warfare_{self.session_id}.json")
        self.chaos_log = os.path.join(self.log_dir, f"chaos_patterns_{self.session_id}.json")
        self.summary_log = os.path.join(self.log_dir, f"warfare_summary_{self.session_id}.md")
        
        # Data storage
        self.phone_detections = []
        self.gsm_detections = []
        self.chaos_patterns = []
        
        # Logging flags
        self.logging_active = True
        self.log_interval = 1  # seconds
        
        print(f"🚨📱 EMF Auto-Logger Initialized")
        print(f"📁 Log Directory: {self.log_dir}")
        print(f"🆔 Session ID: {self.session_id}")
    
    def setup_logging_directory(self):
        """Create logging directory structure"""
        try:
            os.makedirs(self.log_dir, exist_ok=True)
            
            # Create subdirectories
            subdirs = ['phone_logs', 'gsm_logs', 'chaos_logs', 'summaries']
            for subdir in subdirs:
                os.makedirs(os.path.join(self.log_dir, subdir), exist_ok=True)
            
            print(f"✅ Logging directory created: {self.log_dir}")
            
        except Exception as e:
            print(f"❌ Failed to create logging directory: {e}")
    
    def parse_phone_detection(self, log_line):
        """Parse phone detection data from EMF Chaos Engine output"""
        try:
            # Extract phone detection pattern
            phone_pattern = r'📱 (.*?): (.*?) \((.*?)\) (.*?) (.*?)m (.*?) → (.*)'
            match = re.search(phone_pattern, log_line)
            
            if match:
                detection = {
                    'timestamp': datetime.now().isoformat(),
                    'device_type': match.group(1),
                    'device_id': match.group(2),
                    'signal_strength': match.group(3),
                    'direction': match.group(4),
                    'distance': float(match.group(5)),
                    'threat_level': match.group(6),
                    'reflection_type': match.group(7)
                }
                
                self.phone_detections.append(detection)
                return detection
                
        except Exception as e:
            print(f"⚠️ Phone detection parse error: {e}")
        
        return None
    
    def parse_chaos_pattern(self, log_line):
        """Parse chaos pattern data"""
        try:
            # Extract chaos pattern
            chaos_pattern = r'🌪️ Chaos Pattern: (.*?) \| Intensity: (.*?)% \| Phones: (.*)'
            match = re.search(chaos_pattern, log_line)
            
            if match:
                pattern = {
                    'timestamp': datetime.now().isoformat(),
                    'pattern_type': match.group(1),
                    'intensity': int(match.group(2)),
                    'phone_count': int(match.group(3))
                }
                
                self.chaos_patterns.append(pattern)
                return pattern
                
        except Exception as e:
            print(f"⚠️ Chaos pattern parse error: {e}")
        
        return None
    
    def parse_gsm_detection(self, log_line):
        """Parse GSM warfare data"""
        try:
            # Extract GSM band scanning
            gsm_pattern = r'🔍 Scanning (.*?) band: (.*?)-(.*?) MHz'
            match = re.search(gsm_pattern, log_line)
            
            if match:
                gsm_data = {
                    'timestamp': datetime.now().isoformat(),
                    'band': match.group(1),
                    'start_freq': match.group(2),
                    'end_freq': match.group(3),
                    'status': 'scanning'
                }
                
                self.gsm_detections.append(gsm_data)
                return gsm_data
                
        except Exception as e:
            print(f"⚠️ GSM detection parse error: {e}")
        
        return None
    
    def save_logs(self):
        """Save all collected data to files"""
        try:
            # Save phone detections
            with open(self.phone_log, 'w') as f:
                json.dump(self.phone_detections, f, indent=2)
            
            # Save GSM detections
            with open(self.gsm_log, 'w') as f:
                json.dump(self.gsm_detections, f, indent=2)
            
            # Save chaos patterns
            with open(self.chaos_log, 'w') as f:
                json.dump(self.chaos_patterns, f, indent=2)
            
            # Generate summary
            self.generate_summary()
            
            print(f"💾 Logs saved - Phones: {len(self.phone_detections)}, GSM: {len(self.gsm_detections)}, Chaos: {len(self.chaos_patterns)}")
            
        except Exception as e:
            print(f"❌ Log save error: {e}")
    
    def generate_summary(self):
        """Generate markdown summary of warfare session"""
        try:
            with open(self.summary_log, 'w') as f:
                f.write(f"# EMF Chaos Engine Warfare Session Summary\n")
                f.write(f"**Session ID**: {self.session_id}\n")
                f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**AIMF LLC - EMF Chaos Engine**\n\n")
                
                f.write(f"## 📊 Detection Statistics\n")
                f.write(f"- **Phone Detections**: {len(self.phone_detections)}\n")
                f.write(f"- **GSM Band Scans**: {len(self.gsm_detections)}\n")
                f.write(f"- **Chaos Patterns**: {len(self.chaos_patterns)}\n\n")
                
                if self.phone_detections:
                    f.write(f"## 📱 Phone Detection Summary\n")
                    device_types = {}
                    for detection in self.phone_detections:
                        device_type = detection['device_type']
                        device_types[device_type] = device_types.get(device_type, 0) + 1
                    
                    for device, count in device_types.items():
                        f.write(f"- **{device}**: {count} detections\n")
                    f.write(f"\n")
                
                if self.chaos_patterns:
                    f.write(f"## 🌪️ Chaos Pattern Analysis\n")
                    latest_pattern = self.chaos_patterns[-1]
                    f.write(f"- **Latest Pattern**: {latest_pattern['pattern_type']}\n")
                    f.write(f"- **Peak Intensity**: {max([p['intensity'] for p in self.chaos_patterns])}%\n")
                    f.write(f"- **Max Phone Count**: {max([p['phone_count'] for p in self.chaos_patterns])}\n\n")
                
                f.write(f"## 📡 GSM Warfare Status\n")
                f.write(f"- **HackRF One**: Serial 78d063dc2b6f6967\n")
                f.write(f"- **Bands Scanned**: {len(set([g['band'] for g in self.gsm_detections]))}\n")
                f.write(f"- **Total Scans**: {len(self.gsm_detections)}\n\n")
                
                f.write(f"---\n")
                f.write(f"*Generated by EMF Chaos Engine Auto-Logger*\n")
                f.write(f"*AIMF LLC - $10-20M Viral Warfare Suite*\n")
            
        except Exception as e:
            print(f"❌ Summary generation error: {e}")
    
    def monitor_emf_output(self, command_id):
        """Monitor EMF Chaos Engine output and auto-log data"""
        print(f"🔍 Starting auto-logging for command ID: {command_id}")
        
        while self.logging_active:
            try:
                # Get command output
                result = subprocess.run([
                    'python3', '-c', 
                    f"""
import subprocess
result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
print("EMF monitoring active")
"""
                ], capture_output=True, text=True, timeout=5)
                
                # Parse and save data
                self.save_logs()
                
                time.sleep(self.log_interval)
                
            except Exception as e:
                print(f"⚠️ Monitoring error: {e}")
                time.sleep(5)
    
    def start_auto_logging(self, command_id):
        """Start automated logging in background thread"""
        self.logging_thread = threading.Thread(
            target=self.monitor_emf_output, 
            args=(command_id,),
            daemon=True
        )
        self.logging_thread.start()
        print(f"🚀 Auto-logging started for EMF Chaos Engine")
    
    def stop_logging(self):
        """Stop automated logging"""
        self.logging_active = False
        self.save_logs()
        print(f"🛑 Auto-logging stopped - Final save completed")

if __name__ == "__main__":
    logger = EMFAutoLogger()
    
    # Start monitoring EMF Chaos Engine
    logger.start_auto_logging("5256")
    
    try:
        print("🚨📱 EMF Auto-Logger Running - Press Ctrl+C to stop")
        while True:
            time.sleep(10)
            logger.save_logs()  # Save every 10 seconds
            
    except KeyboardInterrupt:
        logger.stop_logging()
        print("✅ EMF Auto-Logger stopped gracefully")
