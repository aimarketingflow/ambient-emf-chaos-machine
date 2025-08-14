#!/usr/bin/env python3
"""
🚨📱 EMF CHAOS ENGINE - ATTACK EXPERIMENTS LAUNCHER
The Viral $10-20M Warfare Suite - Easy Launch Interface

Quick launcher for advanced SDR attack experiments with menu selection.

AIMF LLC - EMF Chaos Engine Team
August 14, 2025
"""

import subprocess
import sys
import os

def main():
    print("🚨📱 EMF CHAOS ENGINE - ATTACK EXPERIMENTS LAUNCHER")
    print("🛡️ The Viral $10-20M Warfare Suite")
    print("⚡ Advanced SDR Attack Battery")
    print("="*60)
    
    experiments = {
        "1": ("gsm_intercept_replay", "GSM Intercept & Replay Attack"),
        "2": ("wifi_deauth_capture", "WiFi Deauth + Capture Attack"),
        "3": ("bluetooth_jam_sniff", "Bluetooth Jam & Sniff Attack"),
        "4": ("cellular_imsi_attack", "Cellular IMSI Catcher Attack"),
        "5": ("lte_downgrade_attack", "LTE Downgrade Attack"),
        "all": ("all", "🚨 RUN ALL EXPERIMENTS (Full Attack Battery)")
    }
    
    print("\n🎯 AVAILABLE ATTACK EXPERIMENTS:")
    for key, (exp_key, name) in experiments.items():
        print(f"  [{key}] {name}")
    
    print("\n⚠️  WARNING: These are REAL attack experiments!")
    print("🛡️ Only run in controlled environments with proper authorization")
    
    choice = input("\n🎯 Select experiment (1-5, 'all', or 'q' to quit): ").strip().lower()
    
    if choice == 'q':
        print("👋 Exiting attack experiments")
        return
    
    if choice not in experiments:
        print("❌ Invalid selection")
        return
    
    exp_key, name = experiments[choice]
    print(f"\n🚨 LAUNCHING: {name}")
    print("⚡ Initializing HackRF One warfare systems...")
    
    # Launch the experiment
    script_path = "/Users/flowgirl/Documents/EMF_Chaos_Engine/advanced_sdr_attack_experiments.py"
    
    if choice == "all":
        cmd = ["python3", script_path]
    else:
        cmd = ["python3", script_path, exp_key]
    
    try:
        subprocess.run(cmd, cwd="/Users/flowgirl/Documents/EMF_Chaos_Engine")
    except KeyboardInterrupt:
        print("\n🛑 Attack experiments interrupted")
    except Exception as e:
        print(f"❌ Failed to launch experiments: {e}")

if __name__ == "__main__":
    main()
