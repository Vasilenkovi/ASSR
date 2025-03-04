from DjangoAssr.settings.base import *
import os
ALLOWED_HOSTS = ["*"]

# Загрузка переменных окружения из .env

DEBUG = True

    
# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'ATOMIC_REQUESTS': True
    }
}
