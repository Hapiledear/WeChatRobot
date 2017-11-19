# -*- coding: utf-8 -*-
import os

import django
from django.conf import settings

# 外部调用django时，需要设置django相关环境变量

# 设置INSTALLED_APPS信息
INSTALLED_APPS = [
    'orm',
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',
]
# 设置数据库信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # mysql的engine
        'NAME': 'wcr',  # 数据库名称
        'USER': 'yanghuang',  # 数据库用户名
        'PASSWORD': '19951015',  # 数据库密码
        'HOST': '172.16.20.55',  # 主机地址
        'PORT': '3306',  # 数据库端口号
    }
}
# 给Django配置相关信息
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
# 启动Django
django.setup()

from django.db import models


# 构造ORM的对象
class Chats(models.Model):
    C_TYPE_CHOICES = (('1','个人'),('2',"群聊"))
    DEL_FLG_CHOICES = (('0','删除'),('1','正常'))
    id = models.CharField(primary_key=True,max_length=32)
    c_name = models.CharField(max_length=32)
    c_type = models.CharField(max_length=1,choices=C_TYPE_CHOICES)
    del_flg = models.CharField(max_length=1,choices=DEL_FLG_CHOICES,default='1')

    class Meta:
        db_table = 'chats'

    def __unicode__(self):
        return self.c_name


