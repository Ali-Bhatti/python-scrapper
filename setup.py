#!/usr/bin/env python3
"""
Setup script for Amazon Review Scraper
Installs dependencies and sets up the project
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    
    try:
        # Install from requirements.txt
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_installation():
    """Test if the scraper can be imported"""
    print("\nTesting installation...")
    
    try:
        import requests
        import beautifulsoup4
        import pandas
        import fake_useragent
        print("✅ All dependencies are available!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def main():
    print("Amazon Review Scraper - Setup")
    print("=" * 40)
    
    # Install dependencies
    if not install_dependencies():
        print("\nSetup failed. Please install dependencies manually:")
        print("  pip install -r requirements.txt")
        return
    
    # Test installation
    if not test_installation():
        print("\nSetup failed. Please check your Python environment.")
        return
    
    print("\n" + "=" * 40)
    print("🎉 Setup completed successfully!")
    print("\nYou can now use the scraper:")
    print("  python3 amazon_review_scraper.py B08N5WRWNW")
    print("  python3 amazon_review_scraper.py --help")
    print("\nOr run the test script:")
    print("  python3 test_scraper.py")

if __name__ == "__main__":
    main() 