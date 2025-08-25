#!/usr/bin/env python3
"""
Enhanced GUI Launcher for Natural Language to SQL Assistant
This script launches the enhanced Streamlit application with advanced data analysis features.
"""

import os
import sys
import subprocess
import importlib.util

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'streamlit', 'pandas', 'plotly', 'numpy', 'openpyxl'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.util.find_spec(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_file_exists():
    """Check if the enhanced GUI file exists."""
    gui_file = "gui/enhanced_app.py"
    
    if not os.path.exists(gui_file):
        print(f"❌ Enhanced GUI file not found: {gui_file}")
        print("Please ensure the enhanced_app.py file exists in the gui/ directory")
        return False
    
    print(f"✅ Enhanced GUI file found: {gui_file}")
    return True

def launch_gui():
    """Launch the enhanced Streamlit GUI."""
    try:
        print("🚀 Launching Enhanced Data Analysis & SQL Assistant...")
        print("📊 Features: Interactive Visualizations • Advanced Analytics • Data Export • Statistical Analysis")
        print("🌐 Opening in your default web browser...")
        print("⏹️  Press Ctrl+C to stop the application")
        print("-" * 60)
        
        # Change to the gui directory and run streamlit
        os.chdir("gui")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "enhanced_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error launching GUI: {str(e)}")
        print("Please check the error message and try again")

def main():
    """Main function to check dependencies and launch the GUI."""
    print("=" * 60)
    print("🚀 Enhanced Data Analysis & SQL Assistant Launcher")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if GUI file exists
    if not check_file_exists():
        sys.exit(1)
    
    print("\n🎯 All checks passed! Launching enhanced GUI...")
    print("-" * 60)
    
    # Launch the GUI
    launch_gui()

if __name__ == "__main__":
    main()
