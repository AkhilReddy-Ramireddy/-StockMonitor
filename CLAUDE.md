# StockMonitor - Paper Trading System

This is a paper trading simulation environment with real-market discipline.

## Project Overview

A hypothetical trading simulator that:
- Starts with $1,000 cash
- Runs daily trading sessions from 9:30 AM ET to 4:00 PM ET
- Trades 15 NYSE/NASDAQ common stocks (no ETFs/OTC)
- Maintains trading discipline and data honesty
- All trades are hypothetical but tracked with real-money rigor

## Key Directories

- `session/` - Trading state and logs
  - `portfolio.json` - Current portfolio state (cash, positions)
  - `trades.csv` - All executed trades
  - `log.md` - Chronological narrative log
  - `checkpoints/` - Portfolio snapshots by time
  - `DATA_AUDIT.md` - Data source verification results
  - `FINAL_REPORT.md` - End-of-day summary
- `tools/` - Core trading utilities
  - `quotes.py` - Price and news fetcher
  - `ledger.py` - Trade execution and portfolio management

## Trading Rules

### Portfolio Construction
- 15 distinct NYSE/NASDAQ common stocks
- Max 15% of capital in one name at entry
- Max 4 names in one sector
- Prefer liquid stocks (avg volume > 1M shares)
- Opening allocations sum to exactly $1,000

### Execution Rules
- Trades only between 9:30 AM ET and 4:00 PM ET
- Assume 0.05% adverse slippage on fills
- No fractional shares negative cash
- Every trade must have a reason and price source

### Data Honesty (Rule Zero)
- Never fabricate or present invented data as real
- Test data sources at start and record in DATA_AUDIT.md
- No lookahead: only use information available at logged timestamp
- Report losses as plainly as gains

## Session Flow

1. **Pre-open (9:15 AM ET)** - Data audit, news scan, pick 15 stocks
2. **Open (9:30-9:45 AM)** - Execute opening buys
3. **Mid-morning (~10:30 AM)** - First review, cut obvious losers
4. **Midday (~12:30 PM)** - Rebalance, rotate positions
5. **Power hour (~3:00 PM)** - Decide what to hold into close
6. **Close (4:00 PM)** - Mark/close all positions
7. **Wrap-up (by 5:00 PM)** - Reconcile, write FINAL_REPORT.md

## Continuous Learning Loop

The agent must maintain a continuous learning loop to improve trading accuracy:
1. **Observe**: During every checkpoint, record "Observations" in `log.md`.
2. **Categorize**: Move recurring patterns and failures into `session/learning_ledger.md`.
3. **Analyze**: For every losing trade, perform a "Thesis Failure Analysis" in the ledger.
4. **Evolve**: Update `session/agent-strategy.md` based on verified lessons from the ledger.
5. **Apply**: Tag future trades with `(informed by [Date] lesson)` to trace the learning loop.

### Resume Sessions
If `session/portfolio.json` exists, this is a RESUMED session:
- Read portfolio.json, trades.csv, and last log.md entry
- Continue from next checkpoint, do NOT restart
- State in one line: time, cash, positions, last checkpoint

### Real-time vs Replay
- If market is closed (weekend/holiday), run a labeled REPLAY using historical data
- Use [REPLAY] or [SIMULATED] disclaimer when not real-time
- For REPLAY, use historical intraday data from yfinance

### Tools Usage
- Always execute trades through `tools/ledger.py`
- Never edit portfolio.json or trades.csv by hand
- Run reconcile() after every trade and checkpoint
- Build all tools first, then start trading session

## Technical Requirements

### Data Sources
Primary: `yfinance` (tools/quotes.py)
- Returns JSON: ticker, last_price, previous_close, day_change_pct, volume, avg_volume, quote_ts, data_delay, source
- Also supports --news for headlines and --index for SPY/QQQ/^VIX

### Data Modes
Set in DATA_AUDIT.md as:
- LIVE: real quotes ≤ 15 min old
- DELAYED/EOD: real but stale data  
- SIMULATED: no real data reachable (must label [SIMULATED])

### Log Format
log.md entries:
```
## HH:MM ET | Checkpoint name | Portfolio value $X | Cash $Y | DATA_MODE
Market context: ...
Trades this cycle: (ticker, action, shares @ price, reason, source)
Observations & adjustments: ...
Reconcile: PASS/FAIL
```

### Final Report
FINAL_REPORT.md must contain:
1. DATA_MODE disclosure
2. Final portfolio value and P&L vs $1,000
3. Comparison vs SPY's daily return
4. Full trade table from trades.csv
5. Best/worst trades with reasoning
6. What worked, what didn't, patterns noticed
7. Final reconcile result

## Quality Standards

- Every price needs source and timestamp
- Every trade must have reason and price source
- Reconcile must pass after every trade (tolerance ≤ $0.01)
- Observations must trace learning: "(informed by HH:MM obs)"
- Final report must be truthful, reporting losses plainly

## Environment

- PowerShell for all shell commands (no bash syntax)
- Python available via `python`, install deps with `pip install yfinance pandas requests`
- Current ET time: `[TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([DateTime]::UtcNow,'Eastern Standard Time').ToString('yyyy-MM-dd HH:mm')`
- Working directory: project root

## Important Notes

- Built-in WebSearch/WebFetch may fail - use tools/quotes.py as primary
- Run continuously or use checkpoint system if session can't stay alive
- Make decisions, log them, keep moving - don't ask unnecessary questions
- Commit to picks, report results truthfully
- If tools cannot execute (file edits/shell commands fail), stop immediately rather than narrating fake results
