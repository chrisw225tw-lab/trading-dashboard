# Export trading data to JSON for dashboard
import sqlite3
import json
from datetime import datetime

DB_PATH = '/home/chris/.openclaw/workspace-buffett/trading_buffett.db'
OUTPUT_PATH = '/home/chris/.openclaw/workspace-buffett/trading-dashboard/data.json'

def export_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Get summary stats
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM decisions")
    total_decisions = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) as trades FROM trading_log WHERE action IN ('BUY', 'SELL')")
    total_trades = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) as holds FROM decisions WHERE signal='HOLD'")
    total_holds = cursor.fetchone()[0]
    
    # Get recent decisions
    cursor.execute("""
        SELECT timestamp, signal, confidence, reasoning 
        FROM decisions 
        ORDER BY timestamp DESC 
        LIMIT 50
    """)
    decisions = [dict(row) for row in cursor.fetchall()]
    
    # Get trades
    cursor.execute("""
        SELECT timestamp, action, symbol, qty, price, reason, pnl
        FROM trading_log
        ORDER BY timestamp DESC
    """)
    trades = [dict(row) for row in cursor.fetchall()]
    
    # Get latest market state
    cursor.execute("""
        SELECT timestamp, spy_price, sentiment_score, news_headline
        FROM market_state
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    latest = cursor.fetchone()
    latest_state = dict(latest) if latest else {}
    
    conn.close()
    
    data = {
        'last_updated': datetime.now().isoformat(),
        'summary': {
            'total_decisions': total_decisions,
            'total_trades': total_trades,
            'total_holds': total_holds,
            'win_rate': 0,
            'total_pnl': 0
        },
        'latest_state': latest_state,
        'recent_decisions': decisions,
        'trades': trades
    }
    
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Data exported to {OUTPUT_PATH}")

if __name__ == '__main__':
    export_data()
