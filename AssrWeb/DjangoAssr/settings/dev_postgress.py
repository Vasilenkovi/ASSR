from DjangoAssr.settings.base import *
from dotenv import load_dotenv
import os

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
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'assr',
            'PASSWORD': '1eHPdAi918Lf7X6b',
            'HOST': 'postgres',
            'PORT': '5432',
        }
}