# Agent Training Strategy - Monday 2026-10-13 Trading Session

## Training Agent Profile: Street-Smart Trader

### Session Context
- **Training Date**: Friday 2026-10-10 (Post-market Close)
- **Trading Date**: Monday 2026-10-13 9:30-16:00 ET
- **Starting Capital**: $1,000 (paper trading)
- **Data Mode**: LIVE (yfinance with ~15 min delay)
- **Risk Rules**: Max 15% per position, max 4 stocks per sector

---

## Part 1: Today's Market Snapshot (Training Data)

### Current Market Conditions (2026-10-10 Close)
- **Market Status**: Closed (Friday 17:29 ET)
- **Next Session**: Monday 9:30 AM ET
- **VIX Sentiment**: Unknown (need to fetch)

### Key Holdings for Monday Pre-Open Analysis
We need to analyze these 15 liquid names for Monday:
1. AAPL (Tech - Apple)
2. MSFT (Tech - Microsoft)
3. GOOGL (Tech - Alphabet)
4. AMZN (E-commerce)
5. META (Tech - Meta)
6. NVDA (Semiconductors)
7. AMD (Semiconductors)
8. TSLA (EV/Auto)
9. F (Auto)
10. KO (Consumer Staples)
11. PG (Consumer Staples)
12. JNJ (Healthcare)
13. VZ (Telecom)
14. XOM (Energy)
15. WMT (Retail)

---

## Part 2: Training Principles (Street-Smart Method)

### The 9 Filters for Every Trade
Every trade MUST pass these filters:

1. **What happened vs. what is implied**
   - Strip the spin from headlines
   - Look for what the announcement ACTUALLY says
   - Identify what's being ignored

2. **Already priced in?**
   - Check pre-market move
   - Last 1-2 week run-up
   - Stock vs its range

3. **Reaction vs. expectation**
   - Beat that sells off = weakness
   - Miss that holds = strength
   - Tape is truth-teller

4. **Second-order winners/losers**
   - Suppliers, customers, competitors
   - Sympathy names
   - Sector rotation signals

5. **Source and incentive**
   - Primary sources only (SEC, company IR, Reuters, Bloomberg)
   - Skeptical of promotional sites

6. **The fine print**
   - Guidance beats headline EPS
   - Margins, inventory, backlog
   - Insider buying/selling

7. **Macro and flow overlay**
   - Rates, dollar, oil, VIX
   - Sector rotation patterns

8. **Pattern check**
   - Buy rumor/sell fact
   - Short squeezes
   - Overreactions to fade

9. **Verdict with conviction**
   - BUY/SELL/WATCH/IGNORE
   - Conviction 1-5
   - What proves me wrong?
   - Exit level

---

## Part 3: Monday Morning Scripts (Pre-Approved Trade Patterns)

### Script 1: Monday Pre-Market Momentum Play
**Entry**: If SPY up >0.5% pre-market and QQQ up >1%
**Tactics**:
- Buy NVDA or AMD (semiconductors)
- Size: $150 max
- Stop: -3% from entry
- Thesis: Tech momentum continuation

### Script 2: Contrarian Weakness Buy
**Entry**: If any of AAPL/MSFT/GOOGL down >1.5% pre-market despite strong market
**Tactics**:
- Buy the dip on big tech
- Size: $100 max
- Stop: -2.5% from entry
- Thesis: Market overreacting, buy the quality discount

### Script 3: Sector Rotation Switch
**Entry**: If Energy (XOM) up >1% while Tech flat
**Tactics**:
- Rotate from underperforming tech to energy
- Sell weakest tech position, buy XOM
- Size: $100 move
- Thesis: Sector rotation in play

### Script 4: Earnings Reaction Fade
**Entry**: If any stock gapped up >3% on earnings
**Tactics**:
- WAIT 15 minutes
- If volume spikes but price drifts down: SELL THE NEWS
- Take profit at +1.5%
- Thesis: Buy rumor, sell fact

