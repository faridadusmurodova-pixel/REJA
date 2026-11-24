"""
REJA - Django sozlamalari (soz.py).
Mavzular: Django, Deploy, PostgreSQL, SQLite, REST API.
"""
from pathlib import Path
import os

ASOSIY_PAPKA = Path(__file__).resolve().parent.parent
BASE_DIR = ASOSIY_PAPKA

MAXFIY_KALIT = 'reja-maxfiy-kalit-2026-xavfsiz'
SECRET_KEY = MAXFIY_KALIT

DEBUG = True
ALLOWED_HOSTS = ['*']

# O'rnatilgan ilovalar
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'ilova.apps.IlovaConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'reja.yol'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ASOSIY_PAPKA / 'qolip'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'reja.wsgi.application'
ASGI_APPLICATION = 'reja.asgi.application'

# 19. Python SQLite va PostgreSQL sozlamalari
# Agar atrof-muhitda POSTGRES_DB mavjud bo'lsa PostgreSQL ishlatiladi, aks holda tezkor SQLite
POSTGRES_DB = os.environ.get('POSTGRES_DB')

if POSTGRES_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': POSTGRES_DB,
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
            'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ASOSIY_PAPKA / 'baza.sqlite3',
        }
    }

# Maxsus foydalanuvchi modeli (Ism, Familiya, Yosh)
AUTH_USER_MODEL = 'ilova.Foydalanuvchi'

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# Statik fayllar
STATIC_URL = '/statik/'
STATICFILES_DIRS = [ASOSIY_PAPKA / 'statik']
STATIC_ROOT = ASOSIY_PAPKA / 'statik_yigilgan'

MEDIA_URL = '/media/'
MEDIA_ROOT = ASOSIY_PAPKA / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/kirish/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/kirish/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
