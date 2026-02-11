-- Create tables for Agent Buffett trading logs
-- Run this in Supabase SQL Editor: https://gfulzxjfgdfmkkuzktil.supabase.co/project/sql

-- 1. Decisions table (all trading decisions)
CREATE TABLE IF NOT EXISTS decisions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    signal VARCHAR(10) NOT NULL CHECK (signal IN ('BUY', 'SELL', 'HOLD')),
    confidence INTEGER CHECK (confidence >= 0 AND confidence <= 100),
    reasoning TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Trades table (executed trades only)
CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    action VARCHAR(10) NOT NULL CHECK (action IN ('BUY', 'SELL')),
    symbol VARCHAR(10) DEFAULT 'SPY',
    qty INTEGER,
    price DECIMAL(10,2),
    reason TEXT,
    pnl DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Market snapshots table (price/sentiment history)
CREATE TABLE IF NOT EXISTS market_snapshots (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    spy_price DECIMAL(10,2),
    sentiment_score INTEGER CHECK (sentiment_score >= 0 AND sentiment_score <= 100),
    news_headline TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security (RLS) - recommended for production
ALTER TABLE decisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE trades ENABLE ROW LEVEL SECURITY;
ALTER TABLE market_snapshots ENABLE ROW LEVEL SECURITY;

-- Create policies to allow all operations (for development)
-- You can restrict this later for security
CREATE POLICY "Enable all operations" ON decisions
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Enable all operations" ON trades
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Enable all operations" ON market_snapshots
    FOR ALL USING (true) WITH CHECK (true);

-- Create indexes for faster queries
CREATE INDEX idx_decisions_timestamp ON decisions(timestamp DESC);
CREATE INDEX idx_trades_timestamp ON trades(timestamp DESC);
CREATE INDEX idx_snapshots_timestamp ON market_snapshots(timestamp DESC);

-- Verify tables created
SELECT 'Tables created successfully!' as status;
