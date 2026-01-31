# Quant Research Process (Guideline)

This is the default loop we follow for each project/strategy.

## 1) Define the hypothesis
- Market inefficiency or behavioral/structural hypothesis
- Expected edge: why it should persist
- Failure mode: what would falsify it

## 2) Translate into a tradable strategy
- Universe / instruments
- Signal definition (entry/exit)
- Position sizing
- Risk controls (stop rules, max exposure, leverage, drawdown guards)
- Transaction cost assumptions

## 3) Implement (Python)
- Strategy code in `MyFirstAlgo/main.py` (or a new project folder)
- Parameters are explicit and recorded per run

## 4) Cloud backtest (QC)
- Push code to QC
- Run cloud backtest with a named run id

## 5) Analyze & summarize
For each run, produce:
- `summary.md`: narrative summary
- `metrics.json`: key performance metrics
- `params.json`: parameters used
- `links.json`: QC backtest URL, commit hash, etc.

## 6) Decide next step
- Iterate parameters, refine logic, or discard
- If promising: run robustness checks (walk-forward, different regimes, cost sensitivity)

## 7) Archive
- Commit summaries to GitHub
- Sync full artifacts to OneDrive
