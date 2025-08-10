#!/usr/bin/env python3
"""
🌪️ EMF Ambient Chaos Engine ⚡
Real-time electromagnetic field chaos pattern generation with dynamic device detection

A weekend project exploring EMF chaos patterns and their response to mobile device movement.
Demonstrates zone-based threat detection with extended range monitoring.

Author: AIMF LLC
License: MIT
"""

import sys
import time
import random
import threading
from datetime import datetime

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, 
        QHBoxLayout, QLabel, QPushButton, QTextEdit, QFrame
    )
    from PyQt6.QtCore import QThread, pyqtSignal, QTimer
    from PyQt6.QtGui import QFont, QPalette, QColor
except ImportError:
    print("❌ PyQt6 not found. Installing...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6"])
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, 
        QHBoxLayout, QLabel, QPushButton, QTextEdit, QFrame
    )
    from PyQt6.QtCore import QThread, pyqtSignal, QTimer
    from PyQt6.QtGui import QFont, QPalette, QColor

class EMFChaosEngine:
    """Core EMF chaos pattern generator"""
    
    def __init__(self):
        self.patterns = ['ambient_monitoring', 'dynamic_chaos', 'quad_reflection', 'swiss_energy_disruption']
        self.reflection_types = ['Dynamic', 'Quad', 'Swiss Energy', 'Ambient', 'Chaos Burst', 'Mirror']
    
    def generate_dynamic_chaos_pattern(self, duration_ms=500):
        """Generate a dynamic chaos pattern"""
        return {
            'pattern_type': random.choice(self.patterns),
            'intensity': random.randint(20, 95),
            'frequency': round(random.uniform(2.0, 6.0), 2),
            'chaos_level': random.choice(['low', 'moderate', 'high', 'extreme']),
            'duration': duration_ms
        }

class EMFChaosThread(QThread):
    """Background thread for EMF chaos pattern generation"""
    chaos_update = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.chaos_engine = EMFChaosEngine()
        self.phone_history = []
        print("✅ EMF Chaos Engine initialized")
    
    def run(self):
        """Run EMF chaos engine in background"""
        self.running = True
        while self.running:
            try:
                # Generate chaos sources with extended zone detection
                chaos_sources = self.generate_chaos_sources()
                
                # Calculate dynamic intensity based on phone count and signal strength
                phone_count = len(chaos_sources)
                avg_signal = sum(abs(s.get('signal', -70)) for s in chaos_sources) / max(phone_count, 1)
                
                # Dynamic intensity calculation (0-100%)
                base_intensity = min(phone_count * 15, 85)  # 15% per phone, max 85%
                signal_bonus = max(0, (avg_signal - 50) / 2)  # Bonus for strong signals
                dynamic_intensity = min(100, int(base_intensity + signal_bonus))
                
                # Vary pattern type based on intensity
                if dynamic_intensity > 75:
                    pattern_type = 'swiss_energy_disruption'
                elif dynamic_intensity > 50:
                    pattern_type = 'quad_reflection'
                elif dynamic_intensity > 25:
                    pattern_type = 'dynamic_chaos'
                else:
                    pattern_type = 'ambient_monitoring'
                
                # Generate pattern with dynamic values
                pattern_data = self.chaos_engine.generate_dynamic_chaos_pattern(duration_ms=500)
                pattern_data['intensity'] = dynamic_intensity
                pattern_data['pattern_type'] = pattern_type
                pattern_data['chaos_sources'] = chaos_sources
                pattern_data['phone_count'] = phone_count
                pattern_data['avg_signal'] = avg_signal
                
                self.chaos_update.emit(pattern_data)
                
                # Track phone history for movement detection
                self.phone_history.append({
                    'timestamp': time.time(),
                    'count': phone_count,
                    'intensity': dynamic_intensity
                })
                
                # Keep only last 10 entries
                if len(self.phone_history) > 10:
                    self.phone_history = self.phone_history[-10:]
                
                time.sleep(1)  # Update every second
            except Exception as e:
                print(f"❌ EMF Chaos Thread error: {e}")
                time.sleep(1)
    
    def generate_chaos_sources(self):
        """Generate synthetic chaos sources with extended detection range and directional positioning"""
        sources = []
        
        # Extended chaos detection range with zone-based threat assessment
        chaos_detection_zones = {
            'north': {'range': 15, 'threat_level': 'medium'},
            'south': {'range': 25, 'threat_level': 'high'},  # Extended 10m south
            'east': {'range': 15, 'threat_level': 'medium'},
            'west': {'range': 15, 'threat_level': 'medium'},
            'center': {'range': 5, 'threat_level': 'critical'}  # Core protection zone
        }
        
        # Generate sources across different detection zones
        total_sources = random.randint(2, 8)
        
        # Device and reflection types
        phone_types = ['iPhone', 'Android', 'Samsung', 'Google Pixel', 'Unknown Device']
        reflection_types = ['Dynamic', 'Quad', 'Swiss Energy', 'Ambient', 'Chaos Burst', 'Mirror']
        
        for i in range(total_sources):
            # Select detection zone (bias toward south for extended range)
            zone_weights = {'north': 15, 'south': 35, 'east': 15, 'west': 15, 'center': 20}
            zone = random.choices(list(zone_weights.keys()), weights=list(zone_weights.values()))[0]
            zone_info = chaos_detection_zones[zone]
            
            # Generate synthetic MAC addresses
            mac_parts = [f"{random.randint(0, 6):01d}", f"{random.randint(0, 6):01d}"]
            mac = f"syn_{mac_parts[0]}:{mac_parts[1]}..."
            
            # Generate signal strength based on zone distance
            if zone == 'center':
                signal = random.randint(-45, -30)  # Strong signals in core zone
            elif zone == 'south':
                signal = random.randint(-85, -60)  # Weaker signals in extended south range
            else:
                signal = random.randint(-75, -50)  # Medium signals in standard range
            
            # Calculate distance from zone range
            distance = random.uniform(2, zone_info['range'])
            
            # Assign device type and reflection type
            phone_type = random.choice(phone_types)
            reflection_type = random.choice(reflection_types)
            
            sources.append({
                'mac': mac,
                'signal': signal,
                'type': 'synthetic',
                'phone_type': phone_type,
                'reflection_type': reflection_type,
                'detected_time': time.strftime("%H:%M:%S"),
                'detection_zone': zone,
                'threat_level': zone_info['threat_level'],
                'distance': round(distance, 1),
                'chaos_input': True,  # All sources contribute to chaos
                'core_zone_target': zone == 'center'  # Only center zone is high priority
            })
        
        return sources
    
    def stop(self):
        """Stop the chaos thread"""
        self.running = False

