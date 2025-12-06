#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         Trading Dashboard Launcher                             ║
║                           مشغل داش بورد التداول                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python run.py           # Start the dashboard
    python run.py --test    # Run tests first
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check and install required packages"""
    required = [
        'streamlit',
        'pandas',
        'numpy',
        'alpaca-py',
        'ta',
    ]
    
    print("🔍 Checking dependencies...")
    
    for package in required:
        try:
            __import__(package.replace('-', '_').split('[')[0])
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  📦 Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])
            print(f"  ✅ {package} installed")
    
    print()

def run_tests():
    """Run basic tests"""
    print("🧪 Running tests...")
    
    # Test imports
    try:
        from core.data_fetcher import DataFetcher
        from core.signal_generator import SignalGenerator
        from core.risk_manager import RiskManager
        print("  ✅ Core modules imported successfully")
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        return False
    
    # Test DataFetcher
    try:
        fetcher = DataFetcher()
        market = fetcher.is_market_open()
        print(f"  ✅ DataFetcher working - Market: {'Open' if market.get('is_open') else 'Closed'}")
    except Exception as e:
        print(f"  ⚠️ DataFetcher warning: {e}")
    
    # Test SignalGenerator
    try:
        gen = SignalGenerator()
        print("  ✅ SignalGenerator initialized")
    except Exception as e:
        print(f"  ❌ SignalGenerator error: {e}")
        return False
    
    # Test RiskManager
    try:
        risk = RiskManager()
        summary = risk.get_risk_summary()
        print(f"  ✅ RiskManager working - Capital: ${summary['capital']:,}")
    except Exception as e:
        print(f"  ❌ RiskManager error: {e}")
        return False
    
    print("\n✅ All tests passed!\n")
    return True

def run_dashboard():
    """Launch the Streamlit dashboard"""
    print("🚀 Starting Trading Dashboard...")
    print("=" * 50)
    print()
    print("📊 Dashboard URL: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop")
    print()
    print("=" * 50)
    
    dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard', 'app.py')
    
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run',
        dashboard_path,
        '--server.headless', 'true',
        '--browser.gatherUsageStats', 'false',
        '--theme.base', 'dark',
        '--theme.primaryColor', '#4CAF50'
    ])

def main():
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " Trading Dashboard - داش بورد توصيات التداول ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check dependencies
    check_dependencies()
    
    # Run tests if requested
    if '--test' in sys.argv:
        if not run_tests():
            print("❌ Tests failed. Please fix errors before running.")
            sys.exit(1)
    
    # Run dashboard
    run_dashboard()

if __name__ == "__main__":
    main()
