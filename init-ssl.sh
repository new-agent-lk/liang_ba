#!/bin/bash
set -euo pipefail

# 获取 Let's Encrypt SSL 证书（webroot 模式，不占用宿主机 80 端口）

DOMAIN="liangbax.com"
WWW_DOMAIN="www.liangbax.com"
EMAIL="liangbax@126.com"
COMPOSE_FILE="docker-compose.prod.yml"

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "正在为 $DOMAIN 和 $WWW_DOMAIN 获取 SSL 证书..."

# 创建必要目录
mkdir -p certbot/www certbot/conf certbot/log

# 确保 nginx 运行（由 nginx 处理 /.well-known/acme-challenge/）
if ! docker compose -f "$COMPOSE_FILE" ps --status running nginx >/dev/null 2>&1; then
    echo "启动 nginx 服务..."
    docker compose -f "$COMPOSE_FILE" up -d nginx
fi

# 使用 webroot 验证，不需要绑定宿主机 80 端口
docker compose -f "$COMPOSE_FILE" run --rm certbot \
    certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email="$EMAIL" \
    --agree-tos \
    --no-eff-email \
    -d "$DOMAIN" \
    -d "$WWW_DOMAIN"

# 重载 nginx 应用新证书
docker compose -f "$COMPOSE_FILE" exec nginx nginx -s reload

echo "证书获取完成。"
echo "证书目录: certbot/conf/live/$DOMAIN/"
echo "下一步: 安装自动续期任务（scripts/renew-cert.sh + crontab）"
