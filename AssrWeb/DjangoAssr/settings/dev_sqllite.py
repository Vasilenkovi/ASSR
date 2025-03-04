from DjangoAssr.settings.base import *
from dotenv import load_dotenv
import os
ALLOWED_HOSTS = ["*"]

# Загрузка переменных окружения из .env
load_dotenv()

if os.environ.get('DJANGO_DEBUG'):
    DEBUG = True
    # When not specified, ALLOW_HOSTS defaults to:
    # ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
else:
    DEBUG = False
    ALLOWED_HOSTS = ["*"]
    
# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'ATOMIC_REQUESTS': True
    }
}
