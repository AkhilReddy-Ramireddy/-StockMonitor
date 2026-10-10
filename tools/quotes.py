#!/usr/bin/env python3
"""
Real-time quote fetcher using yfinance.
Returns JSON: ticker, last_price, previous_close, day_change_pct, volume, avg_volume, quote_ts, data_delay, source.
Also supports --news TICKER and --index for SPY/QQQ/^VIX.

Colab-friendly: Uses relative paths, configurable via environment variables.
"""

import yfinance as yf
import json
import sys
import os
from datetime import datetime, timezone

# Configurable data directory - defaults to local 'session' folder
DATA_DIR = os.environ.get('STOCKMONITOR_DATA_DIR', 'session')

def get_quote(ticker):
    """Fetch current quote for a ticker."""
    try:
        t = yf.Ticker(ticker)

        # Try fast_info first (real-time when available)
        info = t.fast_info

        if not info or 'lastPrice' not in info:
            # Fall back to recent history
            hist = t.history(period='5d', interval='1m')
            if hist.empty:
                return {'error': f'No data for {ticker}'}

            last_row = hist.iloc[-1]
            last_price = last_row['Close']
            prev_close = info.get('previousClose', hist.iloc[0]['Close']) if info else hist.iloc[0]['Close']
        else:
            last_price = info['lastPrice']
            prev_close = info.get('previousClose', last_price)

        volume = info.get('lastVolume', 0) if info else 0
        avg_volume = info.get('averageVolume', 0) if info else 0

        day_change = last_price - prev_close
        day_change_pct = (day_change / prev_close * 100) if prev_close else 0

        now = datetime.now(timezone.utc)
        quote_ts = now.isoformat()

        return {
            'ticker': ticker,
            'last_price': round(last_price, 2),
            'previous_close': round(prev_close, 2),
            'day_change_pct': round(day_change_pct, 2),
            'volume': volume,
            'avg_volume': avg_volume,
            'quote_ts': quote_ts,
            'data_delay': '~15min',
            'source': 'yfinance'
        }
    except Exception as e:
        return {'error': f'{ticker}: {str(e)}'}

def get_news(ticker):
    """Fetch latest news headlines."""
    try:
        t = yf.Ticker(ticker)
        news = t.news if hasattr(t, 'news') else []
        if not news:
            return {'ticker': ticker, 'news': [], 'source': 'yfinance'}

        headlines = []
        for item in news[:5]:  # Last 5 headlines
            headlines.append({
                'title': item.get('title', ''),
                'link': item.get('link', ''),
                'providerPublishTime': item.get('providerPublishTime', '')
            })
        return {'ticker': ticker, 'news': headlines, 'source': 'yfinance'}
    except Exception as e:
        return {'error': f'{ticker}: {str(e)}'}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'Usage: quotes.py AAPL [MSFT ...] or --news TICKER or --index'}))
        sys.exit(1)

    if sys.argv[1] == '--news':
        result = get_news(sys.argv[2])
        print(json.dumps(result))
    elif sys.argv[1] == '--index':
        for ticker in ['SPY', 'QQQ', '^VIX']:
            result = get_quote(ticker)
            print(json.dumps(result))
    else:
        results = []
        for ticker in sys.argv[1:]:
            results.append(get_quote(ticker))
        for r in results:
            print(json.dumps(r))