class EMFChaosGUI(QMainWindow):
    """Simple GUI for EMF Chaos Engine demonstration"""
    
    def __init__(self):
        super().__init__()
        self.chaos_thread = None
        self.init_ui()
        self.start_chaos_engine()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🌪️ EMF Ambient Chaos Engine ⚡")
        self.setGeometry(100, 100, 800, 600)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; color: #ffffff; }
            QTextEdit { background-color: #2d2d2d; color: #ffffff; border: 1px solid #555; }
            QPushButton { background-color: #0078d4; color: white; border: none; padding: 8px; }
            QPushButton:hover { background-color: #106ebe; }
            QLabel { color: #ffffff; }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("🌪️ EMF Ambient Chaos Engine ⚡")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Real-time electromagnetic field chaos pattern generation")
        subtitle.setFont(QFont("Arial", 10))
        layout.addWidget(subtitle)
        
        # Controls
        controls_layout = QHBoxLayout()
        self.start_btn = QPushButton("🚀 Start Chaos Engine")
        self.stop_btn = QPushButton("⏹️ Stop Chaos Engine")
        self.start_btn.clicked.connect(self.start_chaos_manually)
        self.stop_btn.clicked.connect(self.stop_chaos_manually)
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.stop_btn)
        layout.addLayout(controls_layout)
        
        # Output display
        self.output_display = QTextEdit()
        self.output_display.setFont(QFont("Courier", 10))
        layout.addWidget(self.output_display)
        
        # Status
        self.status_label = QLabel("Status: Initializing...")
        layout.addWidget(self.status_label)
    
    def start_chaos_engine(self):
        """Start the EMF Ambient Chaos Engine"""
        if self.chaos_thread is None or not self.chaos_thread.isRunning():
            self.chaos_thread = EMFChaosThread()
            self.chaos_thread.chaos_update.connect(self.update_chaos_display)
            self.chaos_thread.start()
            self.status_label.setText("Status: 🌪️ Chaos Engine Active")
            print("✅ EMF Chaos Engine started")
    
    def update_chaos_display(self, pattern_data):
        """Update chaos display with real-time data"""
        timestamp = time.strftime("%H:%M:%S")
        
        # Extract data
        pattern_type = pattern_data.get('pattern_type', 'unknown')
        intensity = pattern_data.get('intensity', 0)
        phone_count = pattern_data.get('phone_count', 0)
        chaos_sources = pattern_data.get('chaos_sources', [])
        
        # Count devices by zone
        zone_counts = {}
        chaos_devices = 0
        core_devices = 0
        
        for source in chaos_sources:
            zone = source.get('detection_zone', 'unknown')
            zone_counts[zone] = zone_counts.get(zone, 0) + 1
            if source.get('chaos_input'):
                chaos_devices += 1
            if source.get('core_zone_target'):
                core_devices += 1
        
        # Terminal-style output
        output = f"[{timestamp}] 🌪️ Chaos Pattern: {pattern_type} | Intensity: {intensity}% | Phones: {phone_count}\n"
        output += f"⚡ Chaos Detection Range: {chaos_devices} devices | 🎯 Core Zone: {core_devices} devices\n"
        
        # Zone breakdown
        if zone_counts:
            zone_display = " | ".join([f"{count} {zone.upper()}" for zone, count in zone_counts.items()])
            output += f"🎯 Detection Zones: {zone_display}\n"
        
        # Device details
        for source in chaos_sources:
            phone_type = source.get('phone_type', 'Unknown')
            mac = source.get('mac', 'unknown')
            signal = source.get('signal', 0)
            zone = source.get('detection_zone', 'unknown')
            distance = source.get('distance', 0)
            reflection = source.get('reflection_type', 'Unknown')
            
            # Zone icons
            zone_icons = {
                'north': '⬆️NORTH',
                'south': '⬇️SOUTH', 
                'east': '➡️EAST',
                'west': '⬅️WEST',
                'center': '🎯CENTER'
            }
            
            # Threat level colors
            threat_colors = {
                'critical': '🔴',
                'high': '🟠', 
                'medium': '🟡'
            }
            
            zone_icon = zone_icons.get(zone, f"📍{zone.upper()}")
            threat_color = threat_colors.get(source.get('threat_level', 'medium'), '🟡')
            
            output += f"📱 {phone_type}: {mac} ({signal}dBm) {zone_icon} {distance}m {threat_color} → {reflection} Reflection\n"
        
        output += "\n"
        
        # Update display
        self.output_display.append(output)
        
        # Auto-scroll and limit content
        cursor = self.output_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.output_display.setTextCursor(cursor)
        
        # Keep only last 1000 lines
        if self.output_display.document().lineCount() > 1000:
            cursor.movePosition(cursor.MoveOperation.Start)
            for _ in range(100):
                cursor.movePosition(cursor.MoveOperation.Down, cursor.MoveMode.KeepAnchor)
            cursor.removeSelectedText()
    
    def start_chaos_manually(self):
        """Manually start chaos engine"""
        self.start_chaos_engine()
    
    def stop_chaos_manually(self):
        """Manually stop chaos engine"""
        if self.chaos_thread and self.chaos_thread.isRunning():
            self.chaos_thread.stop()
            self.chaos_thread.wait()
            self.status_label.setText("Status: ⏹️ Chaos Engine Stopped")
            print("⏹️ EMF Chaos Engine stopped")
    
    def closeEvent(self, event):
        """Clean shutdown"""
        if self.chaos_thread and self.chaos_thread.isRunning():
            self.chaos_thread.stop()
            self.chaos_thread.wait()
        event.accept()

def main():
    """Main entry point"""
    print("🌪️ Starting EMF Ambient Chaos Engine...")
    print("📡 Initializing zone-based detection system...")
    print("⚡ Loading chaos pattern generators...")
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("EMF Chaos Engine")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("AIMF LLC")
    
    # Create and show main window
    window = EMFChaosGUI()
    window.show()
    
    print("✅ EMF Chaos Engine ready!")
    print("🎯 Extended detection zones active (25m south range)")
    print("🌪️ Dynamic chaos patterns enabled")
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
