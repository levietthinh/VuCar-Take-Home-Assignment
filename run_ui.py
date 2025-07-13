#!/usr/bin/env python3
"""
VuCar Web UI Runner
Simple script to start the Streamlit web interface for Vietnamese Car Value Insights
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['streamlit', 'plotly', 'pandas', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def check_data_file():
    """Check if car.xlsx data file exists"""
    if not os.path.exists('car.xlsx'):
        print("❌ car.xlsx file not found!")
        print("Please ensure the car.xlsx file is in the current directory.")
        return False
    return True

def main():
    """Main function to run the VuCar web UI"""
    print("🚗 VuCar - Vietnamese Car Value Insights")
    print("=" * 50)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        return
    
    # Check data file
    print("📊 Checking data file...")
    if not check_data_file():
        return
    
    print("✅ All checks passed!")
    print("\n🌐 Starting VuCar Web UI...")
    print("📱 The application will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("\n💡 Features available:")
    print("   • 🏷️ Price Fairness Indicator")
    print("   • 📈 Depreciation Trends")
    print("   • 📊 Market Insights")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "web_ui.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 VuCar Web UI stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting web UI: {e}")

if __name__ == "__main__":
    main() 