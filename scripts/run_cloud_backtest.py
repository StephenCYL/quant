#!/usr/bin/env python3
"""Run a QuantConnect cloud backtest and archive a record.

This script is intentionally conservative: it shells out to `lean`.
Later we can extend it to parse results and compute extra stats.

Usage (example):
  python scripts/run_cloud_backtest.py --project MyFirstAlgo --name "test-001" \
    --param symbol=AAPL --param period=20
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def ensure_qc_login() -> None:
    """Log in to QuantConnect using env vars only.

    Required env vars:
      - QC_USER_ID
      - QC_API_TOKEN

    We send the token through stdin to avoid leaking it via process args.
    """
    uid = os.getenv("QC_USER_ID")
    tok = os.getenv("QC_API_TOKEN")
    if not uid or not tok:
        raise SystemExit("ERROR: QC_USER_ID or QC_API_TOKEN is not set")

    subprocess.run(["lean", "login", "-u", uid], input=tok + "\n", text=True, check=True)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--project", required=True, help="QC project name or id")
    p.add_argument("--name", required=True, help="Backtest name")
    p.add_argument("--push", action="store_true", default=True, help="Push before backtest")
    p.add_argument("--param", action="append", default=[], help="key=value pairs")
    args = p.parse_args()

    params = {}
    for kv in args.param:
        if "=" not in kv:
            raise SystemExit(f"Bad --param {kv!r}, expected key=value")
        k, v = kv.split("=", 1)
        # keep as string; QC CLI supports int/float too, can add parsing later
        params[k] = v

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = Path("reports/backtests") / ts / args.project / args.name
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "params.json").write_text(json.dumps(params, indent=2, ensure_ascii=False) + "\n")
    (out_dir / "meta.json").write_text(json.dumps({
        "project": args.project,
        "name": args.name,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }, indent=2, ensure_ascii=False) + "\n")

    # Always authenticate from env vars (do not rely on stored tokens)
    ensure_qc_login()

    cmd = ["lean", "cloud", "backtest", args.project, "--name", args.name]
    if args.push:
        cmd.append("--push")
    for k, v in params.items():
        cmd += ["--parameter", k, str(v)]

    # Save a reproducible command line
    (out_dir / "command.txt").write_text(" ".join(cmd) + "\n")

    # Run
    run(cmd)

    # Placeholder summary; later we'll pull results and fill metrics
    (out_dir / "summary.md").write_text(
        f"# Backtest Summary\n\n- Project: {args.project}\n- Name: {args.name}\n- UTC: {datetime.now(timezone.utc).isoformat()}\n\n> Results: (TODO)\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
