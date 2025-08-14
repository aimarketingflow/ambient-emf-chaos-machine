#!/usr/bin/env python3
"""
🚨📱 SDR Hardware Monitor - HackRF One Detection & Auto-Shutdown
The Viral $10-20M Warfare Suite - Hardware Safety Module

AIMF LLC - EMF Chaos Engine Team
August 14, 2025
"""

import subprocess
import time
import threading
import json
from datetime import datetime
from pathlib import Path

class SDRHardwareMonitor:
    """Monitor SDR hardware connection and auto-shutdown on disconnect"""
    
    def __init__(self, callback_on_disconnect=None):
        self.is_monitoring = False
        self.hackrf_detected = False
        self.hackrf_serial = None
        self.monitor_thread = None
        self.callback_on_disconnect = callback_on_disconnect
        self.check_interval = 2.0  # Check every 2 seconds
        self.consecutive_failures = 0
        self.max_failures = 3  # Allow 3 consecutive failures before shutdown
        
        print("🛡️ SDR Hardware Monitor initialized")
    
    def detect_hackrf(self):
        """Detect HackRF One hardware and get serial number"""
        try:
            # Run hackrf_info to detect hardware
            result = subprocess.run(['hackrf_info'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            
            if result.returncode == 0:
                output = result.stdout
                
                # Parse serial number from output
                for line in output.split('\n'):
                    if 'Serial number:' in line:
                        self.hackrf_serial = line.split(':')[1].strip()
                        break
                
                # Check if we found valid hardware info
                if 'Found HackRF' in output and self.hackrf_serial:
                    self.hackrf_detected = True
                    self.consecutive_failures = 0
                    return True
                else:
                    self.hackrf_detected = False
                    return False
            else:
                self.hackrf_detected = False
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️ HackRF detection timeout")
            self.hackrf_detected = False
            return False
        except FileNotFoundError:
            print("❌ hackrf_info command not found - HackRF tools not installed")
            self.hackrf_detected = False
            return False
        except Exception as e:
            print(f"⚠️ HackRF detection error: {e}")
            self.hackrf_detected = False
            return False
    
    def initial_hardware_check(self):
        """Perform initial hardware check before starting app"""
        print("🔍 Performing initial SDR hardware check...")
        
        if self.detect_hackrf():
            print(f"✅ HackRF One detected - Serial: {self.hackrf_serial}")
            print("🛡️ Hardware validation passed - EMF Chaos Engine ready")
            return True
        else:
            print("❌ HackRF One not detected!")
            print("🚨 EMF Chaos Engine requires HackRF One hardware")
            print("📋 Please check:")
            print("   • HackRF One is connected via USB")
            print("   • HackRF tools are installed (hackrf_info)")
            print("   • USB permissions are correct")
            print("   • No other software is using the HackRF")
            return False
    
    def start_monitoring(self):
        """Start continuous hardware monitoring"""
        if self.is_monitoring:
            print("⚠️ Hardware monitoring already active")
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("🔄 Continuous SDR hardware monitoring started")
    
    def stop_monitoring(self):
        """Stop hardware monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        print("🛑 SDR hardware monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop running in background thread"""
        while self.is_monitoring:
            try:
                # Check if HackRF is still connected
                if not self.detect_hackrf():
                    self.consecutive_failures += 1
                    print(f"⚠️ HackRF detection failed ({self.consecutive_failures}/{self.max_failures})")
                    
                    if self.consecutive_failures >= self.max_failures:
                        print("🚨 HackRF One DISCONNECTED - Initiating emergency shutdown!")
                        self._log_disconnect_event()
                        
                        # Call disconnect callback if provided
                        if self.callback_on_disconnect:
                            self.callback_on_disconnect()
                        
                        break
                else:
                    # Reset failure counter on successful detection
                    if self.consecutive_failures > 0:
                        print(f"✅ HackRF One reconnected - Serial: {self.hackrf_serial}")
                        self.consecutive_failures = 0
                
                # Wait before next check
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"⚠️ Monitor loop error: {e}")
                time.sleep(self.check_interval)
    
    def _log_disconnect_event(self):
        """Log SDR disconnect event for debugging"""
        try:
            # Create WarfareLogs directory if it doesn't exist
            logs_dir = Path("WarfareLogs")
            logs_dir.mkdir(exist_ok=True)
            
            # Create disconnect log entry
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "event": "SDR_HARDWARE_DISCONNECT",
                "device": "HackRF One",
                "last_known_serial": self.hackrf_serial,
                "consecutive_failures": self.consecutive_failures,
                "action": "EMERGENCY_SHUTDOWN"
            }
            
            # Write to JSON log
            log_file = logs_dir / f"sdr_disconnect_{timestamp}.json"
            with open(log_file, 'w') as f:
                json.dump(log_entry, f, indent=2)
            
            print(f"📝 Disconnect event logged: {log_file}")
            
        except Exception as e:
            print(f"⚠️ Failed to log disconnect event: {e}")
    
    def get_status(self):
        """Get current hardware status"""
        return {
            "hackrf_detected": self.hackrf_detected,
            "hackrf_serial": self.hackrf_serial,
            "is_monitoring": self.is_monitoring,
            "consecutive_failures": self.consecutive_failures
        }

def test_sdr_monitor():
    """Test the SDR hardware monitor"""
    print("🚨📱 SDR Hardware Monitor Test")
    print("=" * 40)
    
    def on_disconnect():
        print("🚨 DISCONNECT CALLBACK TRIGGERED!")
        print("💀 This would normally shut down the EMF Chaos Engine")
    
    monitor = SDRHardwareMonitor(callback_on_disconnect=on_disconnect)
    
    # Test initial detection
    if monitor.initial_hardware_check():
        print("\n🔄 Starting 30-second monitoring test...")
        print("📋 Try disconnecting your HackRF One to test auto-shutdown")
        
        monitor.start_monitoring()
        
        # Monitor for 30 seconds
        for i in range(30):
            time.sleep(1)
            if i % 5 == 0:  # Status update every 5 seconds
                status = monitor.get_status()
                print(f"⏰ {30-i}s remaining | Status: {status}")
        
        monitor.stop_monitoring()
        print("✅ Monitoring test complete")
    else:
        print("❌ Initial hardware check failed - cannot start monitoring")

if __name__ == "__main__":
    test_sdr_monitor()
