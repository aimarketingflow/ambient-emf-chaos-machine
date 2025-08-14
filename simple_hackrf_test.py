#!/usr/bin/env python3
"""
Simple HackRF One Detection Test
Direct test to verify HackRF One connectivity
"""

import subprocess
import sys

def test_hackrf_detection():
    """Test HackRF One detection with different methods"""
    
    print("🚨📱 Simple HackRF One Detection Test")
    print("=" * 50)
    
    # Test 1: Basic hackrf_info
    print("\n🔍 Test 1: Basic hackrf_info")
    try:
        result = subprocess.run(['hackrf_info'], capture_output=True, text=True, timeout=10)
        print(f"Exit code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        
        if 'Found HackRF' in result.stdout:
            print("✅ HackRF One FOUND!")
            if 'Access denied' in result.stdout:
                print("⚠️ Permission issue detected")
                return test_with_sudo()
            else:
                print("✅ HackRF One accessible without sudo")
                return True
        else:
            print("❌ HackRF One not found")
            
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
    
    # Test 2: Check USB devices
    print("\n🔍 Test 2: USB device check")
    try:
        result = subprocess.run(['system_profiler', 'SPUSBDataType'], capture_output=True, text=True, timeout=10)
        if 'HackRF' in result.stdout or '1d50' in result.stdout:
            print("✅ HackRF USB device found in system profiler")
        else:
            print("❌ No HackRF USB device found")
            print("First few USB devices:")
            lines = result.stdout.split('\n')[:20]
            for line in lines:
                if 'Product ID' in line or 'Vendor ID' in line:
                    print(f"  {line.strip()}")
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
    
    return False

def test_with_sudo():
    """Test HackRF with sudo permissions"""
    print("\n🔍 Test 3: hackrf_info with sudo")
    try:
        result = subprocess.run(['sudo', 'hackrf_info'], capture_output=True, text=True, timeout=15)
        print(f"Exit code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        
        if result.returncode == 0 and 'Board ID Number' in result.stdout:
            print("✅ HackRF One accessible with sudo!")
            return True
        else:
            print("❌ HackRF One not accessible even with sudo")
            
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
    
    return False

if __name__ == "__main__":
    success = test_hackrf_detection()
    
    if success:
        print("\n🎯 RESULT: HackRF One is READY for live GSM detection!")
    else:
        print("\n❌ RESULT: HackRF One not available - using simulation mode")
        print("\n💡 TROUBLESHOOTING:")
        print("1. Check USB connection")
        print("2. Try unplugging and reconnecting HackRF One")
        print("3. Check if another application is using the device")
        print("4. Verify HackRF One drivers are installed")
