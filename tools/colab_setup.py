#!/usr/bin/env python3
"""
Google Colab Setup Script for StockMonitor
Run this in your first Colab cell to configure the environment.
"""

import os
import subprocess
import sys

def setup_colab():
    """Configure Colab environment for StockMonitor."""

    print("🔧 Setting up StockMonitor in Google Colab...")

    # 1. Install dependencies
    print("\n📦 Installing dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'yfinance', 'pandas'])

    # 2. Mount Google Drive
    print("\n💾 Mounting Google Drive...")
    try:
        from google.colab import drive
        drive.mount('/content/drive')
        print("✅ Drive mounted at /content/drive")
    except Exception as e:
        print(f"⚠️  Could not mount drive (may already be mounted): {e}")

    # 3. Set project directory
    project_dir = '/content/drive/MyDrive/StockMonitor'
    if not os.path.exists(project_dir):
        # Try to find existing project or create new
        possible_paths = [
            '/content/drive/MyDrive/StockMonitor',
            '/content/StockMonitor',
            '/content/drive/MyDrive/Colab Notebooks/StockMonitor',
        ]

        for path in possible_paths:
            if os.path.exists(path):
                project_dir = path
                break
        else:
            # Create new
            os.makedirs(project_dir, exist_ok=True)
            print(f"📁 Created new project directory: {project_dir}")

    os.chdir(project_dir)
    print(f"📂 Working directory: {os.getcwd()}")

    # 4. Set environment variable for data directory
    os.environ['STOCKMONITOR_DATA_DIR'] = os.path.join(project_dir, 'session')
    print(f"📊 Data directory: {os.environ['STOCKMONITOR_DATA_DIR']}")

    # 5. Create session directory
    os.makedirs(os.environ['STOCKMONITOR_DATA_DIR'], exist_ok=True)

    # 6. Add to Python path
    tools_dir = os.path.join(project_dir, 'tools')
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)

    print("\n✅ Colab setup complete!")
    print("\n📋 Next steps:")
    print("   1. Upload your project files to:", project_dir)
    print("   2. Import tools: from tools import ledger, quotes")
    print("   3. Run: python tools/ledger.py summary")
    print("   4. Or use in notebook: portfolio = ledger.Portfolio()")

    return project_dir

if __name__ == '__main__':
    setup_colab()