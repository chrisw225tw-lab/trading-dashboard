import sqlite3
import json
import urllib.request
from datetime import datetime

# Supabase config
SUPABASE_URL = 'https://gfulzxjfgdfmkkuzktil.supabase.co'
SUPABASE_KEY = 'sb_publishable_iLopC9XI5S5vfZoiJrW-ag_HWl3Ysuh'
DB_PATH = '/home/chris/.openclaw/workspace-buffett/trading_buffett.db'

def supabase_request(method, endpoint, data=None):
    """Make request to Supabase REST API"""
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode() if data else None,
        headers=headers,
        method=method
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

def sync_decisions():
    """Sync SQLite decisions to Supabase"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get recent decisions
    cursor.execute("""
        SELECT timestamp, signal, confidence, reasoning 
        FROM decisions 
        ORDER BY timestamp DESC 
        LIMIT 100
    """)
    
    rows = cursor.fetchall()
    
    for row in rows:
        data = {
            'timestamp': row['timestamp'],
            'signal': row['signal'],
            'confidence': row['confidence'],
            'reasoning': row['reasoning'][:500] if row['reasoning'] else None
        }
        
        # Upsert to Supabase
        status, response = supabase_request('POST', 'decisions', data)
        if status >= 400:
            print(f"Error inserting {data['timestamp']}: {response}")
    
    conn.close()
    print(f"Synced {len(rows)} decisions to Supabase")

def sync_trades():
    """Sync trading log to Supabase"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT timestamp, action, symbol, qty, price, reason, pnl
        FROM trading_log
        ORDER BY timestamp DESC
    """)
    
    rows = cursor.fetchall()
    
    for row in rows:
        data = {
            'timestamp': row['timestamp'],
            'action': row['action'],
            'symbol': row['symbol'],
            'qty': row['qty'],
            'price': row['price'],
            'reason': row['reason'][:500] if row['reason'] else None,
            'pnl': row['pnl']
        }
        
        status, response = supabase_request('POST', 'trades', data)
        if status >= 400:
            print(f"Error inserting trade: {response}")
    
    conn.close()
    print(f"Synced {len(rows)} trades to Supabase")

if __name__ == '__main__':
    print("Syncing data to Supabase...")
    sync_decisions()
    sync_trades()
    print("Done!")
