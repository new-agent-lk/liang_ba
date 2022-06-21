from .base_settings import *


#DEBUG = False
DEBUG = True

DATABASES = {
    'default': {
        'TEST_CHARSET': 'utf8',
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'liang_ba',   # 请换成新建的数据库名称
        'USER': 'root',
        'PASSWORD': 'LCJKKwti',  # 请换成自己的密码
        'HOST': '127.0.0.1',  # 如果不能连接，改成localhost
        'POST': '3306',
    }
}
