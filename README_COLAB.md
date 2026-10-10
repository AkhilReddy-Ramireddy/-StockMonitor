# StockMonitor in Google Colab

## Quick Start

1. **Mount your Drive** (first cell in Colab):
```python
from google.colab import drive
drive.mount('/content/drive')
```

2. **Navigate to your project folder**:
```python
%cd /content/drive/MyDrive/StockMonitor
```

3. **Install dependencies**:
```python
!pip install -q yfinance pandas
```

4. **Run the setup script** (optional but recommended):
```python
%run tools/colab_setup.py
```

## File Structure

```
StockMonitor/
├── CLAUDE.md                  # Project guidelines
├── dashboard.html             # Trading dashboard
├── README_COLAB.md            # This file
├── session/                   # Auto-generated data
│   ├── portfolio.json         # Current portfolio state
│   ├── trades.csv             # Trade history
│   ├── log.md                 # Trading log
│   ├── DATA_AUDIT.md          # Data source verification
│   ├── learning_ledger.md     # Continuous learning base
│   ├── agent-strategy.md      # Trading strategy
│   └── checkpoints/           # Portfolio snapshots
└── tools/
    ├── colab_setup.py         # Colab environment setup
    ├── colab_dashboard.py     # Dashboard display helper
    ├── quotes.py              # Price fetcher (yfinance)
    └── ledger.py              # Trade execution & tracking
```

## Usage Examples

### Initialize Portfolio
```python
%run tools/ledger.py summary
# Output: {"cash": 1000.0, "positions": 0, ...}
```

### Get Quotes
```python
%run tools/quotes.py AAPL MSFT NVDA
```

### Execute Trade
```python
# Format: ledger.py buy TICKER DOLLARS PRICE TIMESTAMP REASON SOURCE
%run tools/ledger.py buy AAPL 66.67 189.32 "09:31" "Tech momentum play" "yfinance"
```

### Display Dashboard in Colab
```python
from tools.colab_dashboard import display_dashboard
display_dashboard()  # Shows live portfolio in output cell
```

## Key Features for Colab

1. **Relative Paths**: All scripts use `STOCKMONITOR_DATA_DIR` env var
2. **Google Drive Integration**: Data persists across sessions
3. **Dashboard Display**: View portfolio in Colab output cells
4. **Continuous Learning**: `learning_ledger.md` captures insights
5. **Street-Smart Trading**: Follows the agent strategy in `agent-strategy.md`

## Notes

- The dashboard in Colab won't auto-refresh (security restriction)
- Re-run the display cell to update the view
- All trading data is saved to your Google Drive
- Ready for Monday 9:30 AM ET paper trading session