#!/usr/bin/env python3
"""
Portfolio ledger for tracking trades and portfolio state.
Single source of truth: session/portfolio.json
All trades go through this module.

Colab-friendly: Uses relative paths, configurable via environment variables.
"""

import json
import csv
import os
import sys
from datetime import datetime, timezone
import traceback

# Configurable paths - defaults to local 'session' folder
DATA_DIR = os.environ.get('STOCKMONITOR_DATA_DIR', 'session')
PORTFOLIO_PATH = os.path.join(DATA_DIR, 'portfolio.json')
TRADES_PATH = os.path.join(DATA_DIR, 'trades.csv')
STARTING_CASH = 1000.0  # $1,000 starting capital

class Portfolio:
    def __init__(self):
        self.load()

    def load(self):
        """Load portfolio state from file."""
        if os.path.exists(PORTFOLIO_PATH):
            with open(PORTFOLIO_PATH, 'r') as f:
                data = json.load(f)
                self.cash = data['cash']
                self.positions = data['positions']
                self.last_prices = data.get('last_prices', {})
                self.timestamp = data.get('timestamp', datetime.now(timezone.utc).isoformat())
                self.data_mode = data.get('data_mode', 'UNKNOWN')
        else:
            # Initialize fresh portfolio
            self.cash = STARTING_CASH
            self.positions = {}
            self.last_prices = {}
            self.timestamp = datetime.now(timezone.utc).isoformat()
            self.data_mode = 'UNKNOWN'

    def save(self):
        """Save portfolio state to file."""
        os.makedirs(DATA_DIR, exist_ok=True)
        data = {
            'cash': round(self.cash, 2),
            'positions': self.positions,
            'last_prices': self.last_prices,
            'timestamp': self.timestamp,
            'data_mode': self.data_mode
        }
        with open(PORTFOLIO_PATH, 'w') as f:
            json.dump(data, f, indent=2)

    def buy(self, ticker, dollars, price, ts, reason, source):
        """
        Buy shares with specified dollar amount.

        Args:
            ticker: Stock symbol
            dollars: Dollar amount to invest
            price: Execution price per share
            ts: Timestamp ET
            reason: Reason for trade
            source: Price source (yfinance, etc.)

        Returns: shares purchased
        """
        if dollars > self.cash:
            raise ValueError(f"Insufficient cash: ${dollars} > ${self.cash:.2f}")
        if price <= 0:
            raise ValueError(f"Invalid price: ${price}")

        # Apply 0.05% adverse slippage
        effective_price = price * 1.0005
        shares = dollars / effective_price
        shares = round(shares, 6)  # Allow fractional shares

        cost = shares * effective_price
        self.cash -= cost

        if ticker in self.positions:
            # Average cost basis for existing position
            pos = self.positions[ticker]
            total_shares = pos['shares'] + shares
            total_cost = (pos['shares'] * pos['avg_cost']) + cost
            new_avg = total_cost / total_shares if total_shares > 0 else 0
            self.positions[ticker] = {
                'shares': round(total_shares, 6),
                'avg_cost': round(new_avg, 2)
            }
        else:
            self.positions[ticker] = {
                'shares': shares,
                'avg_cost': round(effective_price, 2)
            }

        self.last_prices[ticker] = round(effective_price, 2)
        self.timestamp = datetime.now(timezone.utc).isoformat()

        # Record trade
        self._record_trade(ts, ticker, 'BUY', shares, effective_price, cost, reason, source)

        self.save()
        self.reconcile()

        return shares, effective_price

    def sell(self, ticker, shares_or_all, price, ts, reason, source):
        """
        Sell shares.

        Args:
            ticker: Stock symbol
            shares_or_all: Number of shares or 'all' to sell entire position
            price: Execution price per share
            ts: Timestamp ET
            reason: Reason for trade
            source: Price source

        Returns: proceeds from sale
        """
        if ticker not in self.positions:
            raise ValueError(f"No position in {ticker}")

        pos = self.positions[ticker]
        if shares_or_all == 'all':
            shares_to_sell = pos['shares']
        else:
            shares_to_sell = float(shares_or_all)
            if shares_to_sell > pos['shares']:
                raise ValueError(f"Cannot sell {shares_to_sell} shares, only hold {pos['shares']}")

        # Apply 0.05% adverse slippage
        effective_price = price * 0.9995
        proceeds = shares_to_sell * effective_price

        # Update position
        remaining_shares = pos['shares'] - shares_to_sell
        if remaining_shares <= 0.000001:  # Near zero
            del self.positions[ticker]
            if ticker in self.last_prices:
                del self.last_prices[ticker]
        else:
            self.positions[ticker]['shares'] = round(remaining_shares, 6)
            self.last_prices[ticker] = round(effective_price, 2)

        self.cash += proceeds
        self.timestamp = datetime.now(timezone.utc).isoformat()

        # Record trade
        self._record_trade(ts, ticker, 'SELL', shares_to_sell, effective_price, proceeds, reason, source)

        self.save()
        self.reconcile()

        return proceeds, effective_price

    def _record_trade(self, ts, ticker, action, shares, price, amount, reason, source):
        """Append trade to trades.csv."""
        # Get company name for display (simplified)
        company = ticker

        # Ensure trades.csv exists with headers
        headers_exist = os.path.exists(TRADES_PATH) and os.path.getsize(TRADES_PATH) > 0
        mode = 'a' if headers_exist else 'w'

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(TRADES_PATH, mode, newline='') as f:
            writer = csv.writer(f)
            if not headers_exist:
                writer.writerow([
                    'timestamp_et', 'ticker', 'company', 'action', 'shares',
                    'price', 'dollars', 'cash_after', 'reason', 'price_source', 'data_mode'
                ])

            writer.writerow([
                ts, ticker, company, action, round(shares, 6),
                round(price, 2), round(amount, 2), round(self.cash, 2),
                reason, source, self.data_mode
            ])

    def mark(self, prices_dict):
        """
        Mark portfolio to market with current prices.

        Args:
            prices_dict: {ticker: price}

        Returns: total portfolio value
        """
        total_value = self.cash

        for ticker, pos in self.positions.items():
            price = prices_dict.get(ticker)
            if price:
                self.last_prices[ticker] = price
                position_value = pos['shares'] * price
                total_value += position_value
            elif ticker in self.last_prices:
                # Use last known price if current not available
                position_value = pos['shares'] * self.last_prices[ticker]
                total_value += position_value

        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.save()

        return round(total_value, 2)

    def reconcile(self):
        """
        Verify cash + invested cost basis = starting capital + realized P&L.
        Tolerance ≤ $0.01.

        Returns: True if passes, raises ValueError if fails
        """
        invested_cost = 0
        for pos in self.positions.values():
            invested_cost += pos['shares'] * pos['avg_cost']

        total_capital = self.cash + invested_cost

        # Read realized P&L from trades.csv
        realized_pnl = 0
        if os.path.exists(TRADES_PATH):
            with open(TRADES_PATH, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['action'] == 'BUY':
                        realized_pnl -= float(row['dollars'])
                    elif row['action'] == 'SELL':
                        realized_pnl += float(row['dollars'])

        expected = STARTING_CASH + realized_pnl
        diff = abs(total_capital - expected)

        if diff > 0.01:
            raise ValueError(
                f"Reconcile failed: ${total_capital:.2f} != ${expected:.2f} "
                f"(diff: ${diff:.2f})\n"
                f"Cash: ${self.cash:.2f}, Cost basis: ${invested_cost:.2f}\n"
                f"Starting: ${STARTING_CASH:.2f}, Realized P&L: ${realized_pnl:.2f}"
            )

        return True

    def set_data_mode(self, mode):
        """Set data mode (LIVE/DELAYED/EOD/SIMULATED)."""
        self.data_mode = mode
        self.save()

    def summary(self):
        """Return summary dict."""
        return {
            'cash': round(self.cash, 2),
            'positions': len(self.positions),
            'timestamp': self.timestamp,
            'data_mode': self.data_mode
        }

# CLI Interface
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  ledger.py buy TICKER DOLLARS PRICE TIMESTAMP REASON SOURCE")
        print("  ledger.py sell TICKER SHARES PRICE TIMESTAMP REASON SOURCE")
        print("  ledger.py mark")
        print("  ledger.py reconcile")
        print("  ledger.py summary")
        sys.exit(1)

    portfolio = Portfolio()

    try:
        if sys.argv[1] == 'buy':
            ticker = sys.argv[2]
            dollars = float(sys.argv[3])
            price = float(sys.argv[4])
            ts = sys.argv[5]
            reason = sys.argv[6]
            source = sys.argv[7]

            shares, exec_price = portfolio.buy(ticker, dollars, price, ts, reason, source)
            print(f"Bought {shares:.6f} shares of {ticker} @ ${exec_price:.2f}")
            print(f"Cash remaining: ${portfolio.cash:.2f}")

        elif sys.argv[1] == 'sell':
            ticker = sys.argv[2]
            shares = sys.argv[3]
            price = float(sys.argv[4])
            ts = sys.argv[5]
            reason = sys.argv[6]
            source = sys.argv[7]

            proceeds, exec_price = portfolio.sell(ticker, shares, price, ts, reason, source)
            print(f"Sold {shares} shares of {ticker} @ ${exec_price:.2f}")
            print(f"Proceeds: ${proceeds:.2f}, Cash now: ${portfolio.cash:.2f}")

        elif sys.argv[1] == 'mark':
            # This would need price input; for CLI, use separate script
            print("Mark requires prices_dict input; use from Python code")

        elif sys.argv[1] == 'reconcile':
            portfolio.reconcile()
            print("Reconcile PASSED")

        elif sys.argv[1] == 'summary':
            portfolio.save()
            summary = portfolio.summary()
            print(json.dumps(summary, indent=2))

        else:
            print(f"Unknown command: {sys.argv[1]}")
            sys.exit(1)

    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)