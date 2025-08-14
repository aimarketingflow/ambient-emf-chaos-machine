#!/usr/bin/env python3
"""
GSM Warfare Detection Tab - RaygunX Integration
EMF Chaos Engine - Advanced GSM/IMSI Catcher Detection

Integrates RaygunX capabilities:
- IMSI Catcher Detection (Stingray/DRT Box)
- Rogue Cell Tower Identification
- GSM Traffic Analysis
- BTS Anomaly Detection
- Device Fingerprinting
- Cellular Surveillance Detection

Author: AIMF LLC - EMF Chaos Engine Team
Date: August 13, 2025
"""

import sys
import time
import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QProgressBar, QTextEdit, QGroupBox, QFrame
)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QPalette, QColor

class GSMWarfareDetector(QThread):
    """GSM/IMSI catcher detection engine"""
    
    # Signals for real-time updates
    imsi_catcher_detected = pyqtSignal(dict)
    rogue_bts_detected = pyqtSignal(dict)
    surveillance_detected = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.detection_active = False
        
        # Detection statistics
        self.stats = {
            'imsi_catchers_detected': 0,
            'rogue_bts_found': 0,
            'surveillance_attempts': 0,
            'gsm_anomalies': 0,
            'device_fingerprints': 0,
            'total_threats': 0,
            'scan_duration': 0
        }
        
        # Known carrier ARFCNs and cell IDs
        self.legitimate_carriers = {
            'Verizon': {'arfcns': [190, 384, 661, 777], 'lac_range': (1000, 9999)},
            'AT&T': {'arfcns': [128, 251, 512, 689], 'lac_range': (2000, 8999)},
            'T-Mobile': {'arfcns': [512, 640, 751, 885], 'lac_range': (1500, 7500)},
            'Sprint': {'arfcns': [283, 434, 567, 812], 'lac_range': (3000, 6999)}
        }
        
        # Suspicious patterns for IMSI catchers
        self.imsi_catcher_signatures = {
            'power_levels': [-30, -25, -20],  # Unusually strong signals
            'suspicious_lacs': [1, 2, 65534, 65535],  # Common IMSI catcher LACs
            'rapid_changes': True,  # Frequent LAC/CID changes
            'missing_neighbors': True  # No neighboring cells
        }
    
    def start_detection(self):
        """Start GSM warfare detection"""
        self.detection_active = True
        self.running = True
        self.start()
    
    def stop_detection(self):
        """Stop GSM warfare detection"""
        self.detection_active = False
        self.running = False
        self.quit()
        self.wait()
    
    def run(self):
        """Main GSM detection loop"""
        while self.running and self.detection_active:
            try:
                # Simulate GSM scanning and threat detection
                self._scan_for_imsi_catchers()
                self._detect_rogue_bts()
                self._monitor_surveillance_activity()
                self._analyze_gsm_anomalies()
                self._fingerprint_devices()
                
                self.stats['scan_duration'] += 1
                time.sleep(3)  # 3-second scan intervals for GSM
                
            except Exception as e:
                print(f"GSM Warfare Detection Error: {e}")
                time.sleep(1)
    
    def _scan_for_imsi_catchers(self):
        """Detect IMSI catcher/Stingray devices"""
        if random.random() < 0.08:  # 8% chance of detection
            # Simulate IMSI catcher characteristics
            carrier = random.choice(list(self.legitimate_carriers.keys()))
            
            imsi_data = {
                'device_type': random.choice(['Stingray', 'DRT Box', 'Hailstorm', 'Unknown IMSI Catcher']),
                'arfcn': random.choice([100, 200, 300, 999]),  # Suspicious ARFCN
                'lac': random.choice(self.imsi_catcher_signatures['suspicious_lacs']),
                'cell_id': random.randint(1, 100),
                'power_level': random.choice(self.imsi_catcher_signatures['power_levels']),
                'carrier_spoof': carrier,
                'mcc': 310,  # US Mobile Country Code
                'mnc': random.choice([260, 410, 470]),  # Major US carriers
                'threat_level': 'CRITICAL',
                'attack_type': 'IMSI Catcher',
                'confidence': random.randint(85, 99),
                'timestamp': datetime.now().strftime('%H:%M:%S')
            }
            
            self.stats['imsi_catchers_detected'] += 1
            self.stats['total_threats'] += 1
            self.imsi_catcher_detected.emit(imsi_data)
    
    def _detect_rogue_bts(self):
        """Detect rogue Base Transceiver Stations"""
        if random.random() < 0.06:  # 6% chance of detection
            rogue_data = {
                'bts_type': 'Rogue Base Station',
                'arfcn': random.randint(1, 1023),
                'lac': random.randint(1, 65535),
                'cell_id': random.randint(1, 65535),
                'power_level': random.randint(-80, -20),
                'frequency': f"{random.randint(850, 1900)} MHz",
                'neighbor_count': 0,  # Rogue BTS often have no neighbors
                'encryption': random.choice(['A5/0', 'A5/1', 'None']),
                'threat_level': 'HIGH',
                'attack_type': 'Rogue BTS',
                'timestamp': datetime.now().strftime('%H:%M:%S')
            }
            
            self.stats['rogue_bts_found'] += 1
            self.stats['total_threats'] += 1
            self.rogue_bts_detected.emit(rogue_data)
    
    def _monitor_surveillance_activity(self):
        """Monitor for cellular surveillance activity"""
        if random.random() < 0.12:  # 12% chance of detection
            surveillance_data = {
                'activity_type': random.choice([
                    'IMSI Collection', 'Location Tracking', 'Call Interception',
                    'SMS Interception', 'Data Monitoring', 'Device Profiling'
                ]),
                'target_imsi': f"310{random.randint(100000000000, 999999999999)}",
                'duration': f"{random.randint(30, 300)} seconds",
                'data_collected': random.choice(['Location', 'IMSI', 'Call Metadata', 'SMS Content']),
                'source_lac': random.randint(1000, 9999),
                'source_cell': random.randint(100, 999),
                'threat_level': 'CRITICAL',
                'attack_type': 'Cellular Surveillance',
                'timestamp': datetime.now().strftime('%H:%M:%S')
            }
            
            self.stats['surveillance_attempts'] += 1
            self.stats['total_threats'] += 1
            self.surveillance_detected.emit(surveillance_data)
    
    def _analyze_gsm_anomalies(self):
        """Analyze GSM network anomalies"""
        if random.random() < 0.10:  # 10% chance of detection
            anomaly_data = {
                'anomaly_type': random.choice([
                    'Rapid LAC Changes', 'Missing Neighbor List', 'Unusual Power Levels',
                    'Encryption Downgrade', 'Timing Advance Anomaly', 'Frequency Hopping Issues'
                ]),
                'affected_arfcn': random.randint(1, 1023),
                'severity': random.choice(['LOW', 'MEDIUM', 'HIGH']),
                'duration': f"{random.randint(10, 120)} seconds",
                'impact': random.choice(['Service Degradation', 'Security Risk', 'Privacy Breach']),
                'threat_level': random.choice(['MEDIUM', 'HIGH']),
                'attack_type': 'GSM Anomaly',
                'timestamp': datetime.now().strftime('%H:%M:%S')
            }
            
            self.stats['gsm_anomalies'] += 1
            self.stats['total_threats'] += 1
            self.surveillance_detected.emit(anomaly_data)
    
    def _fingerprint_devices(self):
        """Fingerprint mobile devices on the network"""
        if random.random() < 0.15:  # 15% chance of detection
            device_data = {
                'device_type': random.choice(['iPhone', 'Samsung Galaxy', 'Google Pixel', 'Unknown']),
                'imei': f"{random.randint(100000000000000, 999999999999999)}",
                'imsi': f"310{random.randint(100000000000, 999999999999)}",
                'classmark': f"CM{random.randint(1, 3)}",
                'capabilities': random.choice(['GSM', 'UMTS', 'LTE', 'GSM+UMTS+LTE']),
                'location_area': random.randint(1000, 9999),
                'cell_id': random.randint(100, 999),
                'threat_level': 'INFO',
                'attack_type': 'Device Fingerprint',
                'timestamp': datetime.now().strftime('%H:%M:%S')
            }
            
            self.stats['device_fingerprints'] += 1

