import os
import sys
import platform
import djcelery

# Heroku Specific
# Load in .env file if not in heroku
heroku_env = os.environ.get('USE_HEROKU', 'false')
if not heroku_env == 'true':
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

from django.contrib.messages import constants as messages

# ===========================
# = Directory Declaractions =
# ===========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_DIR   = os.path.dirname(__file__)
UTIL_ROOT    = os.path.join(CURRENT_DIR, 'util')
APPS_ROOT    = os.path.join(CURRENT_DIR, 'apps')
VENDOR_ROOT   = os.path.join(CURRENT_DIR, 'vendor')

if '/util' not in ' '.join(sys.path):
    sys.path.append(UTIL_ROOT)

if '/vendor' not in ' '.join(sys.path):
    sys.path.append(VENDOR_ROOT)

if '/apps' not in ' '.join(sys.path):
    sys.path.append(APPS_ROOT)

DEBUG = True
ENABLE_CACHE = False
ENABLE_S3 = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
	'alifewellplayed.com', '*.alifewellplayed.com',
    'alifewellplayed.net', '*.alifewellplayed.net',
    'alifewellplayed.org', '*.alifewellplayed.org',
	'alifewellplayed.herokuapp.com',
]

ADMINS = (('Tyler Rilling', 'tyler@alifewellplayed.com'))
MANAGERS = ADMINS

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', ''),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', ''),
    }
}
#DB info injected by Heroku
if heroku_env:
    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

#Cache
if ENABLE_CACHE:
    import urlparse
    redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
    CACHES = {
            'default': {
                'BACKEND': 'redis_cache.RedisCache',
                'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
                'OPTIONS': {
                    'PASSWORD': redis_url.password,
                    'DB': 0,
            }
        },
        "staticfiles": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "TIMEOUT": 60 * 60 * 24 * 365,
            "LOCATION": "static",
        },
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }


# ====================
# = #Global Settings =
# ====================

BROKER_HOST = "localhost"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = "25"
#EMAIL_USE_TLS = True
TIME_ZONE = 'US/Pacific'
LANGUAGE_CODE = 'en-us'
SITE_ID = 2
USE_I18N = False
USE_L10N = False
AUTH_USER_MODEL = 'coreExtend.Account'
LOGIN_REDIRECT_URL = '/replica/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
ALLOW_NEW_REGISTRATIONS = False
WSGI_APPLICATION = 'app.wsgi.application'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

if ENABLE_S3:
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATIC_URL = os.environ.get('LIVE_STATIC_URL', 'https://static.example.com/')
    MEDIA_URL = os.environ.get('LIVE_MEDIA_URL', 'https://static.example.com/media/')
else:    
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    STATIC_URL = '/static/'
    MEDIA_URL = '/static/media/'



#Site Settings
SITE_NAME = os.environ.get('SITE_NAME', 'A Life Well Played')
SITE_DESC =  os.environ.get('SITE_DESC', 'Just a copy of another content publishing platform.')
SITE_URL =  os.environ.get('SITE_URL', 'http://localhost')
SITE_AUTHOR = os.environ.get('SITE_AUTHOR', 'Tyler Rilling')

#Amazon S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '123')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '123')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME', 'static.example.com')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_BUCKET_DOMAIN', 'static.example.com')
AWS_S3_SECURE_URLS = False

from boto.s3.connection import OrdinaryCallingFormat
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

REST_FRAMEWORK = {
    'PAGINATE_BY': 25, # Default to 25
    'PAGINATE_BY_PARAM': 'page_size', # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100, # Maximum limit allowed when using `?page_size=xxx`.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# ===========================
# = Django-specific Modules =
# ===========================

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = os.environ.get('SECRET_KEY', '4eJUc9x86aXSLG07QgM1qZskVYZTBsWRkRMQc04rPLLgjos1wp')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(CURRENT_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            	'coreExtend.context_processors.template_settings',
                'coreExtend.context_processors.template_times',
            ],
            'debug': DEBUG,
        },
    },
]

MIDDLEWARE_CLASSES = (
    'coreExtend.middleware.SubdomainURLRoutingMiddleware',
	'coreExtend.middleware.MultipleProxyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

ROOT_URLCONF = 'app.urls'

SUBDOMAIN_URLCONFS = {
	None: 'app.urls',
    'api': 'app.apps.replica.api.urls',
}

#SESSION_COOKIE_DOMAIN = '.alifewellplayed.com'


INSTALLED_APPS = (
    #Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    #external
    'storages',
    'rest_framework',
    'rest_framework_swagger',
    'pagedown',

    #Internal
    'coreExtend',
    'replica',
    'replica.cms',
    'replica.pulse',
    'replica.api',
    'replica.contrib.micro',
    'replica.contrib.shorturl',
    'replica.contrib.publisher',
)

LOGGING = {
    "version": 1,
    # Don't throw away default loggers.
    "disable_existing_loggers": False,
    "handlers": {
        # Redefine console logger to run in production.
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        # Redefine django logger to use redefined console logging.
        "django": {
            "handlers": ["console"],
        }
    }
}
