# Backtest Summary — smoke-001

Purpose: end-to-end smoke test of the QuantConnect cloud workflow (push → compile → backtest → record).

## Links
- QC: https://www.quantconnect.com/project/27861788/089fc4dfefa87203e3bb3bce05cd8abd

## Headline metrics
- Start equity: 100,000
- End equity: 101,692.55
- Net profit: 1.693%
- Max drawdown: 2.200%
- Sharpe: 8.857
- Fees: $3.68
- Total orders: 1

## Notes
- Cloud project created and compiled successfully.
- Push reported a collaboration lock warning; backtest still ran successfully.
- Next: add automated result download + richer summary generation.
