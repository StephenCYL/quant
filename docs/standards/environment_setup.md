# Environment Setup (Server + QuantConnect Cloud)

> Purpose: make this repo runnable as an end-to-end workflow:
> GitHub versioning → push/sync to QuantConnect Cloud → run cloud backtests → pull results → generate summary → archive to OneDrive.

## 0. Security rules (non‑negotiable)
- **Never commit** credentials to GitHub.
- **Never print/echo** real secret values in terminal output or logs.
- **QuantConnect token source-of-truth is the environment variable** `QC_API_TOKEN`.
  - Allowed access patterns:
    - Bash: `$QC_API_TOKEN`
    - Python: `os.getenv("QC_API_TOKEN")`
    - Node: `process.env.QC_API_TOKEN`
- Do **not** search for secrets in files, shell history, logs, or configs.
- OneDrive OAuth credentials live in: `~/.config/rclone/rclone.conf`.
- Reports are safe to commit **only as summaries** (`summary.md`, `metrics.json`, `params.json`, links). Raw large result files should be archived to OneDrive.

## 1. System prerequisites (OpenCloudOS 9 / RHEL-like)
Install base tools:
```bash
sudo dnf -y install git curl unzip jq python3-pip python3-virtualenv
```

Optional but recommended:
```bash
sudo dnf -y install pipx
pipx ensurepath
```

## 2. Install QuantConnect LEAN CLI
We currently install LEAN CLI with pip (user install):
```bash
python3 -m pip install --user --upgrade lean
export PATH="$PATH:$HOME/.local/bin"
lean --version
```

## 3. Authenticate with QuantConnect (env-var only)
We **do not paste tokens** into terminals. Authentication uses the environment variable `QC_API_TOKEN`.

Set these (example):
```bash
export QC_USER_ID="227798"
export QC_API_TOKEN="(managed by admin; do not echo)"
```

Then log in (interactive prompt reads token from stdin):
```bash
python - <<'PY'
import os, subprocess, sys
uid = os.getenv("QC_USER_ID")
tok = os.getenv("QC_API_TOKEN")
if not uid or not tok:
    print("ERROR: QC_USER_ID or QC_API_TOKEN is not set", file=sys.stderr)
    raise SystemExit(2)
subprocess.run(["lean", "login", "-u", uid], input=tok + "\n", text=True, check=True)
print("OK: logged in")
PY
```

## 4. GitHub authentication (SSH)
Generate key if needed:
```bash
ssh-keygen -t ed25519 -C "clawd-assistant" -f ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```
Add the public key to GitHub: **Settings → SSH and GPG keys**.

## 5. Create/sync a cloud project
Two ways:
- If a cloud project already exists: `lean cloud pull <projectIdOrName>` to the repo.
- If the project only exists locally: push it:

```bash
# Example
lean cloud push --project MyFirstAlgo
```

## 6. Run a cloud backtest
```bash
lean cloud backtest <projectIdOrName> --push --name "<name>" \
  --parameter key value
```

## 7. Archiving (OneDrive via rclone)
Install rclone, configure OneDrive remote, then sync:
```bash
rclone sync reports/backtests onedrive:QuantResearchBotFile/backtests \
  --checksum --transfers 4 --checkers 8
```

## 8. Repo conventions
- Standards live in `docs/standards/`.
- Backtest outputs live in `reports/backtests/`.
- Automation lives in `scripts/`.
