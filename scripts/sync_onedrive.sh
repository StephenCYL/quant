#!/usr/bin/env bash
set -euo pipefail

# Requires rclone remote named "onedrive".
# Target root: QuantResearchBotFile/

rclone sync reports/backtests "onedrive:QuantResearchBotFile/backtests" \
  --checksum --transfers 4 --checkers 8
