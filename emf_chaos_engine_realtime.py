#!/usr/bin/env python3
"""
🌪️ EMF Ambient Chaos Engine - Real-Time HackRF Detection ⚡
Real phone detection using HackRF One with configurable timing

Author: AIMF LLC
License: MIT
"""

import sys
import time
import subprocess
import re
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QTextEdit
)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QFont

class RealTimePhoneDetector(QThread):
    """Real-time phone detection using HackRF One"""
    detection_update = pyqtSignal(dict)
    
    def __init__(self, detection_delay=2, scan_interval=7):
        super().__init__()
        self.running = False
        self.detection_delay = detection_delay  # 2 seconds delay before output
        self.scan_interval = scan_interval  # 7 seconds between scans
        self.hackrf_available = self.check_hackrf()
        print(f"✅ Real-time detector initialized (delay: {detection_delay}s, interval: {scan_interval}s)")
    
    def check_hackrf(self):
        """Check if HackRF One is available"""
        try:
            result = subprocess.run(['hackrf_info'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and 'Found HackRF' in result.stdout:
                print("✅ HackRF One detected and ready")
                return True
            else:
                print("⚠️ HackRF One not detected - will use simulation")
                return False
        except Exception as e:
            print(f"⚠️ HackRF check failed: {e}")
            return False
    
    def run(self):
        """Run real-time detection loop"""
        self.running = True
        scan_count = 0
        
        while self.running:
            try:
                scan_count += 1
                print(f"\n🔍 Starting scan #{scan_count}...")
                
                # STEP 1: Detect phones (input detection)
                detection_start = time.time()
                phones = self.detect_phones_realtime()
                detection_time = time.time() - detection_start
                
                print(f"⏱️  Detection completed in {detection_time:.2f}s")
                print(f"📱 Found {len(phones)} device(s)")
                
                # STEP 2: Wait 2 seconds before output
                print(f"⏳ Waiting {self.detection_delay}s before output...")
                time.sleep(self.detection_delay)
                
                # STEP 3: Output results
                output_data = {
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'scan_number': scan_count,
                    'phones': phones,
                    'phone_count': len(phones),
                    'detection_time': detection_time,
                    'hackrf_active': self.hackrf_available
                }
                
                self.detection_update.emit(output_data)
                print(f"✅ Output sent at {output_data['timestamp']}")
                
                # STEP 4: Wait 7 seconds before next scan
                print(f"⏳ Waiting {self.scan_interval}s until next scan...")
                time.sleep(self.scan_interval)
                
            except Exception as e:
                print(f"❌ Detection error: {e}")
                time.sleep(5)
    
    def detect_phones_realtime(self):
        """Detect phones using HackRF One"""
        phones = []
        
        if self.hackrf_available:
            # Real HackRF detection - scan 2.4GHz WiFi band
            phones = self.scan_wifi_band()
        else:
            # Fallback simulation
            phones = self.simulate_detection()
        
        return phones
    
    def scan_wifi_band(self):
        """Scan 2.4GHz WiFi band for phone signals using HackRF"""
        phones = []
        
        try:
            # Scan 2.4GHz WiFi band (2400-2500 MHz)
            cmd = [
                'sudo', 'hackrf_sweep',
                '-f', '2400:2500',  # 2.4GHz WiFi band
                '-w', '1000000',    # 1MHz bin width
                '-l', '32',         # LNA gain
                '-g', '40',         # VGA gain  
                '-n', '10'          # 10 sweeps (~5 seconds)
            ]
            
            print("📡 Scanning 2.4GHz WiFi band with HackRF...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Parse spectrum data
                phones = self.parse_wifi_signals(result.stdout)
                print(f"✅ HackRF scan complete - found {len(phones)} signals")
            else:
                print(f"⚠️ HackRF scan failed: {result.stderr}")
                phones = self.simulate_detection()
                
        except subprocess.TimeoutExpired:
            print("⚠️ HackRF scan timeout")
            phones = self.simulate_detection()
        except Exception as e:
            print(f"❌ HackRF scan error: {e}")
            phones = self.simulate_detection()
        
        return phones
    
    def parse_wifi_signals(self, spectrum_data):
        """Parse HackRF spectrum data for WiFi signals"""
        phones = []
        
        try:
            lines = spectrum_data.strip().split('\n')
            signal_count = 0
            
            for line in lines:
                if line.startswith('#') or not line.strip():
                    continue
                
                parts = line.split(',')
                if len(parts) > 6:
                    # Parse power data
                    power_data = [float(x) for x in parts[6:] if x.strip() and x != 'inf']
                    
                    # Look for strong signals (likely phones/devices)
                    for i, power in enumerate(power_data):
                        if power > -50:  # Strong signal threshold
                            freq = 2400 + (i * 1)  # Approximate frequency
                            signal_count += 1
                            
                            # Determine device type based on frequency
                            if 2412 <= freq <= 2462:  # WiFi channels 1-11
                                device_type = self.identify_device_type(freq, power)
                                phones.append({
                                    'type': device_type,
                                    'frequency': f"{freq} MHz",
                                    'signal': f"{power:.1f} dBm",
                                    'channel': self.freq_to_channel(freq),
                                    'distance': self.estimate_distance(power),
                                    'source': 'HackRF'
                                })
            
            # Deduplicate similar signals
            phones = self.deduplicate_signals(phones)
            
        except Exception as e:
            print(f"❌ Parse error: {e}")
        
        return phones
    
    def identify_device_type(self, freq, power):
        """Identify likely device type"""
        if power > -40:
            return "Phone (Very Close)"
        elif power > -50:
            return "Phone/Tablet"
        else:
            return "WiFi Device"
    
    def freq_to_channel(self, freq):
        """Convert frequency to WiFi channel"""
        if freq < 2412:
            return "?"
        return int((freq - 2407) / 5)
    
    def estimate_distance(self, power):
        """Estimate distance based on signal power"""
        if power > -40:
            return "< 2m"
        elif power > -50:
            return "2-5m"
        elif power > -60:
            return "5-10m"
        else:
            return "> 10m"
    
    def deduplicate_signals(self, phones):
        """Remove duplicate/similar signals"""
        if len(phones) <= 1:
            return phones
        
        # Group by channel and keep strongest
        by_channel = {}
        for phone in phones:
            channel = phone['channel']
            if channel not in by_channel or float(phone['signal'].split()[0]) > float(by_channel[channel]['signal'].split()[0]):
                by_channel[channel] = phone
        
        return list(by_channel.values())
    
    def simulate_detection(self):
        """Fallback simulation when HackRF not available"""
        import random
        num_devices = random.randint(1, 4)
        phones = []
        
        for i in range(num_devices):
            phones.append({
                'type': random.choice(['iPhone', 'Android Phone', 'Samsung', 'Google Pixel']),
                'frequency': f"{random.randint(2412, 2462)} MHz",
                'signal': f"{random.randint(-70, -40)} dBm",
                'channel': random.randint(1, 11),
                'distance': random.choice(['< 2m', '2-5m', '5-10m']),
                'source': 'Simulated'
            })
        
        return phones
    
    def stop(self):
        """Stop detection"""
        self.running = False

class RealTimeGUI(QMainWindow):
    """GUI for real-time phone detection"""
    
    def __init__(self):
        super().__init__()
        self.detector = None
        self.init_ui()
        self.start_detection()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("🌪️ EMF Chaos Engine - Real-Time Detection")
        self.setGeometry(100, 100, 900, 700)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; color: #ffffff; }
            QTextEdit { background-color: #2d2d2d; color: #ffffff; border: 1px solid #555; 
                       font-family: 'Courier New'; font-size: 11pt; }
            QPushButton { background-color: #0078d4; color: white; border: none; 
                         padding: 10px; font-size: 12pt; }
            QPushButton:hover { background-color: #106ebe; }
            QLabel { color: #ffffff; font-size: 11pt; }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("🌪️ EMF Chaos Engine - Real-Time Phone Detection")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Status
        self.status_label = QLabel("Status: Initializing...")
        self.status_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.status_label)
        
        # Info
        info = QLabel("⏱️  Detection Timing: 2s delay | 7s scan interval")
        info.setFont(QFont("Arial", 10))
        layout.addWidget(info)
        
        # Controls
        controls = QHBoxLayout()
        self.start_btn = QPushButton("🚀 Start Detection")
        self.stop_btn = QPushButton("⏹️ Stop Detection")
        self.start_btn.clicked.connect(self.start_detection)
        self.stop_btn.clicked.connect(self.stop_detection)
        controls.addWidget(self.start_btn)
        controls.addWidget(self.stop_btn)
        layout.addLayout(controls)
        
        # Output with label
        output_label = QLabel("📋 Detection Log (All scans preserved)")
        output_label.setFont(QFont("Arial", 10))
        layout.addWidget(output_label)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)
    
    def start_detection(self):
        """Start real-time detection"""
        if self.detector is None or not self.detector.isRunning():
            self.detector = RealTimePhoneDetector(detection_delay=2, scan_interval=7)
            self.detector.detection_update.connect(self.update_display)
            self.detector.start()
            self.status_label.setText("Status: 🟢 Active Detection")
            self.output.append("✅ Real-time detection started\n")
    
    def update_display(self, data):
        """Update display with detection results"""
        timestamp = data['timestamp']
        scan_num = data['scan_number']
        phones = data['phones']
        count = data['phone_count']
        det_time = data['detection_time']
        hackrf = data['hackrf_active']
        
        source_icon = "📡" if hackrf else "🔮"
        source_text = "HackRF One" if hackrf else "Simulation"
        
        output = f"\n{'='*80}\n"
        output += f"[{timestamp}] SCAN #{scan_num} | {source_icon} {source_text}\n"
        output += f"{'='*80}\n"
        output += f"📱 Devices Detected: {count}\n"
        output += f"⏱️  Detection Time: {det_time:.2f}s\n\n"
        
        if phones:
            for i, phone in enumerate(phones, 1):
                output += f"  {i}. {phone['type']}\n"
                output += f"     📶 Signal: {phone['signal']} | 📡 Freq: {phone['frequency']}\n"
                output += f"     📍 Channel: {phone['channel']} | 📏 Distance: ~{phone['distance']}\n"
                output += f"     🔧 Source: {phone['source']}\n\n"
        else:
            output += "  No devices detected in this scan\n\n"
        
        self.output.append(output)
        
        # Auto-scroll
        cursor = self.output.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.output.setTextCursor(cursor)
    
    def stop_detection(self):
        """Stop detection"""
        if self.detector and self.detector.isRunning():
            self.detector.stop()
            self.detector.wait()
            self.status_label.setText("Status: ⏹️ Stopped")
            self.output.append("\n⏹️ Detection stopped\n")
    
    def closeEvent(self, event):
        """Clean shutdown"""
        if self.detector and self.detector.isRunning():
            self.detector.stop()
            self.detector.wait()
        event.accept()

def main():
    """Main entry point"""
    print("🌪️ Starting EMF Chaos Engine - Real-Time Detection...")
    print("📡 Checking for HackRF One...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("EMF Chaos Engine - Real-Time")
    
    window = RealTimeGUI()
    window.show()
    
    print("✅ Real-time detection GUI ready!")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
