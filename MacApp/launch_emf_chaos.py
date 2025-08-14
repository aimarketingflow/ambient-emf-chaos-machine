#!/usr/bin/env python3
"""
EMF Chaos Engine - Mac App Launcher
Quick launcher with dependency checking and virtual environment setup

Author: AIMF LLC - EMF Chaos Engine Team
Date: August 14, 2025
"""

import sys
import os
import subprocess
from pathlib import Path

def check_pyqt6():
    """Check if PyQt6 is installed"""
    try:
        import PyQt6
        print("✅ PyQt6 is installed")
        return True
    except ImportError:
        print("❌ PyQt6 not found")
        return False

def install_pyqt6():
    """Install PyQt6 using pip3"""
    print("🔧 Installing PyQt6...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6"], check=True)
        print("✅ PyQt6 installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install PyQt6")
        return False

def create_venv():
    """Create virtual environment for EMF Chaos Engine"""
    venv_path = Path(__file__).parent / "emf_chaos_venv"
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return str(venv_path)
    
    print("🔧 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("✅ Virtual environment created")
        return str(venv_path)
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return None

def activate_venv_and_install(venv_path):
    """Activate venv and install dependencies"""
    if sys.platform == "darwin":  # macOS
        pip_path = Path(venv_path) / "bin" / "pip3"
        python_path = Path(venv_path) / "bin" / "python3"
    else:
        pip_path = Path(venv_path) / "Scripts" / "pip.exe"
        python_path = Path(venv_path) / "Scripts" / "python.exe"
    
    print("🔧 Installing PyQt6 in virtual environment...")
    try:
        subprocess.run([str(pip_path), "install", "PyQt6"], check=True)
        print("✅ PyQt6 installed in virtual environment")
        return str(python_path)
    except subprocess.CalledProcessError:
        print("❌ Failed to install PyQt6 in virtual environment")
        return None

def launch_app(python_path=None):
    """Launch the EMF Chaos Engine app"""
    app_path = Path(__file__).parent / "emf_chaos_main.py"
    
    if python_path:
        cmd = [python_path, str(app_path)]
    else:
        cmd = [sys.executable, str(app_path)]
    
    print("🚀 Launching EMF Chaos Engine...")
    print(f"🎯 Command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch app: {e}")
    except KeyboardInterrupt:
        print("\n🛑 App terminated by user")

def main():
    """Main launcher function"""
    print("🚨📱 EMF CHAOS ENGINE - MAC APP LAUNCHER")
    print("=" * 50)
    print("🛡️ The Viral $10-20M Warfare Suite")
    print("🔥 What a fucking week!")
    print()
    
    # Check if PyQt6 is available
    if check_pyqt6():
        # PyQt6 is available, launch directly
        launch_app()
    else:
        print("🔧 PyQt6 not found. Setting up virtual environment...")
        
        # Create virtual environment
        venv_path = create_venv()
        if not venv_path:
            print("❌ Cannot create virtual environment. Trying system install...")
            if install_pyqt6():
                launch_app()
            else:
                print("❌ Cannot install PyQt6. Please install manually:")
                print("   pip3 install PyQt6")
                sys.exit(1)
        else:
            # Install in venv and launch
            python_path = activate_venv_and_install(venv_path)
            if python_path:
                launch_app(python_path)
            else:
                print("❌ Setup failed. Please install PyQt6 manually:")
                print("   pip3 install PyQt6")
                sys.exit(1)

if __name__ == "__main__":
    main()
