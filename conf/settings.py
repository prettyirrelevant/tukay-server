"""
Django settings for tukay project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

from environ import Env
from huey import RedisHuey
from redis import ConnectionPool

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env(DEBUG=(bool, True))

# ==============================================================================
# CORE SETTINGS
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
# ==============================================================================
DEBUG = env.bool('DEBUG')
if DEBUG:
    env.read_env(BASE_DIR / '.env.local')

SECRET_KEY = env.str('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[]) if DEBUG else env.list('ALLOWED_HOSTS')

DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
]
if DEBUG:
    DJANGO_APPS.insert(5, 'whitenoise.runserver_nostatic')

THIRD_PARTY_APPS = [
    'drf_yasg',
    'rest_framework',
    'huey.contrib.djhuey',
]

LOCAL_APPS = [
    'apps.tokens',
    'apps.accounts',
    'apps.airdrops',
    'apps.giveaways',
    'apps.crowdfunds',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

WSGI_APPLICATION = 'conf.wsgi.application'

ROOT_URLCONF = 'conf.urls'

DATA_UPLOAD_MAX_MEMORY_SIZE = 5_242_880  # 5 MB in bytes

# ==============================================================================
# MIDDLEWARE SETTINGS
# https://docs.djangoproject.com/en/4.2/topics/http/middleware/
# https://docs.djangoproject.com/en/4.2/ref/middleware/
# ==============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==============================================================================
# TEMPLATES SETTINGS
# ==============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# ==============================================================================
# STORAGES SETTINGS
# ==============================================================================
STORAGES = {'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'}}

# ==============================================================================
# DATABASES SETTINGS
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
# ==============================================================================
DATABASES = {'default': env.db('DATABASE_URL')}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# PASSWORD VALIDATION SETTINGS
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================================================
# I18N AND L10N SETTINGS
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# ==============================================================================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# ==============================================================================
# STATIC FILES SETTINGS
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# ==============================================================================
STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

# ==============================================================================
# SECURITY
# ==============================================================================
SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_HTTPONLY = True

CSRF_COOKIE_SECURE = not DEBUG

SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'DENY'

# ==============================================================================
# CACHING
# ==============================================================================
CACHES = {'default': env.cache()}

# ==============================================================================
# DJANGO REST FRAMEWORK SETTINGS
# ==============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'EXCEPTION_HANDLER': 'common.exceptions.custom_exception_handler',
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
}
if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')

# ==============================================================================
# DJANGO CORS HEADERS SETTINGS
# ==============================================================================
CORS_ALLOW_ALL_ORIGINS = True

# ==============================================================================
# HUEY SETTINGS
# ==============================================================================
connection_pool = ConnectionPool.from_url(env.str('HUEY_REDIS_URL'))
connection_pool.max_connections = env.int('HUEY_STORAGE_MAX_CONNECTIONS', default=5)
HUEY = RedisHuey(name=__name__, immediate=env.bool('HUEY_IMMEDIATE'), connection_pool=connection_pool)

# ==============================================================================
# EVM SETTINGS
# ==============================================================================
RPC_ENDPOINTS = env.list('RPC_ENDPOINTS')
AIRDROP_CONTRACT_ADDRESS = env.str('AIRDROP_CONTRACT_ADDRESS')
GIVEAWAY_CONTRACT_ADDRESS = env.str('GIVEAWAY_CONTRACT_ADDRESS')
MULTICALL_CONTRACT_ADDRESS = env.str('MULTICALL_CONTRACT_ADDRESS')
AIRDROP_CONTRACT_CREATION_BLOCK = env.int('AIRDROP_CONTRACT_CREATION_BLOCK')
GIVEAWAY_CONTRACT_CREATION_BLOCK = env.int('GIVEAWAY_CONTRACT_CREATION_BLOCK')

# ==============================================================================
# LOGGING SETTINGS
# ==============================================================================
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {'format': '[%(asctime)s] %(levelname)s:%(name)s:%(process)d:%(threadName)s: %(message)s'},
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            }
        },
        'root': {'level': 'INFO', 'handlers': ['console']},
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.security.DisallowedHost': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }
