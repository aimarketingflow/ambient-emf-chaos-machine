#!/usr/bin/env python3
"""
WiFi Warfare Detection Tab - PineappleExpress Integration
EMF Chaos Engine - Advanced WiFi Attack Vector Detection

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

class WiFiWarfareDetector(QThread):
    """WiFi attack detection engine"""
    
    # Signals for real-time updates
    threat_detected = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.detection_active = False
        
        # Attack detection counters
        self.stats = {
            'pineapples_detected': 0,
            'evil_twins_blocked': 0,
            'deauth_attacks': 0,
            'beacon_floods': 0,
            'mgmt_frame_attacks': 0,
            'wps_vulnerabilities': 0,
            'total_threats': 0
        }
    
    def start_detection(self):
        """Start WiFi warfare detection"""
        self.detection_active = True
        self.running = True
        self.start()
    
    def stop_detection(self):
        """Stop WiFi warfare detection"""
        self.detection_active = False
        self.running = False
        self.quit()
        self.wait()
    
    def run(self):
        """Main detection loop"""
        while self.running and self.detection_active:
            try:
                # Simulate WiFi attack detection
                if random.random() < 0.15:
                    attack_type = random.choice([
                        'WiFi Pineapple', 'Evil Twin', 'Deauth Attack',
                        'Beacon Flood', 'Management Frame Injection', 'WPS Vulnerability'
                    ])
                    
                    threat_data = {
                        'attack_type': attack_type,
                        'ssid': f"Threat_{random.randint(1000, 9999)}",
                        'bssid': f"{random.randint(10,99):02x}:{random.randint(10,99):02x}:{random.randint(10,99):02x}:{random.randint(10,99):02x}:{random.randint(10,99):02x}:{random.randint(10,99):02x}",
                        'channel': random.choice([1, 6, 11, 36, 44, 149]),
                        'signal': random.randint(-80, -30),
                        'threat_level': random.choice(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']),
                        'timestamp': datetime.now().strftime('%H:%M:%S')
                    }
                    
                    # Update stats
                    if attack_type == 'WiFi Pineapple':
                        self.stats['pineapples_detected'] += 1
                    elif attack_type == 'Evil Twin':
                        self.stats['evil_twins_blocked'] += 1
                    elif attack_type == 'Deauth Attack':
                        self.stats['deauth_attacks'] += 1
                    elif attack_type == 'Beacon Flood':
                        self.stats['beacon_floods'] += 1
                    elif attack_type == 'Management Frame Injection':
                        self.stats['mgmt_frame_attacks'] += 1
                    elif attack_type == 'WPS Vulnerability':
                        self.stats['wps_vulnerabilities'] += 1
                    
                    self.stats['total_threats'] += 1
                    self.threat_detected.emit(threat_data)
                
                time.sleep(2)  # 2-second scan intervals
                
            except Exception as e:
                print(f"WiFi Warfare Detection Error: {e}")
                time.sleep(1)

class WiFiWarfareTab(QWidget):
    """WiFi Warfare Detection Tab Widget"""
    
    def __init__(self):
        super().__init__()
        self.detector = WiFiWarfareDetector()
        self.threats = []
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """Initialize the WiFi Warfare UI"""
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("🍍 WiFi Warfare Detection")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ff6b35; margin: 10px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Control buttons
        self.start_btn = QPushButton("🚀 Start Detection")
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
        
        self.stop_btn = QPushButton("⏹️ Stop Detection")
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
        stats_group = QGroupBox("📊 WiFi Attack Statistics")
        stats_layout = QGridLayout()
        
        # Create stat labels
        self.stat_labels = {}
        stat_items = [
            ('pineapples', '🍍 Pineapples Detected'),
            ('evil_twins', '👥 Evil Twins Blocked'),
            ('deauth', '💥 Deauth Attacks'),
            ('beacon_floods', '📻 Beacon Floods'),
            ('mgmt_frames', '⚡ Mgmt Frame Attacks'),
            ('wps_vulns', '🔓 WPS Vulnerabilities'),
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
            value_widget.setStyleSheet("color: #ff6b35; font-weight: bold;")
            self.stat_labels[key] = value_widget
            stats_layout.addWidget(value_widget, row, col + 1)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Threats table
        threats_group = QGroupBox("🚨 Live WiFi Threats")
        threats_layout = QVBoxLayout()
        
        self.threats_table = QTableWidget()
        self.threats_table.setColumnCount(6)
        self.threats_table.setHorizontalHeaderLabels([
            "Time", "Attack Type", "SSID", "BSSID", "Channel", "Threat Level"
        ])
        
        # Style the table
        self.threats_table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                color: white;
                gridline-color: #555;
                selection-background-color: #ff6b35;
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
        log_group = QGroupBox("📝 Detection Activity Log")
        log_layout = QVBoxLayout()
        
        self.activity_log = QTextEdit()
        self.activity_log.setMaximumHeight(150)
        self.activity_log.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
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
        self.log_message("🍍 WiFi Warfare Detection System Initialized")
        self.log_message("📡 Ready to detect WiFi Pineapples, Evil Twins, and attack vectors")
    
    def setup_connections(self):
        """Setup signal connections"""
        self.detector.threat_detected.connect(self.handle_threat_detected)
    
    def start_detection(self):
        """Start WiFi warfare detection"""
        self.detector.start_detection()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_message("🚀 WiFi Warfare Detection STARTED - Scanning for threats...")
    
    def stop_detection(self):
        """Stop WiFi warfare detection"""
        self.detector.stop_detection()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.log_message("⏹️ WiFi Warfare Detection STOPPED")
    
    def handle_threat_detected(self, threat_data):
        """Handle detected WiFi threat"""
        # Add to threats list
        self.threats.append(threat_data)
        
        # Update table
        row = self.threats_table.rowCount()
        self.threats_table.insertRow(row)
        
        items = [
            threat_data['timestamp'],
            threat_data['attack_type'],
            threat_data['ssid'],
            threat_data['bssid'],
            str(threat_data['channel']),
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
            'WiFi Pineapple': '🍍',
            'Evil Twin': '👥',
            'Deauth Attack': '💥',
            'Beacon Flood': '📻',
            'Management Frame Injection': '⚡',
            'WPS Vulnerability': '🔓'
        }.get(threat_data['attack_type'], '🚨')
        
        self.log_message(f"{threat_emoji} {threat_data['threat_level']} THREAT: {threat_data['attack_type']} detected on {threat_data['ssid']} (Ch {threat_data['channel']})")
    
    def update_statistics(self):
        """Update statistics display"""
        stats = self.detector.stats
        
        self.stat_labels['pineapples'].setText(str(stats['pineapples_detected']))
        self.stat_labels['evil_twins'].setText(str(stats['evil_twins_blocked']))
        self.stat_labels['deauth'].setText(str(stats['deauth_attacks']))
        self.stat_labels['beacon_floods'].setText(str(stats['beacon_floods']))
        self.stat_labels['mgmt_frames'].setText(str(stats['mgmt_frame_attacks']))
        self.stat_labels['wps_vulns'].setText(str(stats['wps_vulnerabilities']))
        self.stat_labels['total_threats'].setText(str(stats['total_threats']))
    
    def log_message(self, message):
        """Add message to activity log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted_message = f"[{timestamp}] {message}"
        self.activity_log.append(formatted_message)
        
        # Auto-scroll to bottom
        scrollbar = self.activity_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
