#!/bin/bash
# 获取 Let's Encrypt SSL 证书

# 配置
DOMAIN="liangbax.com"
EMAIL="liangbax@126.com"

echo "正在为 $DOMAIN 获取 SSL 证书..."

# 创建必要目录
mkdir -p nginx/ssl certbot/www certbot/log

# 停止 nginx（如果正在运行）
docker-compose -f docker-compose.prod.yml stop nginx 2>/dev/null || true

# 获取证书（支持根域名和 www 子域名）
docker run --rm \
    -v $(pwd)/nginx/ssl:/etc/nginx/ssl:rw \
    -v $(pwd)/certbot/www:/var/www/certbot:rw \
    -v $(pwd)/certbot/log:/var/log/certbot:rw \
    certbot/certbot:latest \
    certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email=$EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    -d www.$DOMAIN

# 重新启动 nginx
docker-compose -f docker-compose.prod.yml start nginx

echo "证书获取完成！"
echo "证书文件位于: nginx/ssl/"
echo ""
echo "注意：证书将在 90 天后自动续期"