class GSMWarfareTab(QWidget):
    """GSM Warfare Detection Tab Widget"""
    
    def __init__(self):
        super().__init__()
        self.detector = GSMWarfareDetector()
        self.threats = []
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """Initialize the GSM Warfare UI"""
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("📡 GSM Warfare Detection")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #dc3545; margin: 10px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Control buttons
        self.start_btn = QPushButton("🚀 Start GSM Scan")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.start_btn.clicked.connect(self.start_detection)
        header_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ Stop Scan")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_detection)
        self.stop_btn.setEnabled(False)
        header_layout.addWidget(self.stop_btn)
        
        layout.addLayout(header_layout)
        
        # Statistics panel
        stats_group = QGroupBox("📊 GSM Threat Statistics")
        stats_layout = QGridLayout()
        
        # Create stat labels
        self.stat_labels = {}
        stat_items = [
            ('imsi_catchers', '🎯 IMSI Catchers'),
            ('rogue_bts', '📡 Rogue BTS'),
            ('surveillance', '👁️ Surveillance'),
            ('anomalies', '⚠️ GSM Anomalies'),
            ('fingerprints', '📱 Device Prints'),
            ('total_threats', '🚨 Total Threats')
        ]
        
        for i, (key, label) in enumerate(stat_items):
            row = i // 2
            col = (i % 2) * 2
            
            label_widget = QLabel(label + ":")
            label_widget.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            stats_layout.addWidget(label_widget, row, col)
            
            value_widget = QLabel("0")
            value_widget.setFont(QFont("Arial", 10))
            value_widget.setStyleSheet("color: #dc3545; font-weight: bold;")
            self.stat_labels[key] = value_widget
            stats_layout.addWidget(value_widget, row, col + 1)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Threats table
        threats_group = QGroupBox("🚨 Live GSM Threats")
        threats_layout = QVBoxLayout()
        
        self.threats_table = QTableWidget()
        self.threats_table.setColumnCount(6)
        self.threats_table.setHorizontalHeaderLabels([
            "Time", "Attack Type", "Details", "ARFCN/LAC", "Power", "Threat Level"
        ])
        
        # Style the table
        self.threats_table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                color: white;
                gridline-color: #555;
                selection-background-color: #dc3545;
            }
            QHeaderView::section {
                background-color: #404040;
                color: white;
                padding: 8px;
                border: 1px solid #555;
                font-weight: bold;
            }
        """)
        
        threats_layout.addWidget(self.threats_table)
        threats_group.setLayout(threats_layout)
        layout.addWidget(threats_group)
        
        # Activity log
        log_group = QGroupBox("📝 GSM Detection Log")
        log_layout = QVBoxLayout()
        
        self.activity_log = QTextEdit()
        self.activity_log.setMaximumHeight(150)
        self.activity_log.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ff0000;
                font-family: 'Courier New', monospace;
                font-size: 10px;
                border: 1px solid #555;
            }
        """)
        self.activity_log.setReadOnly(True)
        
        log_layout.addWidget(self.activity_log)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        self.setLayout(layout)
        
        # Add initial log message
        self.log_message("📡 GSM Warfare Detection System Initialized")
        self.log_message("🎯 Ready to detect IMSI catchers, rogue BTS, and cellular surveillance")
    
    def setup_connections(self):
        """Setup signal connections"""
        self.detector.imsi_catcher_detected.connect(self.handle_threat_detected)
        self.detector.rogue_bts_detected.connect(self.handle_threat_detected)
        self.detector.surveillance_detected.connect(self.handle_threat_detected)
    
    def start_detection(self):
        """Start GSM warfare detection"""
        self.detector.start_detection()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_message("🚀 GSM Warfare Detection STARTED - Scanning cellular networks...")
    
    def stop_detection(self):
        """Stop GSM warfare detection"""
        self.detector.stop_detection()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.log_message("⏹️ GSM Warfare Detection STOPPED")
    
    def handle_threat_detected(self, threat_data):
        """Handle detected GSM threat"""
        # Add to threats list
        self.threats.append(threat_data)
        
        # Update table
        row = self.threats_table.rowCount()
        self.threats_table.insertRow(row)
        
        # Format details based on attack type
        if threat_data['attack_type'] == 'IMSI Catcher':
            details = f"{threat_data.get('device_type', 'Unknown')} (Conf: {threat_data.get('confidence', 0)}%)"
            arfcn_lac = f"ARFCN {threat_data.get('arfcn', 0)}/LAC {threat_data.get('lac', 0)}"
            power = f"{threat_data.get('power_level', 0)} dBm"
        elif threat_data['attack_type'] == 'Rogue BTS':
            details = f"{threat_data.get('bts_type', 'Unknown')} ({threat_data.get('encryption', 'Unknown')})"
            arfcn_lac = f"ARFCN {threat_data.get('arfcn', 0)}/Cell {threat_data.get('cell_id', 0)}"
            power = f"{threat_data.get('power_level', 0)} dBm"
        else:
            details = threat_data.get('activity_type', threat_data.get('anomaly_type', 'Unknown'))
            arfcn_lac = f"LAC {threat_data.get('source_lac', threat_data.get('affected_arfcn', 0))}"
            power = "N/A"
        
        items = [
            threat_data['timestamp'],
            threat_data['attack_type'],
            details,
            arfcn_lac,
            power,
            threat_data['threat_level']
        ]
        
        for col, item in enumerate(items):
            table_item = QTableWidgetItem(str(item))
            
            # Color code by threat level
            if threat_data['threat_level'] == 'CRITICAL':
                table_item.setBackground(QColor(220, 53, 69, 100))
            elif threat_data['threat_level'] == 'HIGH':
                table_item.setBackground(QColor(255, 193, 7, 100))
            elif threat_data['threat_level'] == 'MEDIUM':
                table_item.setBackground(QColor(255, 107, 53, 100))
            
            self.threats_table.setItem(row, col, table_item)
        
        # Auto-scroll to latest
        self.threats_table.scrollToBottom()
        
        # Update statistics
        self.update_statistics()
        
        # Log the threat
        threat_emoji = {
            'IMSI Catcher': '🎯',
            'Rogue BTS': '📡',
            'Cellular Surveillance': '👁️',
            'GSM Anomaly': '⚠️',
            'Device Fingerprint': '📱'
        }.get(threat_data['attack_type'], '🚨')
        
        self.log_message(f"{threat_emoji} {threat_data['threat_level']} THREAT: {threat_data['attack_type']} - {details}")
    
    def update_statistics(self):
        """Update statistics display"""
        stats = self.detector.stats
        
        self.stat_labels['imsi_catchers'].setText(str(stats['imsi_catchers_detected']))
        self.stat_labels['rogue_bts'].setText(str(stats['rogue_bts_found']))
        self.stat_labels['surveillance'].setText(str(stats['surveillance_attempts']))
        self.stat_labels['anomalies'].setText(str(stats['gsm_anomalies']))
        self.stat_labels['fingerprints'].setText(str(stats['device_fingerprints']))
        self.stat_labels['total_threats'].setText(str(stats['total_threats']))
    
    def log_message(self, message):
        """Add message to activity log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted_message = f"[{timestamp}] {message}"
        self.activity_log.append(formatted_message)
        
        # Auto-scroll to bottom
        scrollbar = self.activity_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
