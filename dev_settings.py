from myproject.settings import *

# Переопределите настройки БД
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testdb',
        'USER': 'postgres',
        'PASSWORD': '123456',  # ваш пароль
        'HOST': 'localhost',
        'PORT': '5432',
    }
}