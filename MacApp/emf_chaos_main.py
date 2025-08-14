#!/usr/bin/env python3
"""
EMF Chaos Engine - Main Application Entry Point
The Viral $10-20M Warfare Suite - Native Mac App

Author: AIMF LLC - EMF Chaos Engine Team
Date: August 14, 2025
"""

import sys
import os
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from emf_chaos_window import EMFChaosMainWindow

def main():
    """Main application entry point"""
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("EMF Chaos Engine")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("AIMF LLC")
    app.setApplicationDisplayName("🚨📱 EMF Chaos Engine - Viral $10-20M Warfare Suite")
    
    # Enable high DPI scaling for Mac (PyQt6 compatible)
    try:
        app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    except AttributeError:
        # PyQt6 newer versions handle this automatically
        pass
    
    # Create and show main window
    window = EMFChaosMainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
