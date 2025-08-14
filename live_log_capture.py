#!/usr/bin/env python3
"""
Live EMF Chaos Engine Log Capture
Real-time warfare data logging with terminal output monitoring

Captures and saves:
- Live phone detections with positioning
- Chaos patterns and intensities  
- Signal strengths and threat levels
- GSM spectrum analysis data
- Complete warfare session logs

Author: AIMF LLC - EMF Chaos Engine Team
Date: August 13, 2025
"""

import os
import json
import time
import subprocess
import threading
from datetime import datetime
from typing import Dict, List, Any
import re

class LiveLogCapture:
    """Real-time log capture for EMF Chaos Engine warfare data"""
    
    def __init__(self):
        self.log_dir = "/Users/flowgirl/Documents/EMF_Chaos_Engine/WarfareLogs"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.setup_directories()
        
        # Live data storage
        self.live_detections = []
        self.warfare_stats = {
            'session_start': datetime.now().isoformat(),
            'total_phones': 0,
            'max_intensity': 0,
            'chaos_patterns': [],
            'gsm_scans': 0
        }
        
        # Log files
        self.live_log = os.path.join(self.log_dir, f"live_warfare_{self.session_id}.json")
        self.summary_md = os.path.join(self.log_dir, f"session_summary_{self.session_id}.md")
        
        print(f"🚨📱 Live Log Capture Initialized")
        print(f"📁 Logs: {self.log_dir}")
        print(f"🆔 Session: {self.session_id}")
    
    def setup_directories(self):
        """Setup logging directory structure"""
        os.makedirs(self.log_dir, exist_ok=True)
        print(f"✅ Log directory ready: {self.log_dir}")
    
    def capture_emf_output(self, process_id):
        """Capture live output from EMF Chaos Engine process"""
        print(f"🔍 Monitoring EMF Chaos Engine (PID: {process_id})")
        
        try:
            while True:
                # Get process output using ps and grep
                result = subprocess.run([
                    'ps', 'aux', '|', 'grep', 'emf_chaos_engine'
                ], shell=True, capture_output=True, text=True)
                
                if result.stdout:
                    self.parse_live_data(result.stdout)
                
                # Save data every 10 seconds
                self.save_live_data()
                time.sleep(10)
                
        except Exception as e:
            print(f"❌ Capture error: {e}")
    
    def parse_live_data(self, output):
        """Parse live warfare data from output"""
        lines = output.split('\n')
        
        for line in lines:
            # Parse phone detections
            if '📱' in line:
                detection = self.parse_phone_line(line)
                if detection:
                    self.live_detections.append(detection)
            
            # Parse chaos patterns
            if '🌪️ Chaos Pattern:' in line:
                pattern = self.parse_chaos_line(line)
                if pattern:
                    self.warfare_stats['chaos_patterns'].append(pattern)
            
            # Parse GSM scans
            if '🔍 Scanning' in line and 'MHz' in line:
                self.warfare_stats['gsm_scans'] += 1
    
    def parse_phone_line(self, line):
        """Parse individual phone detection line"""
        try:
            # Extract phone data: 📱 iPhone: syn_1:4... (-73dBm) ⬅️WEST 4.7m 🟡 → Mirror Reflection
            phone_pattern = r'📱 (.*?): (.*?) \((.*?)\) (.*?) (.*?)m (.*?) → (.*)'
            match = re.search(phone_pattern, line)
            
            if match:
                return {
                    'timestamp': datetime.now().isoformat(),
                    'device_type': match.group(1),
                    'device_id': match.group(2),
                    'signal_strength': match.group(3),
                    'direction': match.group(4),
                    'distance': match.group(5),
                    'threat_level': match.group(6),
                    'reflection': match.group(7)
                }
        except Exception as e:
            print(f"⚠️ Phone parse error: {e}")
        
        return None
    
    def parse_chaos_line(self, line):
        """Parse chaos pattern line"""
        try:
            # Extract: 🌪️ Chaos Pattern: swiss_energy_disruption | Intensity: 91% | Phones: 8
            chaos_pattern = r'🌪️ Chaos Pattern: (.*?) \| Intensity: (.*?)% \| Phones: (.*)'
            match = re.search(chaos_pattern, line)
            
            if match:
                intensity = int(match.group(2))
                phone_count = int(match.group(3))
                
                # Update stats
                self.warfare_stats['max_intensity'] = max(self.warfare_stats['max_intensity'], intensity)
                self.warfare_stats['total_phones'] = max(self.warfare_stats['total_phones'], phone_count)
                
                return {
                    'timestamp': datetime.now().isoformat(),
                    'pattern': match.group(1),
                    'intensity': intensity,
                    'phones': phone_count
                }
        except Exception as e:
            print(f"⚠️ Chaos parse error: {e}")
        
        return None
    
    def save_live_data(self):
        """Save all live data to files"""
        try:
            # Save live detections JSON
            warfare_data = {
                'session_info': {
                    'session_id': self.session_id,
                    'start_time': self.warfare_stats['session_start'],
                    'last_update': datetime.now().isoformat()
                },
                'statistics': self.warfare_stats,
                'live_detections': self.live_detections[-100:],  # Keep last 100
                'total_detections': len(self.live_detections)
            }
            
            with open(self.live_log, 'w') as f:
                json.dump(warfare_data, f, indent=2)
            
            # Generate markdown summary
            self.generate_live_summary()
            
            print(f"💾 Live data saved - {len(self.live_detections)} detections, {self.warfare_stats['total_phones']} phones")
            
        except Exception as e:
            print(f"❌ Save error: {e}")
    
    def generate_live_summary(self):
        """Generate live markdown summary"""
        try:
            with open(self.summary_md, 'w') as f:
                f.write(f"# 🚨📱 EMF Chaos Engine Live Warfare Session\n\n")
                f.write(f"**AIMF LLC - $10-20M Viral EMF Chaos Engine**\n")
                f.write(f"**Session ID**: `{self.session_id}`\n")
                f.write(f"**Started**: {datetime.fromisoformat(self.warfare_stats['session_start']).strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Last Update**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write(f"## 📊 Live Warfare Statistics\n\n")
                f.write(f"- **📱 Total Phones Detected**: {self.warfare_stats['total_phones']}\n")
                f.write(f"- **🌪️ Peak Chaos Intensity**: {self.warfare_stats['max_intensity']}%\n")
                f.write(f"- **📡 GSM Band Scans**: {self.warfare_stats['gsm_scans']}\n")
                f.write(f"- **🔍 Total Detections**: {len(self.live_detections)}\n")
                f.write(f"- **⚡ Detection Rate**: {len(self.live_detections)/max(1, (datetime.now() - datetime.fromisoformat(self.warfare_stats['session_start'])).seconds/60):.1f}/min\n\n")
                
                if self.warfare_stats['chaos_patterns']:
                    latest_pattern = self.warfare_stats['chaos_patterns'][-1]
                    f.write(f"## 🌪️ Current Chaos Status\n\n")
                    f.write(f"- **Pattern**: {latest_pattern['pattern']}\n")
                    f.write(f"- **Intensity**: {latest_pattern['intensity']}%\n")
                    f.write(f"- **Active Phones**: {latest_pattern['phones']}\n\n")
                
                if self.live_detections:
                    f.write(f"## 📱 Recent Detections (Last 10)\n\n")
                    for detection in self.live_detections[-10:]:
                        timestamp = datetime.fromisoformat(detection['timestamp']).strftime('%H:%M:%S')
                        f.write(f"- **{timestamp}** - {detection['device_type']} at {detection['distance']}m {detection['direction']} ({detection['signal_strength']}) → {detection['reflection']}\n")
                    f.write(f"\n")
                
                f.write(f"## 🛡️ Warfare Configuration\n\n")
                f.write(f"- **HackRF One**: Serial `78d063dc2b6f6967` (HackRF One r10)\n")
                f.write(f"- **Detection Range**: Multi-zone (CENTER/WEST/EAST/SOUTH)\n")
                f.write(f"- **Threat Analysis**: Real-time reflection patterns\n")
                f.write(f"- **Auto-Logging**: Active (saves every 10 seconds)\n\n")
                
                f.write(f"---\n")
                f.write(f"*Live data from EMF Chaos Engine - The viral $10-20M warfare suite*\n")
                f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
            
        except Exception as e:
            print(f"❌ Summary error: {e}")

if __name__ == "__main__":
    logger = LiveLogCapture()
    
    print(f"🚀 Starting live log capture for EMF Chaos Engine...")
    print(f"📁 All warfare data will be saved to: {logger.log_dir}")
    print(f"💾 Auto-saving every 10 seconds...")
    
    try:
        # Monitor EMF Chaos Engine process
        logger.capture_emf_output("emf_chaos_engine")
        
    except KeyboardInterrupt:
        logger.save_live_data()
        print(f"\n✅ Live log capture stopped - Final save completed")
        print(f"📄 Summary: {logger.summary_md}")
        print(f"📊 Data: {logger.live_log}")