### Script 5: VIX Spike Opportunity
**Entry**: If VIX up >5% pre-market
**Tactics**:
- Avoid high-beta plays
- Focus on quality (JNJ, KO, PG)
- Size: $100 max
- Thesis: Defensive rotation

---

## Part 4: Risk Management Framework

### Position Sizing
- Max per position: $150 (15% of $1,000)
- Recommended entry: $66-100 per trade
- Leave cash reserve: $200-300 for intraday opportunities

### Stop Loss Rules
- Cut losers at -2.5% to -3% max
- No averaging down
- If stopped out twice in same name, walk away for the day

### Profit Taking
- Take partial profits at +2% (sell 50% of position)
- Move stop to breakeven
- Let remainder run to +5%

### Rotation Logic
1. Identify weakest position (largest loss OR no momentum)
2. Identify strongest idea in watchlist
3. Rotate capital with 1-2 line thesis comparison
4. Log rotation reason for learning

---

## Part 5: Monday 9:00 AM Checklist

### 30 Minutes Before Open (8:30-9:00 AM)
1. Fetch quotes for all 15 candidates
2. Check SPY/QQQ/VIX pre-market levels
3. Scan for overnight news (via yfinance news)
4. Identify top 3 opportunities
5. Write 3-5 Read-Between-the-Lines memos

### First 15 Minutes Open (9:30-9:45 AM)
1. Watch price action vs. expectations
2. Execute opening buys (max 8 positions)
3. Set alerts for entry/stop levels
4. Log fills and slippage

### Mid-Morning Check (10:30 AM)
1. Review all positions
2. Cut any that are broken (-2.5% or worse)
3. Add to momentum winners
4. Log observations

### Midday Review (12:30 PM)
1. Rebalance if sector rotation visible
2. Rotate from weak to strong ideas
3. Take profits on winners
4. Fresh news scan

### Power Hour (3:00 PM)
1. Decide what to hold vs. close
2. Check late headlines
3. Lock in profits

### Close (4:00 PM)
1. Mark all positions to market
2. Close or hold for next session
3. Write observations for learning

---

## Part 6: Success Metrics

### What Success Looks Like
1. **All trades have written thesis** (one line, before entry)
2. **Reconcile passes** after every trade
3. **Position sizes respected** (no >15% per position)
4. **Losses cut fast** (no hope/ hold broken thesis)
5. **Learning logged** (observations with teachable moments)

### What Failure Looks Like
1. Trading off headlines without verification
2. Averaging down on losers
3. Holding positions with broken thesis
4. Missing reconcile checks
5. Not logging observations

---

## Part 7: Key Reminders

### Data Honesty
- Every trade: price source + timestamp
- Every thesis: written before entry
- Every loss: logged plainly
- No backfilling prices
- If data fails: stop, don't guess

### Mental Game
- Don't fall in love with positions
- The tape is the truth-teller
- Volume confirms moves
- News is noise without price action
- Second-order thinking beats headline trading

### Final Goal
End Monday with:
- Clean trade log with reasons
- Reconciled portfolio
- Clear learning from tape
- Plan for Tuesday

## Part 8: Continuous Learning Loop

The agent does not just trade; it evolves. Every session must contribute to the `session/learning_ledger.md`.

### The Learning Cycle
1. **The Tape Check**: At every checkpoint, ask: "Did the price do what the headline said it should?"
2. **The Pattern Log**: If a specific behavior repeats (e.g., a "gap and crap" open), record it in the Pattern Recognition table of the ledger.
3. **The Autopsy**: Every losing trade requires a Thesis Failure Analysis.
   - *Thesis* $\rightarrow$ *Reality* $\rightarrow$ *The Gap* $\rightarrow$ *Corrective Action*.
4. **Strategy Pivot**: When a pattern is verified 3+ times, update the Monday Morning Scripts in this document to reflect the new truth.

### Learning Metrics
- **Thesis Accuracy**: % of trades where the price action matched the original thesis.
- **Recovery Rate**: How quickly the agent identifies a broken thesis and cuts the loss.
- **Insight Density**: Number of verified "Street-Smart Insights" added to the ledger per session.
