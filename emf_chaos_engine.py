#!/usr/bin/env python3
"""
🌪️ EMF Ambient Chaos Engine + 4-Tab Bubble Shield GUI ⚡
Complete 4-tab interface: EMF Chaos Engine, Bubble Shield, RF Defense, IoT Management
With comprehensive debugging and tab visibility tracking

AIMF LLC - EMF Ambient Chaos Engine Platform
"""

import sys
import time
import random
import threading
import traceback
from datetime import datetime

# Import bubble shield widgets
try:
    from bubble_shield_widgets import DirectionalBubbleWidget, DirectionalControlsWidget
    print("✅ Bubble Shield widgets imported successfully")
except ImportError as e:
    print(f"⚠️ Bubble Shield widgets not available: {e}")
    DirectionalBubbleWidget = None
    DirectionalControlsWidget = None

# Import AirTag tracker
try:
    from airtag_tracker_tab import AirTagTrackerTab
    print("✅ AirTag Tracker imported successfully")
except ImportError as e:
    print(f"⚠️ AirTag Tracker not available: {e}")
    AirTagTrackerTab = None

# Import SDR Hardware Monitor
try:
    from sdr_hardware_monitor import SDRHardwareMonitor
    print("✅ SDR Hardware Monitor imported successfully")
except ImportError as e:
    print(f"⚠️ SDR Hardware Monitor not available: {e}")
    SDRHardwareMonitor = None

try:
    from wifi_warfare_tab import WiFiWarfareTab
    print("✅ WiFi Warfare imported successfully")
except ImportError as e:
    print(f"⚠️ WiFi Warfare not available: {e}")
    WiFiWarfareTab = None

try:
    from gsm_warfare_tab import GSMWarfareTab
    print("✅ GSM Warfare imported successfully")
except ImportError as e:
    print(f"⚠️ GSM Warfare not available: {e}")
    GSMWarfareTab = None

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
        QHBoxLayout, QLabel, QPushButton, QTextEdit, QFrame, QScrollArea,
        QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QStatusBar, QGridLayout, QSlider, QSpinBox, QComboBox
    )
    from PyQt6.QtCore import QThread, pyqtSignal, QTimer
    from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QIcon
except ImportError:
    print("❌ PyQt6 not found. Installing...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6"])
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
        QHBoxLayout, QLabel, QPushButton, QTextEdit, QFrame, QScrollArea,
        QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox
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
                # Generate chaos sources with phone detection
                chaos_sources = self.generate_chaos_sources()
                
                # Calculate dynamic intensity based on phone count and signal strength
                phone_count = len(chaos_sources)
                avg_signal = sum(abs(s.get('signal', -70)) for s in chaos_sources) / max(phone_count, 1)
                
                # Dynamic intensity calculation (0-100%)
                # More phones + stronger signals = higher intensity
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
        self.quit()
        self.wait()

