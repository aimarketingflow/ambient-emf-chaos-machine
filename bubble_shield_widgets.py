#!/usr/bin/env python3
"""
3D Directional Bubble Shield Widgets for EMF Chaos Engine
Advanced 3D visualization and directional controls for bubble shield mapping
"""

import sys
import math
import random
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QSlider, QSpinBox, QComboBox, QGroupBox, QGridLayout
)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QFont, QPalette, QColor, QPainter, QPen, QBrush

class DirectionalBubbleWidget(QWidget):
    """3D Directional Bubble Shield Map Widget"""
    
    def __init__(self):
        super().__init__()
        self.devices = []
        self.current_direction = 0  # 0-359 degrees
        self.bubble_radius = 100
        self.zoom_level = 1.0
        self.shield_active = True
        self.directional_ranges = {
            'north': 3,
            'south': 4,
            'east': 5,
            'west': 1,
            'up': 2,
            'down': 1
        }
        
        self.setMinimumSize(500, 400)
        self.setStyleSheet("""
            DirectionalBubbleWidget {
                background-color: #0a0a0a;
                border: 2px solid #00ff00;
                border-radius: 8px;
            }
        """)
        
        # Timer for real-time updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(1000)  # Update every second
        
    def update_direction(self, direction):
        """Update bubble shield direction"""
        self.current_direction = direction
        self.update()
        
    def update_range(self, direction, range_value):
        """Update range for specific direction"""
        if direction in self.directional_ranges:
            self.directional_ranges[direction] = range_value
            self.update()
            
    def update_devices(self, device_list):
        """Update device list for visualization"""
        self.devices = device_list
        self.update()
        
    def update_display(self):
        """Update display with current data"""
        self.update()
        
    def paintEvent(self, event):
        """Paint the 3D directional bubble shield map"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get widget dimensions
        width = self.width()
        height = self.height()
        center_x = width // 2
        center_y = height // 2
        
        # Draw background grid
        self.draw_background_grid(painter, width, height)
        
        # Draw bubble shield perimeter
        self.draw_bubble_shield(painter, center_x, center_y)
        
        # Draw directional indicator
        self.draw_directional_indicator(painter, center_x, center_y)
        
        # Draw detected devices
        self.draw_devices(painter, center_x, center_y)
        
        # Draw directional range indicators
        self.draw_directional_ranges(painter, center_x, center_y)
        
        # Draw shield status
        self.draw_shield_status(painter, width, height)
        
    def draw_background_grid(self, painter, width, height):
        """Draw background grid pattern"""
        painter.setPen(QPen(QColor(0, 50, 0), 1))
        
        # Vertical lines
        for x in range(0, width, 25):
            painter.drawLine(x, 0, x, height)
            
        # Horizontal lines
        for y in range(0, height, 25):
            painter.drawLine(0, y, width, y)
            
    def draw_bubble_shield(self, painter, center_x, center_y):
        """Draw the bubble shield perimeter"""
        # Outer shield boundary
        if self.shield_active:
            painter.setPen(QPen(QColor(0, 255, 0), 3))
            painter.setBrush(QBrush(QColor(0, 255, 0, 20)))
        else:
            painter.setPen(QPen(QColor(255, 0, 0), 3))
            painter.setBrush(QBrush(QColor(255, 0, 0, 20)))
            
        radius = int(self.bubble_radius * self.zoom_level)
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
        
        # Inner core zone
        painter.setPen(QPen(QColor(255, 255, 0), 2))
        core_radius = radius // 3
        painter.drawEllipse(center_x - core_radius, center_y - core_radius, core_radius * 2, core_radius * 2)
        
        # Range rings
        painter.setPen(QPen(QColor(0, 150, 0), 1))
        for ring in range(1, 4):
            ring_radius = (radius * ring) // 4
            painter.drawEllipse(center_x - ring_radius, center_y - ring_radius, ring_radius * 2, ring_radius * 2)
            
    def draw_directional_indicator(self, painter, center_x, center_y):
        """Draw directional focus indicator"""
        painter.setPen(QPen(QColor(255, 255, 0), 3))
        
        # Convert direction to radians
        angle_rad = math.radians(self.current_direction)
        
        # Draw directional arrow
        arrow_length = int(self.bubble_radius * self.zoom_level * 0.8)
        end_x = center_x + int(arrow_length * math.cos(angle_rad))
        end_y = center_y + int(arrow_length * math.sin(angle_rad))
        
        painter.drawLine(center_x, center_y, end_x, end_y)
        
        # Draw arrow head
        head_size = 10
        head_angle1 = angle_rad + math.pi * 0.8
        head_angle2 = angle_rad - math.pi * 0.8
        
        head1_x = end_x + int(head_size * math.cos(head_angle1))
        head1_y = end_y + int(head_size * math.sin(head_angle1))
        head2_x = end_x + int(head_size * math.cos(head_angle2))
        head2_y = end_y + int(head_size * math.sin(head_angle2))
        
        painter.drawLine(end_x, end_y, head1_x, head1_y)
        painter.drawLine(end_x, end_y, head2_x, head2_y)
        
        # Direction label
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.drawText(end_x + 15, end_y, f"{self.current_direction}°")
        
    def draw_devices(self, painter, center_x, center_y):
        """Draw detected devices on the map"""
        if not self.devices:
            # Generate some sample devices for visualization
            self.devices = self.generate_sample_devices()
            
        for device in self.devices:
            # Calculate device position based on zone and distance
            device_angle = self.get_zone_angle(device.get('detection_zone', 'center'))
            device_distance = device.get('distance', 5) * 8  # Scale for visualization
            
            # Add some random variation
            device_angle += random.uniform(-30, 30)
            
            # Convert to screen coordinates
            angle_rad = math.radians(device_angle)
            device_x = center_x + int(device_distance * math.cos(angle_rad))
            device_y = center_y + int(device_distance * math.sin(angle_rad))
            
            # Draw device based on threat level
            threat_level = device.get('threat_level', 'medium')
            if threat_level == 'critical':
                color = QColor(255, 0, 0)  # Red
                size = 8
            elif threat_level == 'high':
                color = QColor(255, 165, 0)  # Orange
                size = 6
            elif threat_level == 'medium':
                color = QColor(255, 255, 0)  # Yellow
                size = 5
            else:
                color = QColor(0, 255, 0)  # Green
                size = 4
                
            painter.setPen(QPen(color, 2))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(device_x - size, device_y - size, size * 2, size * 2)
            
            # Draw device info
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            device_info = f"{device.get('phone_type', 'Device')}\n{device.get('signal', -50)}dBm"
            painter.drawText(device_x + 10, device_y, device_info)
            
    def get_zone_angle(self, zone):
        """Convert zone name to angle"""
        zone_angles = {
            'north': 270,
            'south': 90,
            'east': 0,
            'west': 180,
            'center': self.current_direction
        }
        return zone_angles.get(zone, 0)
        
    def generate_sample_devices(self):
        """Generate sample devices for visualization"""
        zones = ['north', 'south', 'east', 'west', 'center']
        phone_types = ['iPhone', 'Android', 'Samsung', 'Google Pixel']
        threat_levels = ['low', 'medium', 'high', 'critical']
        
        devices = []
        for i in range(random.randint(3, 8)):
            devices.append({
                'detection_zone': random.choice(zones),
                'phone_type': random.choice(phone_types),
                'signal': random.randint(-80, -30),
                'distance': random.uniform(2, 20),
                'threat_level': random.choice(threat_levels)
            })
            
        return devices
        
    def draw_directional_ranges(self, painter, center_x, center_y):
        """Draw directional range indicators"""
        painter.setPen(QPen(QColor(255, 255, 0, 100), 2))
        
        # Direction mappings (angle in degrees)
        directions = {
            'north': 270,
            'south': 90,
            'east': 0,
            'west': 180
        }
        
        # Draw range indicators for each direction
        for direction, angle in directions.items():
            range_value = self.directional_ranges.get(direction, 25)
            range_pixels = range_value * 3  # Scale for visualization
            
            # Convert angle to radians
            angle_rad = math.radians(angle)
            
            # Calculate end point
            end_x = center_x + int(range_pixels * math.cos(angle_rad))
            end_y = center_y + int(range_pixels * math.sin(angle_rad))
            
            # Draw range line
            painter.drawLine(center_x, center_y, end_x, end_y)
            
            # Draw range arc
            painter.setPen(QPen(QColor(255, 255, 0, 80), 1))
            arc_rect = center_x - range_pixels, center_y - range_pixels, range_pixels * 2, range_pixels * 2
            painter.drawArc(*arc_rect, int((angle - 15) * 16), int(30 * 16))
            
            # Draw range label
            label_x = center_x + int((range_pixels + 20) * math.cos(angle_rad))
            label_y = center_y + int((range_pixels + 20) * math.sin(angle_rad))
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.drawText(label_x, label_y, f"{range_value}m")
            
        # Draw vertical range indicators (Up/Down)
        up_range = self.directional_ranges.get('up', 15)
        down_range = self.directional_ranges.get('down', 15)
        
        # Up indicator (smaller circle above center)
        painter.setPen(QPen(QColor(0, 255, 255, 100), 2))
        up_radius = up_range * 2
        painter.drawEllipse(center_x - up_radius//2, center_y - 50 - up_radius//2, up_radius, up_radius)
        painter.drawText(center_x - 15, center_y - 60, f"🔼{up_range}m")
        
        # Down indicator (smaller circle below center)
        down_radius = down_range * 2
        painter.drawEllipse(center_x - down_radius//2, center_y + 50 - down_radius//2, down_radius, down_radius)
        painter.drawText(center_x - 15, center_y + 80, f"🔽{down_range}m")
        
    def draw_shield_status(self, painter, width, height):
        """Draw shield status information"""
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setFont(QFont("Arial", 10))
        
        status_text = [
            f"🛡️ Bubble Shield: {'ACTIVE' if self.shield_active else 'INACTIVE'}",
            f"🎯 Direction: {self.current_direction}°",
            f"📡 Devices: {len(self.devices)}",
            f"🔍 Zoom: {self.zoom_level:.1f}x"
        ]
        
        y_offset = 20
        for text in status_text:
            painter.drawText(10, y_offset, text)
            y_offset += 20


class DirectionalControlsWidget(QWidget):
    """Directional controls for bubble shield"""
    
    direction_changed = pyqtSignal(int)
    range_changed = pyqtSignal(str, int)  # direction, range
    
    def __init__(self):
        super().__init__()
        self.ranges = {
            'north': 3,
            'south': 4,
            'east': 5,
            'west': 1,
            'up': 2,
            'down': 1
        }
        self.init_ui()
        
    def init_ui(self):
        """Initialize the directional controls UI"""
        layout = QVBoxLayout(self)
        
        # Direction control group
        direction_group = QGroupBox("🎯 Directional Controls")
        direction_layout = QGridLayout(direction_group)
        
        # Direction slider
        self.direction_slider = QSlider(Qt.Orientation.Horizontal)
        self.direction_slider.setRange(0, 359)
        self.direction_slider.setValue(0)
        self.direction_slider.valueChanged.connect(self.on_direction_changed)
        
        # Direction spinbox
        self.direction_spinbox = QSpinBox()
        self.direction_spinbox.setRange(0, 359)
        self.direction_spinbox.setSuffix("°")
        self.direction_spinbox.valueChanged.connect(self.on_direction_changed)
        
        # Direction preset buttons
        preset_buttons = [
            ("⬆️ North", 270),
            ("⬇️ South", 90),
            ("➡️ East", 0),
            ("⬅️ West", 180)
        ]
        
        direction_layout.addWidget(QLabel("Direction:"), 0, 0)
        direction_layout.addWidget(self.direction_slider, 0, 1, 1, 2)
        direction_layout.addWidget(self.direction_spinbox, 0, 3)
        
        for i, (text, angle) in enumerate(preset_buttons):
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, a=angle: self.set_direction(a))
            direction_layout.addWidget(btn, 1, i)
            
        layout.addWidget(direction_group)
        
        # 3D Range control group
        range_group = QGroupBox("📏 3D Range Controls")
        range_layout = QGridLayout(range_group)
        
        # Create range sliders for each direction
        range_directions = [
            ("⬆️ North", "north", 0, 0),
            ("⬇️ South", "south", 0, 1),
            ("➡️ East", "east", 1, 0),
            ("⬅️ West", "west", 1, 1),
            ("🔼 Up", "up", 2, 0),
            ("🔽 Down", "down", 2, 1)
        ]
        
        self.range_sliders = {}
        self.range_labels = {}
        
        for label, direction, row, col in range_directions:
            # Direction label
            dir_label = QLabel(label)
            range_layout.addWidget(dir_label, row * 2, col * 2)
            
            # Range slider
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(1, 50)  # 1m to 50m range
            slider.setValue(self.ranges[direction])
            slider.valueChanged.connect(lambda v, d=direction: self.on_range_changed(d, v))
            self.range_sliders[direction] = slider
            range_layout.addWidget(slider, row * 2, col * 2 + 1)
            
            # Range value label
            value_label = QLabel(f"{self.ranges[direction]}m")
            value_label.setStyleSheet("color: #00ff00; font-weight: bold; min-width: 40px;")
            self.range_labels[direction] = value_label
            range_layout.addWidget(value_label, row * 2 + 1, col * 2 + 1)
            
        layout.addWidget(range_group)
        
        # Shield control group
        shield_group = QGroupBox("🛡️ Shield Controls")
        shield_layout = QGridLayout(shield_group)
        
        # Shield toggle
        self.shield_toggle = QPushButton("🛡️ Shield: ACTIVE")
        self.shield_toggle.setCheckable(True)
        self.shield_toggle.setChecked(True)
        self.shield_toggle.clicked.connect(self.toggle_shield)
        
        # Zoom control
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(50, 200)
        self.zoom_slider.setValue(100)
        
        shield_layout.addWidget(self.shield_toggle, 0, 0, 1, 2)
        shield_layout.addWidget(QLabel("Zoom:"), 1, 0)
        shield_layout.addWidget(self.zoom_slider, 1, 1)
        
        layout.addWidget(shield_group)
        
        # Status group
        status_group = QGroupBox("📊 Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("🎯 Bubble Shield Ready\n📡 Scanning for devices...")
        self.status_label.setStyleSheet("color: #00ff00; font-family: monospace;")
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_group)
        
    def on_direction_changed(self, value):
        """Handle direction change"""
        # Sync slider and spinbox
        if self.sender() == self.direction_slider:
            self.direction_spinbox.setValue(value)
        else:
            self.direction_slider.setValue(value)
            
        # Emit signal
        self.direction_changed.emit(value)
        
        # Update status
        self.update_status(f"🎯 Direction: {value}°")
        
    def set_direction(self, angle):
        """Set direction to specific angle"""
        self.direction_slider.setValue(angle)
        self.direction_spinbox.setValue(angle)
        
    def toggle_shield(self):
        """Toggle shield active/inactive"""
        if self.shield_toggle.isChecked():
            self.shield_toggle.setText("🛡️ Shield: ACTIVE")
            self.update_status("🛡️ Bubble Shield ACTIVATED")
        else:
            self.shield_toggle.setText("🛡️ Shield: INACTIVE")
            self.update_status("⚠️ Bubble Shield DEACTIVATED")
            
    def on_range_changed(self, direction, value):
        """Handle range change for specific direction"""
        self.ranges[direction] = value
        self.range_labels[direction].setText(f"{value}m")
        
        # Emit signal for range change
        self.range_changed.emit(direction, value)
        
        # Update status
        direction_icons = {
            'north': '⬆️', 'south': '⬇️', 'east': '➡️', 
            'west': '⬅️', 'up': '🔼', 'down': '🔽'
        }
        icon = direction_icons.get(direction, '📏')
        self.update_status(f"{icon} {direction.title()} range: {value}m")
        
    def get_ranges(self):
        """Get current range settings"""
        return self.ranges.copy()
        
    def set_range(self, direction, value):
        """Set range for specific direction"""
        if direction in self.ranges and 1 <= value <= 50:
            self.ranges[direction] = value
            if direction in self.range_sliders:
                self.range_sliders[direction].setValue(value)
                self.range_labels[direction].setText(f"{value}m")
                
    def reset_ranges(self):
        """Reset all ranges to default"""
        defaults = {'north': 3, 'south': 4, 'east': 5, 'west': 1, 'up': 2, 'down': 1}
        for direction, value in defaults.items():
            self.set_range(direction, value)
            
    def update_status(self, message):
        """Update status display"""
        import time
        timestamp = time.strftime("%H:%M:%S")
        self.status_label.setText(f"{message}\n📡 Last update: {timestamp}")


# Test the widgets
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout
    
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("🛡️ Bubble Shield 3D Map Test")
    window.setGeometry(100, 100, 800, 600)
    
    central_widget = QWidget()
    layout = QHBoxLayout(central_widget)
    
    # Create bubble map
    bubble_map = DirectionalBubbleWidget()
    layout.addWidget(bubble_map, 2)
    
    # Create controls
    controls = DirectionalControlsWidget()
    controls.direction_changed.connect(bubble_map.update_direction)
    layout.addWidget(controls, 1)
    
    window.setCentralWidget(central_widget)
    window.show()
    
    print("🛡️ Bubble Shield 3D Map Test - Running")
    sys.exit(app.exec())
