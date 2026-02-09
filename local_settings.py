from base_settings import *

DEBUG = True

DATABASES = {
    'default': {
        'TEST_CHARSET': 'utf8',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'liang_ba',   # 请换成新建的数据库名称
        'USER': 'root',
        'PASSWORD': 'Kang0716.',  # 请换成自己的密码
        'HOST': '172.18.4.63',  # 如果不能连接，改成localhost
        'POST': 3306,
    }
}

CACHES = {
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:redis_rjmzX6@172.18.4.63:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        'KEY_PREFIX': 'LB-'
    }
}

WAGTAILADMIN_BASE_URL = 'http://172.18.4.63:9999'