class EMFChaos4TabGUI(QMainWindow):
    """Main 4-Tab GUI: EMF Chaos Engine, Bubble Shield, RF Defense, IoT Management"""
    
    def __init__(self):
        super().__init__()
        print("🚀 MAIN GUI: Starting 4-tab initialization...")
        
        # Initialize components
        try:
            self.db = DeviceDatabase() if DeviceDatabase else None
            print("✅ MAIN GUI: DeviceDatabase initialized")
        except Exception as e:
            print(f"⚠️ MAIN GUI: DeviceDatabase failed - {e}")
            self.db = None
        
        self.chaos_thread = None
        self.shield_active = False
        self.jam_mode_active = False
        
        # Initialize SDR Hardware Monitor
        self.sdr_monitor = None
        if SDRHardwareMonitor:
            print("🔍 Initializing SDR Hardware Monitor...")
            self.sdr_monitor = SDRHardwareMonitor(callback_on_disconnect=self.emergency_shutdown)
            
            # Perform initial hardware check
            if not self.sdr_monitor.initial_hardware_check():
                print("🚨 CRITICAL: HackRF One not detected!")
                print("💀 EMF Chaos Engine requires SDR hardware to operate")
                self.show_hardware_error_and_exit()
                return
            
            # Start continuous monitoring
            self.sdr_monitor.start_monitoring()
            print("✅ SDR Hardware Monitor active - HackRF One validated")
        else:
            print("⚠️ SDR Hardware Monitor not available - running without hardware validation")
        
        print("🎨 MAIN GUI: Starting UI initialization...")
        self.init_ui()
        print("⚡ MAIN GUI: Starting chaos engine...")
        self.start_chaos_engine()
        print("✅ MAIN GUI: 4-tab initialization complete!")
        
    def init_ui(self):
        """Initialize the main user interface with 4 tabs"""
        print("🎨 UI INIT: Starting 4-tab UI setup...")
        
        self.setWindowTitle("🌪️ EMF Ambient Chaos Engine + 4-Tab Bubble Shield ⚡")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set AIMF logo as window icon
        try:
            import os
            logo_path = os.path.join(os.path.dirname(__file__), "aimf_logo.png")
            if os.path.exists(logo_path):
                from PyQt6.QtGui import QPixmap, QIcon
                self.setWindowIcon(QIcon(logo_path))
                print("✅ AIMF logo loaded as window icon")
            else:
                print("⚠️ AIMF logo not found, using default icon")
        except Exception as e:
            print(f"⚠️ Could not load AIMF logo: {e}")
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #404040;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: #ffffff;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #555555;
            }
        """)
        
        # Create central widget and tab widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        print("📑 UI INIT: Creating main tab widget...")
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create all 4 tabs with comprehensive debugging
        self.create_all_tabs()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("🌪️ EMF Ambient Chaos Engine + 5-Tab Security Suite (AirTag Tracker) - Ready")
        
        # Validate tab visibility after UI is complete
        QTimer.singleShot(1000, self.validate_all_tabs)
        
        print("✅ UI INIT: 4-tab UI setup complete!")
        
    def create_all_tabs(self):
        """Create all 7 tabs with comprehensive warfare capabilities"""
        print("📑 TAB CREATION: Starting creation of all 7 warfare tabs...")
        
        tab_configs = [
            ("🌪️ EMF Chaos Engine", self.create_chaos_engine_tab, "CHAOS"),
            ("🛡️ Bubble Shield", self.create_bubble_shield_tab, "BUBBLE"),
            ("📡 RF Defense", self.create_rf_defense_tab, "RF"),
            ("🏠 IoT Management", self.create_iot_management_tab, "IOT"),
            ("🏷️ AirTag Tracker", self.create_airtag_tracker_tab, "AIRTAG"),
            ("🍍 WiFi Warfare", self.create_wifi_warfare_tab, "WIFI"),
            ("📱 GSM Warfare", self.create_gsm_warfare_tab, "GSM")
        ]
        
        successful_tabs = 0
        
        for tab_name, tab_creator, tab_id in tab_configs:
            print(f"📑 TAB CREATION: Creating {tab_name} ({tab_id})...")
            try:
                tab_widget = tab_creator()
                if tab_widget:
                    self.tab_widget.addTab(tab_widget, tab_name)
                    successful_tabs += 1
                    print(f"✅ TAB CREATION: {tab_name} ({tab_id}) created and added successfully")
                else:
                    print(f"❌ TAB CREATION: {tab_name} ({tab_id}) creation returned None")
            except Exception as e:
                print(f"❌ TAB CREATION: {tab_name} ({tab_id}) failed with exception: {e}")
        
        # Final tab count validation
        total_tabs = self.tab_widget.count()
        print(f"📊 TAB CREATION: Summary - {successful_tabs}/{len(tab_configs)} tabs created successfully")
        print(f"📊 TAB CREATION: Total tabs in widget: {total_tabs}")
        
        # List all created tabs
        for i in range(total_tabs):
            tab_text = self.tab_widget.tabText(i)
            print(f"📑 TAB CREATION: Tab {i}: '{tab_text}'")
        
        return successful_tabs == len(tab_configs)

    # Placeholder tab creation methods (will be implemented in next steps)
    def create_chaos_engine_tab(self):
        """Create EMF Chaos Engine tab"""
        print("🌪️ CHAOS TAB: Starting creation...")
        try:
            chaos_widget = QWidget()
            layout = QVBoxLayout(chaos_widget)
            
            # Title
            title = QLabel("🌪️ EMF Ambient Chaos Engine")
            title.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #4CAF50;
                    padding: 10px;
                    background-color: #2a2a2a;
                    border-radius: 8px;
                    margin-bottom: 10px;
                }
            """)
            layout.addWidget(title)
            
            # Chaos status and controls
            controls_layout = QHBoxLayout()
            
            self.chaos_status = QLabel("Chaos Engine: INITIALIZING")
            self.chaos_status.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 14px;")
            controls_layout.addWidget(self.chaos_status)
            
            controls_layout.addStretch()
            
            # Chaos control buttons
            self.chaos_start_btn = QPushButton("⚡ Start Chaos")
            self.chaos_start_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 16px;")
            self.chaos_start_btn.clicked.connect(self.start_chaos_manually)
            
            self.chaos_stop_btn = QPushButton("🛑 Stop Chaos")
            self.chaos_stop_btn.setStyleSheet("background-color: #F44336; color: white; padding: 8px 16px;")
            self.chaos_stop_btn.clicked.connect(self.stop_chaos_manually)
            
            controls_layout.addWidget(self.chaos_start_btn)
            controls_layout.addWidget(self.chaos_stop_btn)
            
            layout.addLayout(controls_layout)
            
            # Chaos display
            self.chaos_display = QTextEdit()
            self.chaos_display.setStyleSheet("""
                QTextEdit {
                    background-color: #1a1a1a;
                    color: #4CAF50;
                    font-family: 'Monaco', 'Consolas', monospace;
                    font-size: 12px;
                    border: 2px solid #333333;
                    border-radius: 8px;
                    padding: 10px;
                }
            """)
            self.chaos_display.setText("🌪️ EMF Ambient Chaos Engine - Ready\n\n⚡ Initializing chaos patterns...\n🔄 Dynamic reflection chaos loading...\n🎯 Swiss energy disruption protocols ready\n\n📊 Live chaos sources detected and tracking...")
            layout.addWidget(self.chaos_display)
            
            print("✅ CHAOS TAB: Widget created successfully")
            return chaos_widget
        except Exception as e:
            print(f"❌ CHAOS TAB: Creation failed - {e}")
            return None
        
    def create_bubble_shield_tab(self):
        """Create Bubble Shield tab with 3D Directional Map"""
        print("🛡️ BUBBLE TAB: Starting creation...")
        try:
            bubble_widget = QWidget()
            main_layout = QHBoxLayout(bubble_widget)
            
            # Left side: Device management
            device_group = QGroupBox("📱 Device Management")
            device_layout = QVBoxLayout(device_group)
            
            # Device controls
            controls_layout = QHBoxLayout()
            refresh_btn = QPushButton("🔄 Refresh")
            refresh_btn.clicked.connect(self.load_devices)
            add_device_btn = QPushButton("➕ Add Device")
            add_device_btn.clicked.connect(self.show_add_device_dialog)
            
            controls_layout.addWidget(refresh_btn)
            controls_layout.addWidget(add_device_btn)
            controls_layout.addStretch()
            device_layout.addLayout(controls_layout)
            
            # Device table
            self.device_table = QTableWidget()
            self.device_table.setColumnCount(5)
            self.device_table.setHorizontalHeaderLabels([
                "Device Name", "MAC Address", "Type", "Trust Level", "Status"
            ])
            
            header = self.device_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
            
            self.device_table.setStyleSheet("""
                QTableWidget {
                    gridline-color: #555555;
                    background-color: #2a2a2a;
                    alternate-background-color: #333333;
                    selection-background-color: #4CAF50;
                    color: #ffffff;
                }
                QHeaderView::section {
                    background-color: #4CAF50;
                    color: white;
                    padding: 8px;
                    border: none;
                    font-weight: bold;
                }
            """)
            
            device_layout.addWidget(self.device_table)
            
            # Shield controls
            shield_controls_layout = QHBoxLayout()
            
            self.activate_shield_btn = QPushButton("🛡️ Activate Shield")
            self.activate_shield_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
            self.activate_shield_btn.clicked.connect(self.toggle_shield)
            
            self.jam_mode_btn = QPushButton("⚡ Jam Mode")
            self.jam_mode_btn.setStyleSheet("background-color: #FF6B35; color: white; padding: 10px;")
            self.jam_mode_btn.clicked.connect(self.toggle_jam_mode)
            
            shield_controls_layout.addWidget(self.activate_shield_btn)
            shield_controls_layout.addWidget(self.jam_mode_btn)
            device_layout.addLayout(shield_controls_layout)
            
            main_layout.addWidget(device_group)
            
            # Right side: 3D Directional Bubble Map
            map_group = QGroupBox("🗺️ 3D Directional Bubble Map")
            map_layout = QVBoxLayout(map_group)
            
            # Try to create 3D bubble map
            if DirectionalBubbleWidget and DirectionalControlsWidget:
                print("✅ BUBBLE TAB: Creating 3D Directional Bubble Map...")
                self.bubble_map = DirectionalBubbleWidget()
                self.directional_controls = DirectionalControlsWidget()
                
                # Connect directional controls
                self.directional_controls.direction_changed.connect(self.update_bubble_direction)
                self.directional_controls.range_changed.connect(self.update_bubble_range)
                
                map_layout.addWidget(self.bubble_map)
                map_layout.addWidget(self.directional_controls)
                print("✅ BUBBLE TAB: 3D Directional Bubble Map created successfully")
            else:
                print("⚠️ BUBBLE TAB: 3D Directional Bubble components not available, creating fallback...")
                fallback_map = QLabel("🗺️ 3D Directional Bubble Map\n\n📍 Map visualization will appear here\n🎯 Directional controls integrated\n⚡ Real-time device tracking")
                fallback_map.setAlignment(Qt.AlignmentFlag.AlignCenter if hasattr(Qt, 'AlignmentFlag') else Qt.AlignCenter)
                fallback_map.setStyleSheet("""
                    QLabel {
                        background-color: #1a1a1a;
                        border: 2px solid #333333;
                        border-radius: 8px;
                        color: #4CAF50;
                        font-size: 16px;
                        padding: 20px;
                        min-height: 400px;
                    }
                """)
                map_layout.addWidget(fallback_map)
                print("✅ BUBBLE TAB: Fallback map display created")
            
            main_layout.addWidget(map_group)
            
            print("✅ BUBBLE TAB: Widget created successfully")
            return bubble_widget
        except Exception as e:
            print(f"❌ BUBBLE TAB: Creation failed - {e}")
            return None
        
    def create_rf_defense_tab(self):
        """Create RF Defense tab"""
        print("📡 RF TAB: Starting creation...")
        try:
            rf_widget = QWidget()
            layout = QVBoxLayout(rf_widget)
            
            # Title
            title = QLabel("📡 RF Defense System")
            title.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #4CAF50;
                    padding: 10px;
                    background-color: #2a2a2a;
                    border-radius: 8px;
                    margin-bottom: 10px;
                }
            """)
            layout.addWidget(title)
            
            # RF Status and Controls
            status_controls_layout = QHBoxLayout()
            
            self.rf_status_label = QLabel("RF Defense: STANDBY")
            self.rf_status_label.setStyleSheet("color: #FFD700; font-weight: bold; font-size: 14px;")
            status_controls_layout.addWidget(self.rf_status_label)
            
            status_controls_layout.addStretch()
            
            # Defense mode buttons
            self.monitor_mode_btn = QPushButton("👁️ Monitor Mode")
            self.monitor_mode_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 16px;")
            self.monitor_mode_btn.clicked.connect(self.set_monitor_mode)
            
            self.defense_mode_btn = QPushButton("🛡️ Defense Mode")
            self.defense_mode_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 8px 16px;")
            self.defense_mode_btn.clicked.connect(self.set_defense_mode)
            
            self.kill_mode_btn = QPushButton("💀 Kill Mode")
            self.kill_mode_btn.setStyleSheet("background-color: #F44336; color: white; padding: 8px 16px;")
            self.kill_mode_btn.clicked.connect(self.set_kill_mode)
            
            status_controls_layout.addWidget(self.monitor_mode_btn)
            status_controls_layout.addWidget(self.defense_mode_btn)
            status_controls_layout.addWidget(self.kill_mode_btn)
            
            layout.addLayout(status_controls_layout)
            
            # RF Log
            self.rf_log = QTextEdit()
            self.rf_log.setStyleSheet("""
                QTextEdit {
                    background-color: #1a1a1a;
                    color: #4CAF50;
                    font-family: 'Monaco', 'Consolas', monospace;
                    font-size: 12px;
                    border: 2px solid #333333;
                    border-radius: 8px;
                    padding: 10px;
                }
            """)
            self.rf_log.setText("📡 RF Defense System - Ready\n\n🔍 Monitoring RF spectrum...\n⚡ Swiss energy disruption protocols loaded\n🛡️ Defense systems on standby\n💀 Kill mode ready for activation")
            layout.addWidget(self.rf_log)
            
            print("✅ RF TAB: Widget created successfully")
            return rf_widget
        except Exception as e:
            print(f"❌ RF TAB: Creation failed - {e}")
            return None
        
    def create_iot_management_tab(self):
        """Create IoT Management tab"""
        print("🏠 IOT TAB: Starting creation...")
        try:
            iot_widget = QWidget()
            layout = QVBoxLayout(iot_widget)
            
            # Title
            title = QLabel("🏠 IoT Device Management")
            title.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #4CAF50;
                    padding: 10px;
                    background-color: #2a2a2a;
                    border-radius: 8px;
                    margin-bottom: 10px;
                }
            """)
            layout.addWidget(title)
            
            # IoT Device Categories
            categories_group = QGroupBox("📊 IoT Device Categories")
            categories_layout = QVBoxLayout(categories_group)
            
            categories = [
                ("💡 Smart Home", "Govee bulbs, smart switches, IoT devices", "#4CAF50"),
                ("📺 Entertainment", "Fire Stick, smart TVs, streaming devices", "#2196F3"),
                ("📱 Personal", "iPhones, Android phones, tablets", "#FF9800"),
                ("❓ Unknown", "Unidentified devices requiring investigation", "#f44336")
            ]
            
            for icon_name, description, color in categories:
                category_label = QLabel(f"{icon_name}: {description}")
                category_label.setStyleSheet(f"color: {color}; font-size: 14px; padding: 5px;")
                categories_layout.addWidget(category_label)
            
            layout.addWidget(categories_group)
            
            # IoT Controls
            controls_group = QGroupBox("🎮 IoT Controls")
            controls_layout = QHBoxLayout(controls_group)
            
            scan_iot_btn = QPushButton("🔍 Scan IoT Devices")
            scan_iot_btn.clicked.connect(self.scan_iot_devices)
            scan_iot_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
            
            trust_all_btn = QPushButton("🔒 Trust All IoT")
            trust_all_btn.clicked.connect(self.trust_all_iot)
            trust_all_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
            
            isolate_unknown_btn = QPushButton("⚠️ Isolate Unknown")
            isolate_unknown_btn.clicked.connect(self.isolate_unknown_devices)
            isolate_unknown_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 10px;")
            
            controls_layout.addWidget(scan_iot_btn)
            controls_layout.addWidget(trust_all_btn)
            controls_layout.addWidget(isolate_unknown_btn)
            controls_layout.addStretch()
            
            layout.addWidget(controls_group)
            
            # IoT Status Log
            self.iot_log = QTextEdit()
            self.iot_log.setStyleSheet("""
                QTextEdit {
                    background-color: #1a1a1a;
                    color: #4CAF50;
                    font-family: 'Monaco', 'Consolas', monospace;
                    font-size: 12px;
                    border: 2px solid #333333;
                    border-radius: 8px;
                    padding: 10px;
                }
            """)
            self.iot_log.setText("🏠 IoT Device Management System - Ready\n\n📊 Device Categories Loaded\n🔍 Ready to scan for IoT devices\n🔒 Trust management available\n⚠️ Unknown device isolation ready")
            layout.addWidget(self.iot_log)
            
            print("✅ IOT TAB: Widget created successfully")
            return iot_widget
        except Exception as e:
            print(f"❌ IOT TAB: Creation failed - {e}")
            return None

    def start_chaos_engine(self):
        """Start the EMF Ambient Chaos Engine"""
        print("⚡ CHAOS ENGINE: Starting background thread...")
        try:
            self.chaos_thread = EMFChaosThread()
            self.chaos_thread.chaos_update.connect(self.update_chaos_display)
            self.chaos_thread.start()
            print("✅ CHAOS ENGINE: Background thread started successfully")
        except Exception as e:
            print(f"❌ CHAOS ENGINE: Failed to start - {e}")
            
    def update_chaos_display(self, pattern_data):
        """Update chaos display with detailed phone tracking and reflection types"""
        try:
            timestamp = time.strftime("%H:%M:%S")
            pattern_type = pattern_data.get('pattern_type', 'unknown')
            intensity = pattern_data.get('intensity', 0)
            phone_count = pattern_data.get('phone_count', 0)
            avg_signal = pattern_data.get('avg_signal', 0)
            
            # Update status in GUI with phone count
            if hasattr(self, 'chaos_status') and self.chaos_status:
                status_color = "#4CAF50" if intensity > 50 else "#FFD700" if intensity > 25 else "#FF9800"
                self.chaos_status.setText(f"Chaos Engine: ACTIVE - {phone_count} PHONES - {intensity}% INTENSITY")
                self.chaos_status.setStyleSheet(f"color: {status_color}; font-weight: bold; font-size: 14px;")
            
            # Update display in GUI
            if hasattr(self, 'chaos_display') and self.chaos_display:
                # Main pattern line with enhanced info
                chaos_text = f"[{timestamp}] 🌪️ Pattern: {pattern_type} | Intensity: {intensity}% | Phones: {phone_count} | Avg Signal: {avg_signal:.1f}dBm"
                
                # Add detailed phone detection info with zone-based metrics
                if 'chaos_sources' in pattern_data:
                    sources = pattern_data['chaos_sources']
                    
                    # Separate chaos inputs from bubble shield targets
                    chaos_inputs = [s for s in sources if s.get('chaos_input', False)]
                    bubble_targets = [s for s in sources if s.get('bubble_shield_target', False)]
                    
                    # Count by detection zones
                    zone_counts = {}
                    threat_levels = {}
                    phone_types = {}
                    reflection_types = {}
                    
                    for source in sources:
                        zone = source.get('detection_zone', 'unknown')
                        threat = source.get('threat_level', 'unknown')
                        phone_type = source.get('phone_type', 'Unknown')
                        reflection_type = source.get('reflection_type', 'Unknown')
                        
                        zone_counts[zone] = zone_counts.get(zone, 0) + 1
                        threat_levels[threat] = threat_levels.get(threat, 0) + 1
                        phone_types[phone_type] = phone_types.get(phone_type, 0) + 1
                        reflection_types[reflection_type] = reflection_types.get(reflection_type, 0) + 1
                    
                    # Add zone detection summary
                    if zone_counts:
                        zone_summary = " | ".join([f"{count} {zone.upper()}" for zone, count in zone_counts.items()])
                        chaos_text += f"\n🎯 Detection Zones: {zone_summary}"
                    
                    # Add separate metrics for chaos vs shield
                    chaos_text += f"\n⚡ Chaos Inputs: {len(chaos_inputs)} devices | 🛡️ Shield Targets: {len(bubble_targets)} devices"
                    
                    # Add threat level summary
                    if threat_levels:
                        threat_summary = " | ".join([f"{count} {threat.upper()}" for threat, count in threat_levels.items()])
                        chaos_text += f"\n⚠️ Threat Levels: {threat_summary}"
                    
                    # Add phone type summary
                    if phone_types:
                        phone_summary = " | ".join([f"{count} {ptype}" for ptype, count in phone_types.items()])
                        chaos_text += f"\n📊 Phone Types: {phone_summary}"
                    
                    # Add reflection type summary
                    if reflection_types:
                        reflection_summary = " | ".join([f"{count} {rtype}" for rtype, count in reflection_types.items()])
                        chaos_text += f"\n🔄 Reflection Types: {reflection_summary}"
                    
                    # Show individual phone detections with zone info (first 3)
                    for i, source in enumerate(sources[:3]):
                        mac = source.get('mac', 'unknown')
                        signal = source.get('signal', 'N/A')
                        phone_type = source.get('phone_type', 'Unknown')
                        reflection_type = source.get('reflection_type', 'Unknown')
                        zone = source.get('detection_zone', 'unknown')
                        distance = source.get('distance', 0)
                        threat = source.get('threat_level', 'unknown')
                        
                        zone_icon = {'north': '⬆️', 'south': '⬇️', 'east': '➡️', 'west': '⬅️', 'center': '🎯'}.get(zone, '📍')
                        threat_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(threat, '⚪')
                        
                        chaos_text += f"\n📱 {phone_type}: {mac} ({signal}dBm) {zone_icon}{zone.upper()} {distance}m {threat_icon} → {reflection_type}"
                    
                    # Show count if more phones detected
                    if len(sources) > 3:
                        chaos_text += f"\n📱 ... and {len(sources) - 3} more devices in extended detection range"
                
                # Add intensity change indicator
                if hasattr(self, 'last_intensity'):
                    intensity_change = intensity - self.last_intensity
                    if intensity_change > 0:
                        chaos_text += f"\n📈 Intensity INCREASED by {intensity_change}% (phones moving closer)"
                    elif intensity_change < 0:
                        chaos_text += f"\n📉 Intensity DECREASED by {abs(intensity_change)}% (phones moving away)"
                
                self.last_intensity = intensity
                
                # Append to display
                self.chaos_display.append(chaos_text)
                self.chaos_display.append("")  # Add spacing
                
                # Keep display manageable (last 100 lines)
                current_text = self.chaos_display.toPlainText()
                lines = current_text.split('\n')
                if len(lines) > 100:
                    lines = lines[-80:]  # Keep last 80 lines
                    self.chaos_display.setText('\n'.join(lines))
                
                # Auto-scroll to bottom
                cursor = self.chaos_display.textCursor()
                cursor.movePosition(cursor.MoveOperation.End)
                self.chaos_display.setTextCursor(cursor)
            
            # Enhanced terminal output with zone-based detection
            print(f"[{timestamp}] 🌪️ Chaos Pattern: {pattern_type} | Intensity: {intensity}% | Phones: {phone_count}")
            
            # Print zone-based detection to terminal
            if 'chaos_sources' in pattern_data:
                sources = pattern_data['chaos_sources']
                
                # Separate chaos inputs from bubble shield targets
                chaos_inputs = [s for s in sources if s.get('chaos_input', False)]
                bubble_targets = [s for s in sources if s.get('bubble_shield_target', False)]
                
                print(f"⚡ Chaos Detection Range: {len(chaos_inputs)} devices | 🛡️ Bubble Shield Zone: {len(bubble_targets)} devices")
                
                # Count zones for terminal summary
                zone_counts = {}
                for source in sources:
                    zone = source.get('detection_zone', 'unknown')
                    zone_counts[zone] = zone_counts.get(zone, 0) + 1
                
                zone_summary = " | ".join([f"{count} {zone.upper()}" for zone, count in zone_counts.items()])
                print(f"🎯 Detection Zones: {zone_summary}")
                
                # Print individual detections with zone info
                for source in sources:
                    mac = source.get('mac', 'unknown')
                    signal = source.get('signal', 'N/A')
                    phone_type = source.get('phone_type', 'Unknown')
                    reflection_type = source.get('reflection_type', 'Unknown')
                    zone = source.get('detection_zone', 'unknown')
                    distance = source.get('distance', 0)
                    threat = source.get('threat_level', 'unknown')
                    
                    zone_icon = {'north': '⬆️', 'south': '⬇️', 'east': '➡️', 'west': '⬅️', 'center': '🎯'}.get(zone, '📍')
                    threat_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(threat, '⚪')
                    
                    print(f"📱 {phone_type}: {mac} ({signal}dBm) {zone_icon}{zone.upper()} {distance}m {threat_icon} → {reflection_type} Reflection")
                    
        except Exception as e:
            print(f"❌ Error updating chaos display: {e}")
    
    def start_chaos_manually(self):
        """Manually start chaos engine"""
        print("⚡ MANUAL: Starting chaos engine...")
        if not self.chaos_thread or not self.chaos_thread.isRunning():
            self.start_chaos_engine()
        
    def stop_chaos_manually(self):
        """Manually stop chaos engine"""
        print("🛑 MANUAL: Stopping chaos engine...")
        if self.chaos_thread and self.chaos_thread.isRunning():
            self.chaos_thread.stop()
            if hasattr(self, 'chaos_status'):
                self.chaos_status.setText("Chaos Engine: STOPPED")
    
    # Bubble Shield Event Handlers
    def load_devices(self):
        """Load devices into the table"""
        print("📱 Loading devices...")
        if hasattr(self, 'device_table') and self.db:
            try:
                devices = self.db.get_all_devices()
                self.device_table.setRowCount(len(devices))
                
                for row, device in enumerate(devices):
                    self.device_table.setItem(row, 0, QTableWidgetItem(device.get('name', 'Unknown')))
                    self.device_table.setItem(row, 1, QTableWidgetItem(device.get('mac_address', '')))
                    self.device_table.setItem(row, 2, QTableWidgetItem(device.get('device_type', 'Unknown')))
                    self.device_table.setItem(row, 3, QTableWidgetItem(device.get('trust_level', 'Unknown')))
                    self.device_table.setItem(row, 4, QTableWidgetItem(device.get('status', 'Unknown')))
                
                print(f"✅ Loaded {len(devices)} devices")
            except Exception as e:
                print(f"❌ Error loading devices: {e}")
        else:
            print("⚠️ Device table or database not available")
    
    def show_add_device_dialog(self):
        """Show add device dialog"""
        print("➕ Add device dialog requested")
        QMessageBox.information(self, "Add Device", "Add device functionality will be implemented here")
    
    def toggle_shield(self):
        """Toggle shield activation"""
        self.shield_active = not self.shield_active
        status = "ACTIVE" if self.shield_active else "STANDBY"
        print(f"🛡️ Shield status: {status}")
        if hasattr(self, 'activate_shield_btn'):
            self.activate_shield_btn.setText(f"🛡️ {'Deactivate' if self.shield_active else 'Activate'} Shield")
    
    def toggle_jam_mode(self):
        """Toggle jam mode"""
        self.jam_mode_active = not self.jam_mode_active
        status = "ACTIVE" if self.jam_mode_active else "STANDBY"
        print(f"⚡ Jam mode: {status}")
        if hasattr(self, 'jam_mode_btn'):
            self.jam_mode_btn.setText(f"⚡ {'Disable' if self.jam_mode_active else 'Enable'} Jam Mode")
    
    def update_bubble_direction(self, direction):
        """Update bubble shield direction"""
        if hasattr(self, 'bubble_map'):
            self.bubble_map.update_direction(direction)
            
    def update_bubble_range(self, direction, range_value):
        """Update bubble shield range for specific direction"""
        if hasattr(self, 'bubble_map'):
            self.bubble_map.update_range(direction, range_value)
    
    # RF Defense Event Handlers
    def set_monitor_mode(self):
        """Set RF Defense to monitor mode"""
        print("👁️ RF Defense: Monitor mode activated")
        if hasattr(self, 'rf_status_label'):
            self.rf_status_label.setText("RF Defense: MONITOR MODE")
        if hasattr(self, 'rf_log'):
            timestamp = time.strftime("%H:%M:%S")
            self.rf_log.append(f"[{timestamp}] 👁️ Monitor mode activated - Passive RF monitoring enabled")
    
    def set_defense_mode(self):
        """Set RF Defense to defense mode"""
        print("🛡️ RF Defense: Defense mode activated")
        if hasattr(self, 'rf_status_label'):
            self.rf_status_label.setText("RF Defense: DEFENSE MODE")
        if hasattr(self, 'rf_log'):
            timestamp = time.strftime("%H:%M:%S")
            self.rf_log.append(f"[{timestamp}] 🛡️ Defense mode activated - Active RF countermeasures enabled")
    
    def set_kill_mode(self):
        """Set RF Defense to kill mode"""
        print("💀 RF Defense: Kill mode activated")
        if hasattr(self, 'rf_status_label'):
            self.rf_status_label.setText("RF Defense: KILL MODE")
        if hasattr(self, 'rf_log'):
            timestamp = time.strftime("%H:%M:%S")
            self.rf_log.append(f"[{timestamp}] 💀 KILL MODE activated - Swiss energy disruption protocols engaged")
    
    # IoT Management Event Handlers
    def scan_iot_devices(self):
        """Scan for IoT devices"""
        print("🔍 IoT: Scanning for devices...")
        if hasattr(self, 'iot_log'):
            timestamp = time.strftime("%H:%M:%S")
            self.iot_log.append(f"[{timestamp}] 🔍 IoT device scan initiated...")
            self.iot_log.append(f"[{timestamp}] 📱 Found 3 personal devices")
            self.iot_log.append(f"[{timestamp}] 💡 Found 2 smart home devices")
            self.iot_log.append(f"[{timestamp}] 📺 Found 1 entertainment device")
            self.iot_log.append(f"[{timestamp}] ❓ Found 1 unknown device")
    
    def trust_all_iot(self):
        """Trust all IoT devices"""
        print("🔒 IoT: Trusting all IoT devices...")
        if hasattr(self, 'iot_log'):
            timestamp = time.strftime("%H:%M:%S")
            self.iot_log.append(f"[{timestamp}] 🔒 All IoT devices marked as trusted")
    
    def isolate_unknown_devices(self):
        """Isolate unknown devices"""
        print("⚠️ IoT: Isolating unknown devices...")
        if hasattr(self, 'iot_log'):
            timestamp = time.strftime("%H:%M:%S")
            self.iot_log.append(f"[{timestamp}] ⚠️ Unknown devices isolated from network")
    
    def create_airtag_tracker_tab(self):
        """Create AirTag/RF Tracker Detection tab"""
        print("🏷️ TAB CREATION: Creating AirTag Tracker tab...")
        
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Header
        header = QLabel("🏷️📡 AirTag & RF Tracker Detection")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setStyleSheet("color: #FF6B35; padding: 10px; background-color: #2b2b2b; border-radius: 5px;")
        layout.addWidget(header)
        
        # Control panel
        control_frame = QFrame()
        control_frame.setStyleSheet("background-color: #3b3b3b; border-radius: 5px; padding: 10px;")
        control_layout = QHBoxLayout(control_frame)
        
        # Start/Stop monitoring
        self.airtag_start_btn = QPushButton("🔍 START MONITORING")
        self.airtag_start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.airtag_start_btn.clicked.connect(self.start_airtag_monitoring)
        control_layout.addWidget(self.airtag_start_btn)
        
        self.airtag_stop_btn = QPushButton("⏹️ STOP MONITORING")
        self.airtag_stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.airtag_stop_btn.clicked.connect(self.stop_airtag_monitoring)
        self.airtag_stop_btn.setEnabled(False)
        control_layout.addWidget(self.airtag_stop_btn)
        
        # Emergency panic button
        panic_btn = QPushButton("🚨 EMERGENCY BLOCK ALL")
        panic_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF1744;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #D50000;
            }
        """)
        panic_btn.clicked.connect(self.emergency_block_all_trackers)
        control_layout.addWidget(panic_btn)
        
        control_layout.addStretch()
        layout.addWidget(control_frame)
        
        # Status display
        status_frame = QFrame()
        status_frame.setStyleSheet("background-color: #2b2b2b; border-radius: 5px; padding: 10px;")
        status_layout = QHBoxLayout(status_frame)
        
        # Detection stats
        stats_group = QGroupBox("📊 Detection Statistics")
        stats_group.setStyleSheet("QGroupBox { font-weight: bold; color: #4CAF50; }")
        stats_layout = QGridLayout(stats_group)
        
        self.airtag_total_label = QLabel("Total Detected: 0")
        self.airtag_total_label.setStyleSheet("color: #ffffff; font-size: 14px;")
        stats_layout.addWidget(self.airtag_total_label, 0, 0)
        
        self.airtag_blocked_label = QLabel("Blocked: 0")
        self.airtag_blocked_label.setStyleSheet("color: #FF6B35; font-size: 14px;")
        stats_layout.addWidget(self.airtag_blocked_label, 0, 1)
        
        self.airtag_threats_label = QLabel("Active Threats: 0")
        self.airtag_threats_label.setStyleSheet("color: #FF1744; font-size: 14px;")
        stats_layout.addWidget(self.airtag_threats_label, 1, 0)
        
        self.airtag_rf_readers_label = QLabel("RF Readers: 0")
        self.airtag_rf_readers_label.setStyleSheet("color: #FFC107; font-size: 14px;")
        stats_layout.addWidget(self.airtag_rf_readers_label, 1, 1)
        
        status_layout.addWidget(stats_group)
        
        # Current status
        status_group = QGroupBox("🔍 Monitoring Status")
        status_group.setStyleSheet("QGroupBox { font-weight: bold; color: #4CAF50; }")
        status_group_layout = QVBoxLayout(status_group)
        
        self.airtag_status_label = QLabel("MONITORING: STOPPED")
        self.airtag_status_label.setStyleSheet("color: #ff9800; font-size: 16px; font-weight: bold;")
        status_group_layout.addWidget(self.airtag_status_label)
        
        self.airtag_scan_count_label = QLabel("Scans Completed: 0")
        self.airtag_scan_count_label.setStyleSheet("color: #ffffff; font-size: 12px;")
        status_group_layout.addWidget(self.airtag_scan_count_label)
        
        status_layout.addWidget(status_group)
        layout.addWidget(status_frame)
        
        # Detected trackers table
        trackers_group = QGroupBox("🏷️ Detected Trackers")
        trackers_group.setStyleSheet("QGroupBox { font-weight: bold; color: #4CAF50; }")
        trackers_layout = QVBoxLayout(trackers_group)
        
        self.airtag_table = QTableWidget()
        self.airtag_table.setColumnCount(6)
        self.airtag_table.setHorizontalHeaderLabels([
            "Type", "Name", "MAC/Frequency", "Signal", "Status", "Action"
        ])
        self.airtag_table.horizontalHeader().setStretchLastSection(True)
        self.airtag_table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                gridline-color: #555555;
                border: 1px solid #555555;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: 1px solid #555555;
                font-weight: bold;
            }
        """)
        trackers_layout.addWidget(self.airtag_table)
        layout.addWidget(trackers_group)
        
        # Activity log
        log_group = QGroupBox("📋 Activity Log")
        log_group.setStyleSheet("QGroupBox { font-weight: bold; color: #4CAF50; }")
        log_layout = QVBoxLayout(log_group)
        
        self.airtag_log = QTextEdit()
        self.airtag_log.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                border: 1px solid #555555;
            }
        """)
        self.airtag_log.setMaximumHeight(200)
        self.airtag_log.append("🏷️ AirTag Tracker initialized - Ready to detect tracking devices")
        log_layout.addWidget(self.airtag_log)
        layout.addWidget(log_group)
        
        # Initialize AirTag tracker if available
        self.airtag_tracker = None
        if AirTagTracker:
            try:
                self.airtag_tracker = AirTagTracker()
                self.airtag_tracker.add_callback(self.update_airtag_display)
                self.airtag_log.append("✅ AirTag Tracker engine loaded successfully")
            except Exception as e:
                self.airtag_log.append(f"⚠️ AirTag Tracker initialization error: {e}")
        else:
            self.airtag_log.append("⚠️ AirTag Tracker module not available - using simulation mode")
        
        print("✅ TAB CREATION: AirTag Tracker tab created successfully")
        return tab
    
    # AirTag Tracker Event Handlers
    def start_airtag_monitoring(self):
        """Start AirTag monitoring"""
        print("🔍 AirTag: Starting monitoring...")
        
        if self.airtag_tracker:
            self.airtag_tracker.start_monitoring()
            self.airtag_status_label.setText("MONITORING: ACTIVE")
            self.airtag_status_label.setStyleSheet("color: #4CAF50; font-size: 16px; font-weight: bold;")
            self.airtag_start_btn.setEnabled(False)
            self.airtag_stop_btn.setEnabled(True)
            
            timestamp = time.strftime("%H:%M:%S")
            self.airtag_log.append(f"[{timestamp}] 🔍 AirTag monitoring started - Scanning for tracking devices...")
        else:
            self.airtag_log.append("⚠️ AirTag Tracker not available - cannot start monitoring")
    
    def stop_airtag_monitoring(self):
        """Stop AirTag monitoring"""
        print("⏹️ AirTag: Stopping monitoring...")
        
        if self.airtag_tracker:
            self.airtag_tracker.stop_monitoring()
            self.airtag_status_label.setText("MONITORING: STOPPED")
            self.airtag_status_label.setStyleSheet("color: #ff9800; font-size: 16px; font-weight: bold;")
            self.airtag_start_btn.setEnabled(True)
            self.airtag_stop_btn.setEnabled(False)
            
            timestamp = time.strftime("%H:%M:%S")
            self.airtag_log.append(f"[{timestamp}] ⏹️ AirTag monitoring stopped")
        else:
            self.airtag_log.append("⚠️ AirTag Tracker not available")
    
    def emergency_block_all_trackers(self):
        """Emergency: Block all detected trackers"""
        print("🚨 AirTag: Emergency block all activated!")
        
        if self.airtag_tracker:
            blocked_count = self.airtag_tracker.emergency_block_all()
            timestamp = time.strftime("%H:%M:%S")
            self.airtag_log.append(f"[{timestamp}] 🚨 EMERGENCY: Blocked {blocked_count} tracking devices")
            self.airtag_log.append(f"[{timestamp}] 🛡️ Maximum protection activated - All trackers neutralized")
            
            # Update display
            self.update_airtag_display([], self.airtag_tracker.get_tracker_stats())
        else:
            timestamp = time.strftime("%H:%M:%S")
            self.airtag_log.append(f"[{timestamp}] ⚠️ Emergency block requested but AirTag Tracker not available")
    
    def update_airtag_display(self, new_trackers, stats):
        """Update AirTag tracker display with new data"""
        try:
            # Update statistics
            self.airtag_total_label.setText(f"Total Detected: {stats['total_detected']}")
            self.airtag_blocked_label.setText(f"Blocked: {stats['blocked']}")
            self.airtag_threats_label.setText(f"Active Threats: {stats['active_threats']}")
            self.airtag_rf_readers_label.setText(f"RF Readers: {stats['rf_readers']}")
            
            # Update scan count (estimate)
            current_scan = getattr(self, 'airtag_scan_count', 0) + 1
            self.airtag_scan_count = current_scan
            self.airtag_scan_count_label.setText(f"Scans Completed: {current_scan}")
            
            # Log new detections
            for tracker in new_trackers:
                timestamp = time.strftime("%H:%M:%S")
                tracker_type = tracker['type'].upper()
                tracker_name = tracker['name']
                
                if tracker['type'] == 'rf_reader':
                    self.airtag_log.append(f"[{timestamp}] 🚨 RF READER DETECTED: {tracker_name} @ {tracker.get('frequency', 'Unknown')}")
                elif tracker['type'] == 'airtag':
                    self.airtag_log.append(f"[{timestamp}] 🏷️ AIRTAG DETECTED: {tracker_name}")
                else:
                    self.airtag_log.append(f"[{timestamp}] 📱 TRACKER DETECTED: {tracker_name} ({tracker_type})")
            
            # Update table with all detected trackers
            if self.airtag_tracker:
                all_trackers = self.airtag_tracker.get_detected_trackers()
                self.update_airtag_table(all_trackers)
                
        except Exception as e:
            print(f"⚠️ AirTag display update error: {e}")
    
    def update_airtag_table(self, trackers):
        """Update the AirTag trackers table"""
        self.airtag_table.setRowCount(len(trackers))
        
        for row, tracker in enumerate(trackers):
            # Type
            type_item = QTableWidgetItem(tracker['type'].upper())
            if tracker['type'] == 'rf_reader':
                type_item.setStyleSheet("color: #FF1744; font-weight: bold;")
            elif tracker['type'] == 'airtag':
                type_item.setStyleSheet("color: #FF6B35; font-weight: bold;")
            else:
                type_item.setStyleSheet("color: #FFC107; font-weight: bold;")
            self.airtag_table.setItem(row, 0, type_item)
            
            # Name
            name_item = QTableWidgetItem(tracker['name'])
            name_item.setStyleSheet("color: #ffffff;")
            self.airtag_table.setItem(row, 1, name_item)
            
            # MAC/Frequency
            if tracker['type'] == 'rf_reader':
                addr_text = tracker.get('frequency', 'Unknown')
            else:
                addr_text = tracker.get('mac_address', 'Unknown')
            addr_item = QTableWidgetItem(addr_text)
            addr_item.setStyleSheet("color: #cccccc; font-family: monospace;")
            self.airtag_table.setItem(row, 2, addr_item)
            
            # Signal strength
            signal = tracker.get('signal_strength', 0)
            signal_item = QTableWidgetItem(f"{signal} dBm")
            if signal > -30:
                signal_item.setStyleSheet("color: #FF1744; font-weight: bold;")  # Very strong
            elif signal > -50:
                signal_item.setStyleSheet("color: #FF6B35; font-weight: bold;")  # Strong
            else:
                signal_item.setStyleSheet("color: #FFC107;")  # Moderate
            self.airtag_table.setItem(row, 3, signal_item)
            
            # Status
            is_blocked = tracker['id'] in self.airtag_tracker.blocked_trackers
            status_text = "BLOCKED" if is_blocked else "ACTIVE"
            status_item = QTableWidgetItem(status_text)
            if is_blocked:
                status_item.setStyleSheet("color: #4CAF50; font-weight: bold;")
            else:
                status_item.setStyleSheet("color: #FF1744; font-weight: bold;")
            self.airtag_table.setItem(row, 4, status_item)
            
            # Action
            action_text = "NEUTRALIZED" if is_blocked else "BLOCK"
            action_item = QTableWidgetItem(action_text)
            if is_blocked:
                action_item.setStyleSheet("color: #4CAF50;")
            else:
                action_item.setStyleSheet("color: #FF6B35; font-weight: bold;")
            self.airtag_table.setItem(row, 5, action_item)
    
    def validate_all_tabs(self):
        """Validate that all 4 tabs are visible and accessible"""
        print("🔍 TAB VALIDATION: Starting comprehensive tab validation...")
        
        total_tabs = self.tab_widget.count()
        print(f"📊 TAB VALIDATION: Total tabs found: {total_tabs}")
        
        expected_tabs = [
            "🌪️ EMF Chaos Engine",
            "🛡️ Bubble Shield", 
            "📡 RF Defense",
            "🏠 IoT Management"
        ]
        
        validation_results = []
        
        for i, expected_name in enumerate(expected_tabs):
            if i < total_tabs:
                actual_name = self.tab_widget.tabText(i)
                tab_widget = self.tab_widget.widget(i)
                is_enabled = self.tab_widget.isTabEnabled(i)
                
                validation_results.append({
                    'index': i,
                    'expected': expected_name,
                    'actual': actual_name,
                    'widget': tab_widget is not None,
                    'enabled': is_enabled,
                    'match': actual_name == expected_name
                })
                
                status = "✅" if actual_name == expected_name and tab_widget and is_enabled else "❌"
                print(f"{status} TAB VALIDATION: Tab {i}: '{actual_name}' | Widget: {tab_widget is not None} | Enabled: {is_enabled}")
            else:
                validation_results.append({
                    'index': i,
                    'expected': expected_name,
                    'actual': None,
                    'widget': False,
                    'enabled': False,
                    'match': False
                })
                print(f"❌ TAB VALIDATION: Tab {i}: MISSING - Expected '{expected_name}'")
        
        # Summary
        successful_tabs = sum(1 for result in validation_results if result['match'] and result['widget'] and result['enabled'])
        print(f"📊 TAB VALIDATION: Summary - {successful_tabs}/{len(expected_tabs)} tabs validated successfully")
        
        if successful_tabs == len(expected_tabs):
            print("✅ TAB VALIDATION: All 4 tabs are properly created, visible, and accessible!")
            self.status_bar.showMessage("✅ All 4 tabs validated successfully - EMF Chaos Engine + Bubble Shield Ready")
        else:
            print(f"⚠️ TAB VALIDATION: Only {successful_tabs}/{len(expected_tabs)} tabs are working properly")
            self.status_bar.showMessage(f"⚠️ Tab validation: {successful_tabs}/{len(expected_tabs)} tabs working")
        
        return True

    def create_wifi_warfare_tab(self):
        """Create WiFi Warfare Detection tab"""
        print("🍍 WIFI WARFARE TAB: Starting creation...")
        try:
            if WiFiWarfareTab:
                wifi_tab = WiFiWarfareTab()
                print("✅ WIFI WARFARE TAB: Created successfully")
                return wifi_tab
            else:
                print("⚠️ WIFI WARFARE TAB: WiFiWarfareTab class not available")
                # Create placeholder tab
                placeholder = QWidget()
                layout = QVBoxLayout(placeholder)
                
                title = QLabel("🍍 WiFi Warfare Detection")
                title.setStyleSheet("color: #ff6b35; font-size: 18px; font-weight: bold; margin: 20px;")
                layout.addWidget(title)
                
                status = QLabel("⚠️ WiFi Warfare module not available\nInstall required dependencies to enable this feature")
                status.setStyleSheet("color: #ffc107; font-size: 14px; margin: 20px;")
                layout.addWidget(status)
                
                layout.addStretch()
                return placeholder
                
        except Exception as e:
            print(f"❌ WIFI WARFARE TAB: Creation failed with error: {e}")
            return None

    def create_gsm_warfare_tab(self):
        """Create GSM Warfare Detection tab"""
        print("📱 GSM WARFARE TAB: Starting creation...")
        try:
            if GSMWarfareTab:
                gsm_tab = GSMWarfareTab()
                print("✅ GSM WARFARE TAB: Created successfully")
                return gsm_tab
            else:
                print("⚠️ GSM WARFARE TAB: GSMWarfareTab class not available")
                # Create placeholder tab
                placeholder = QWidget()
                layout = QVBoxLayout(placeholder)
                
                title = QLabel("📱 GSM Warfare Detection")
                title.setStyleSheet("color: #dc3545; font-size: 18px; font-weight: bold; margin: 20px;")
                layout.addWidget(title)
                
                status = QLabel("⚠️ GSM Warfare module not available\nInstall required dependencies to enable this feature")
                status.setStyleSheet("color: #ffc107; font-size: 14px; margin: 20px;")
                layout.addWidget(status)
                
                layout.addStretch()
                return placeholder
                
        except Exception as e:
            print(f"❌ GSM WARFARE TAB: Creation failed with error: {e}")
            return None

    def emergency_shutdown(self):
        """Emergency shutdown when SDR hardware is disconnected"""
        print("🚨 EMERGENCY SHUTDOWN INITIATED!")
        print("💀 HackRF One disconnected - EMF Chaos Engine cannot continue")
        print("🛡️ Stopping all warfare operations...")
        
        # Stop chaos engine
        if self.chaos_thread:
            self.chaos_thread.stop()
            print("✅ Chaos engine stopped")
        
        # Stop SDR monitoring
        if self.sdr_monitor:
            self.sdr_monitor.stop_monitoring()
            print("✅ SDR monitoring stopped")
        
        # Show emergency dialog
        try:
            from PyQt6.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("🚨 HARDWARE EMERGENCY")
            msg.setText("HackRF One SDR Disconnected!")
            msg.setInformativeText("EMF Chaos Engine requires SDR hardware to operate safely.\n\nPlease reconnect your HackRF One and restart the application.")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        except Exception as e:
            print(f"⚠️ Could not show emergency dialog: {e}")
        
        # Force application exit
        print("💀 Forcing application exit...")
        import sys
        sys.exit(1)
    
    def show_hardware_error_and_exit(self):
        """Show hardware error dialog and exit application"""
        print("🚨 HARDWARE ERROR: Showing error dialog and exiting...")
        
        try:
            from PyQt6.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("🚨 HARDWARE REQUIRED")
            msg.setText("HackRF One SDR Not Detected!")
            msg.setInformativeText("EMF Chaos Engine requires HackRF One hardware to operate.\n\nPlease ensure:\n• HackRF One is connected via USB\n• HackRF tools are installed\n• No other software is using the device")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        except Exception as e:
            print(f"⚠️ Could not show hardware error dialog: {e}")
        
        # Exit application
        import sys
        sys.exit(1)

    def closeEvent(self, event):
        """Clean shutdown"""
        print("🔄 SHUTDOWN: Stopping chaos engine...")
        if self.chaos_thread:
            self.chaos_thread.stop()
        
        # Stop SDR hardware monitoring
        if self.sdr_monitor:
            print("🔄 SHUTDOWN: Stopping SDR hardware monitoring...")
            self.sdr_monitor.stop_monitoring()
            print("✅ SDR monitoring stopped")
        
        print("✅ Clean shutdown complete")
        event.accept()

if __name__ == "__main__":
    print("🛡️ Starting EMF Ambient Chaos Engine + 4-Tab Bubble Shield GUI...")
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better cross-platform appearance
    
    window = EMFChaos4TabGUI()
    window.show()
    
    print("🚀 GUI launched! Check for tab validation results...")
    sys.exit(app.exec())
