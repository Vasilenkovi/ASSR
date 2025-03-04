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
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'assr'),
        'PASSWORD': os.getenv('DB_PASSWORD', '1eHPdAi918Lf7X6b'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}