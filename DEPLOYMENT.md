# 生产环境部署指南

## 文件说明

- `Dockerfile.prod` - 生产环境 Docker 镜像（多阶段构建）
- `docker-compose.prod.yml` - 生产环境编排配置
- `.dockerignore` - Docker 构建忽略文件
- `.env.prod.example` - 环境变量模板
- `nginx/conf.d/default.conf` - Nginx 配置

## 部署步骤

### 1. 准备环境变量

```bash
# 复制环境变量模板
cp .env.prod.example .env.prod

# 编辑环境变量，修改所有敏感信息
vim .env.prod
```

**重要**: 必须修改以下配置：
- `DB_ROOT_PASSWORD` - MySQL root 密码
- `DB_PASSWORD` - 应用数据库密码
- `DJANGO_SECRET_KEY` - Django 密钥（使用 `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` 生成）
- `DJANGO_ALLOWED_HOSTS` - 允许的域名

### 2. 构建镜像

```bash
# 构建生产环境镜像
docker-compose -f docker-compose.prod.yml build

# 或者单独构建
docker build -f Dockerfile.prod -t liang_ba:prod .
```

### 3. 启动服务

```bash
# 启动所有服务
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d

# 查看服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f web
```

### 4. 初始化数据库

```bash
# 进入容器
docker-compose -f docker-compose.prod.yml exec web bash

# 运行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic --noinput

# 退出容器
exit
```

### 5. 验证部署

访问以下 URL 验证服务：
- http://localhost/ - 应用首页（通过 Nginx）
- http://localhost/admin/ - Django 管理后台
- http://localhost/health - Nginx 健康检查

### 6. 配置 HTTPS（Let's Encrypt + 自动续期）

```bash
# 1) 首次签发证书（liangbax.com + www.liangbax.com）
./init-ssl.sh

# 2) 安装自动续期 cron（每天 03:17 执行）
./scripts/install-renew-cron.sh

# 3) 手动验证一次续期流程
./scripts/renew-cert.sh
```

说明：
- 首次签发后，证书位于 `certbot/conf/live/liangbax.com/`
- 续期日志位于 `certbot/log/renew.log`
- Nginx 会在续期检查后自动 reload 以应用新证书

## 常用命令

### 服务管理

```bash
# 启动服务
docker-compose -f docker-compose.prod.yml up -d

# 停止服务
docker-compose -f docker-compose.prod.yml down

# 重启服务
docker-compose -f docker-compose.prod.yml restart

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f [service_name]
```

### 数据库管理

```bash
# 备份数据库
docker-compose -f docker-compose.prod.yml exec db mysqldump -u root -p liang_ba > backup.sql

# 恢复数据库
docker-compose -f docker-compose.prod.yml exec -T db mysql -u root -p liang_ba < backup.sql

# 进入 MySQL 命令行
docker-compose -f docker-compose.prod.yml exec db mysql -u root -p
```

### 应用更新

```bash
# 1. 拉取最新代码
git pull

# 2. 重新构建镜像
docker-compose -f docker-compose.prod.yml build web

# 3. 滚动更新（零停机）
docker-compose -f docker-compose.prod.yml up -d --no-deps --build web

# 4. 运行迁移（如果有）
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# 5. 收集静态文件（如果有更新）
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

## 性能优化

### 1. uWSGI 配置优化

编辑 `liangba.ini`：

```ini
[uwsgi]
# 工作进程数（建议 CPU 核心数 * 2 + 1）
processes = 5

# 每个进程的线程数
threads = 2

# 启用主进程
master = true

# 最大请求数后重启进程（防止内存泄漏）
max-requests = 5000

# 缓冲区大小
buffer-size = 32768

# 启用统计信息
stats = :9191

# 真空模式（退出时清理）
vacuum = true
```

### 2. 数据库连接池

在 Django settings 中配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'CONN_MAX_AGE': 600,  # 连接最大存活时间（秒）
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### 3. Redis 缓存配置

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
            },
        },
    }
}
```

## 监控和日志

### 健康检查

```bash
# 检查容器健康状态
docker-compose -f docker-compose.prod.yml ps

# 查看健康检查日志
docker inspect liang_ba_web | jq '.[0].State.Health'
```

### 日志管理

```bash
# 查看应用日志
docker-compose -f docker-compose.prod.yml logs -f --tail=100 web

# 查看 Nginx 日志
docker-compose -f docker-compose.prod.yml logs -f --tail=100 nginx

# 清理日志
docker-compose -f docker-compose.prod.yml exec web sh -c "truncate -s 0 logs/*.log"
```

## 安全建议

1. **环境变量**: 使用 `.env.prod` 管理敏感信息，不要提交到版本控制
2. **数据库密码**: 使用强密码，定期更换
3. **Django SECRET_KEY**: 生成新的密钥，不要使用默认值
4. **ALLOWED_HOSTS**: 只允许实际域名，不要使用 `*`
5. **DEBUG**: 生产环境必须设置为 `False`
6. **HTTPS**: 生产环境建议启用 HTTPS
7. **防火墙**: 只开放必要的端口（80, 443）
8. **定期更新**: 定期更新依赖包和基础镜像

## 故障排查

### 容器无法启动

```bash
# 查看容器日志
docker-compose -f docker-compose.prod.yml logs web

# 检查配置
docker-compose -f docker-compose.prod.yml config

# 进入容器调试
docker-compose -f docker-compose.prod.yml run --rm web bash
```

### 数据库连接失败

```bash
# 检查数据库容器状态
docker-compose -f docker-compose.prod.yml ps db

# 测试数据库连接
docker-compose -f docker-compose.prod.yml exec db mysql -u root -p -e "SHOW DATABASES;"

# 检查网络
docker network inspect liang_ba_liang_ba_network
```

### 静态文件无法访问

```bash
# 检查静态文件是否收集
docker-compose -f docker-compose.prod.yml exec web ls -la static/

# 重新收集静态文件
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# 检查 Nginx 配置
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

## 备份和恢复

### 完整备份

```bash
#!/bin/bash
BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# 备份数据库
docker-compose -f docker-compose.prod.yml exec -T db mysqldump -u root -p"$DB_ROOT_PASSWORD" liang_ba > $BACKUP_DIR/database.sql

# 备份媒体文件
tar -czf $BACKUP_DIR/media.tar.gz media/

# 备份日志
tar -czf $BACKUP_DIR/logs.tar.gz logs/

echo "备份完成: $BACKUP_DIR"
```

### 恢复备份

```bash
#!/bin/bash
BACKUP_DIR="./backups/20260209_120000"  # 替换为实际备份目录

# 恢复数据库
docker-compose -f docker-compose.prod.yml exec -T db mysql -u root -p"$DB_ROOT_PASSWORD" liang_ba < $BACKUP_DIR/database.sql

# 恢复媒体文件
tar -xzf $BACKUP_DIR/media.tar.gz

echo "恢复完成"
```

## 性能监控

### 安装监控工具（可选）

可以使用以下工具进行监控：
- **Prometheus + Grafana**: 指标监控
- **ELK Stack**: 日志聚合分析
- **Sentry**: 错误追踪
- **New Relic / DataDog**: APM 监控
