#!/bin/bash
set -euo pipefail

COMPOSE_FILE="docker-compose.prod.yml"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$PROJECT_DIR/certbot/log"
LOG_FILE="$LOG_DIR/renew.log"
CERT_NAME="liangbax.com"
LIVE_CERT_DIR="$PROJECT_DIR/certbot/conf/live/$CERT_NAME"

mkdir -p "$LOG_DIR"

{
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始证书续期"
    cd "$PROJECT_DIR"

    docker compose -f "$COMPOSE_FILE" run --rm certbot \
        renew \
        --webroot \
        --webroot-path=/var/www/certbot \
        --quiet

    if [ ! -f "$LIVE_CERT_DIR/fullchain.pem" ] || [ ! -f "$LIVE_CERT_DIR/privkey.pem" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 续期后证书文件缺失: $LIVE_CERT_DIR"
        exit 1
    fi

    docker compose -f "$COMPOSE_FILE" exec nginx nginx -s reload
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 续期检查完成并已重载 Nginx"
} >> "$LOG_FILE" 2>&1
