import urllib.request
import json

SUPABASE_URL = 'https://gfulzxjfgdfmkkuzktil.supabase.co'
SUPABASE_KEY = 'sb_publishable_iLopC9XI5S5vfZoiJrW-ag_HWl3Ysuh'

def create_tables():
    """Create tables in Supabase using REST API"""
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Note: Creating tables requires Supabase dashboard or SQL editor
    # This script will just check if tables exist by trying to query them
    
    endpoints = ['decisions', 'trades', 'market_snapshots']
    
    for endpoint in endpoints:
        url = f"{SUPABASE_URL}/rest/v1/{endpoint}?limit=1"
        req = urllib.request.Request(url, headers=headers, method='GET')
        
        try:
            with urllib.request.urlopen(req) as resp:
                print(f"✅ Table '{endpoint}' exists")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"❌ Table '{endpoint}' does not exist. Please create it in Supabase dashboard.")
                print(f"   SQL: CREATE TABLE {endpoint} (id serial PRIMARY KEY, ...);")
            else:
                print(f"⚠️  Error checking {endpoint}: {e.code}")

if __name__ == '__main__':
    print("Checking Supabase tables...")
    print(f"URL: {SUPABASE_URL}")
    print()
    create_tables()
