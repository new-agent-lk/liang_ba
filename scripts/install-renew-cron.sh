#!/bin/bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RENEW_CMD="cd $PROJECT_DIR && /bin/bash $PROJECT_DIR/scripts/renew-cert.sh"
CRON_EXPR="17 3 * * *"
CRON_LINE="$CRON_EXPR $RENEW_CMD"

TMP_FILE="$(mktemp)"
trap 'rm -f "$TMP_FILE"' EXIT

crontab -l 2>/dev/null | grep -v "scripts/renew-cert.sh" > "$TMP_FILE" || true
echo "$CRON_LINE" >> "$TMP_FILE"
crontab "$TMP_FILE"

echo "已安装证书自动续期任务:"
echo "$CRON_LINE"
