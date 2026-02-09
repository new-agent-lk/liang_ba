from base_settings import *
import os

# 生产环境设置 - 从环境变量读取配置

# 安全设置
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('true', '1', 'yes')

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY must be set in production")

ALLOWED_HOSTS = ['.liangbax.com', 'localhost', '127.0.0.1'] + os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'liang_ba'),
        'USER': os.getenv('DB_USER', 'liang_ba_user'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'CONN_MAX_AGE': int(os.getenv('CONN_MAX_AGE', '60')),
    }
}

# Redis 缓存配置
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_DB = int(os.getenv('REDIS_DB', '0'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{":" + REDIS_PASSWORD + "@" if REDIS_PASSWORD else ""}{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
            },
        },
        'KEY_PREFIX': 'LB',
    }
}

# 时区设置
TIME_ZONE = os.getenv('TZ', 'Asia/Shanghai')
USE_TZ = os.getenv('USE_TZ', 'True').lower() in ('true', '1', 'yes')

# 日志级别
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# 安全配置（生产环境）
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False').lower() in ('true', '1', 'yes')

# Wagtail
WAGTAILADMIN_BASE_URL = os.getenv('WAGTAILADMIN_BASE_URL', '/manage/')

# 文件上传限制
DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv('DATA_UPLOAD_MAX_MEMORY_SIZE', 104857600))  # 100MB
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv('FILE_UPLOAD_MAX_MEMORY_SIZE', 52428800))  # 50MB
