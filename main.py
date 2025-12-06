"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    Trading Dashboard - Main Entry Point                        ║
║                          نقطة الدخول الرئيسية                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
------
    python main.py              # Run dashboard
    python main.py --scan       # Run signal scan only
    python main.py --test       # Test connection
"""

import argparse
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_connection():
    """Test API connection"""
    print("🔄 Testing Alpaca API connection...")
    
    try:
        from core.data_fetcher import get_data_fetcher
        
        fetcher = get_data_fetcher()
        
        # Test market status
        market = fetcher.get_market_status()
        print(f"✅ Market Status: {'Open' if market.get('is_open') else 'Closed'}")
        
        # Test account
        account = fetcher.get_account_info()
        if account:
            print(f"✅ Account Equity: ${account['equity']:,.2f}")
            print(f"✅ Buying Power: ${account['buying_power']:,.2f}")
        
        # Test data fetch
        df = fetcher.get_historical_data('AAPL', '1day', 10)
        if df is not None:
            print(f"✅ Data Fetch: {len(df)} bars for AAPL")
            print(f"   Latest Close: ${df['close'].iloc[-1]:.2f}")
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def run_signal_scan():
    """Run signal scan and print results"""
    print("╔" + "═" * 60 + "╗")
    print("║" + " مسح الإشارات - Signal Scan ".center(60) + "║")
    print("╚" + "═" * 60 + "╝")
    print()
    
    try:
        from core.data_fetcher import get_data_fetcher
        from core.signal_generator import get_signal_generator, SignalType
        from config.settings import MONITORED_STOCKS
        
        fetcher = get_data_fetcher()
        generator = get_signal_generator()
        
        # Get high priority stocks
        priority_stocks = [s for s, info in MONITORED_STOCKS.items() if info['priority'] == 1]
        
        print(f"📊 Scanning {len(priority_stocks)} priority stocks...")
        print("─" * 60)
        
        all_signals = generator.get_all_signals(fetcher, priority_stocks, ['1day'])
        
        if not all_signals:
            print("\n⚠️ No signals found")
            return
        
        # Group by signal type
        buy_signals = [s for s in all_signals if s.signal_type == SignalType.BUY]
        sell_signals = [s for s in all_signals if s.signal_type == SignalType.SELL]
        
        print(f"\n🟢 Buy Signals: {len(buy_signals)}")
        print(f"🔴 Sell Signals: {len(sell_signals)}")
        print("─" * 60)
        
        # Print top signals
        print("\n⭐ Top Signals:")
        print("─" * 60)
        
        for signal in all_signals[:10]:
            signal_icon = "🟢" if signal.signal_type == SignalType.BUY else "🔴"
            stars = "⭐" * signal.strength
            
            print(f"""
{signal_icon} {signal.symbol} | {signal.strategy_name_ar}
   Entry: ${signal.entry_price} | SL: ${signal.stop_loss} | TP: ${signal.target_2}
   R:R: 1:{signal.risk_reward} | Strength: {stars}
   Notes: {signal.notes}
""")
        
        print("═" * 60)
        print("✅ Scan complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


def run_dashboard():
    """Run Streamlit dashboard"""
    print("╔" + "═" * 60 + "╗")
    print("║" + " 🎯 Trading Dashboard ".center(60) + "║")
    print("╚" + "═" * 60 + "╝")
    print()
    print("🚀 Starting dashboard...")
    print("📍 Open in browser: http://localhost:8501")
    print()
    print("Press Ctrl+C to stop")
    print("─" * 60)
    
    import subprocess
    dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard', 'app.py')
    subprocess.run(['streamlit', 'run', dashboard_path, '--server.headless', 'true'])


def main():
    parser = argparse.ArgumentParser(description='Trading Dashboard')
    parser.add_argument('--scan', action='store_true', help='Run signal scan only')
    parser.add_argument('--test', action='store_true', help='Test API connection')
    
    args = parser.parse_args()
    
    if args.test:
        test_connection()
    elif args.scan:
        run_signal_scan()
    else:
        run_dashboard()


if __name__ == "__main__":
    main()
