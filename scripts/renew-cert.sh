#!/bin/bash
set -euo pipefail

COMPOSE_FILE="docker-compose.prod.yml"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$PROJECT_DIR/certbot/log"
LOG_FILE="$LOG_DIR/renew.log"

mkdir -p "$LOG_DIR"

{
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始证书续期"
    cd "$PROJECT_DIR"

    docker compose -f "$COMPOSE_FILE" run --rm certbot \
        renew \
        --webroot \
        --webroot-path=/var/www/certbot \
        --quiet

    docker compose -f "$COMPOSE_FILE" exec nginx nginx -s reload
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 续期检查完成并已重载 Nginx"
} >> "$LOG_FILE" 2>&1
