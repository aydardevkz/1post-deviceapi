import os
import time

import environ
from redis.sentinel import Sentinel

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('apps')

env = environ.Env(
    DEBUG=(bool, False)
)
APPEND_SLASH = False
env.read_env(env_file=str(ROOT_DIR.path('.env')))


print("----------------- ENVIRONMENT VARIABLES -----------------")
DEBUG = env.bool('DJANGO_DEBUG', False)

TIME_ZONE = 'Asia/Almaty'
LANGUAGE_CODE = 'en-En'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False

HOST_DB = env('DATABASE_HOST')
PORT_DB = env('DATABASE_PORT')
print(f"HOST_DB: {HOST_DB}")
print(f"PORT_DB: {PORT_DB}")

DATABASES = {
    'app_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'app_service_db',
        'USER': env.str('APP_DATABASE_USER', default='postgres'),
        'PASSWORD': env.str('APP_DATABASE_PASSWORD', default='Admin123'),
        'HOST': HOST_DB,
        'PORT': PORT_DB,
    },
    'user_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'user_service_db',
        'USER': env.str('USER_DATABASE_USER', default='postgres'),
        'PASSWORD': env.str('USER_DATABASE_PASSWORD', default='Admin123'),
        'HOST': HOST_DB,
        'PORT': PORT_DB,
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'default_service_db',
        'USER': env.str('DEFAULT_DATABASE_USER', default='postgres'),
        'PASSWORD': env.str('DEFAULT_DATABASE_PASSWORD', default='Admin123'),
        'HOST': HOST_DB,
        'PORT': PORT_DB,
    },
    'auth_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auth_service_db',
        'USER': env.str('AUTH_DATABASE_USER', default='postgres'),
        'PASSWORD': env.str('AUTH_DATABASE_PASSWORD', default='Admin123'),
        'HOST': HOST_DB,
        'PORT': PORT_DB,
    },
    'express_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'express_service_db',
        'USER': env.str('EXPRESS_DATABASE_USER', default='postgres'),
        'PASSWORD': env.str('EXPRESS_DATABASE_PASSWORD', default='Admin123'),
        'HOST': HOST_DB,
        'PORT': PORT_DB,
    },
    'notification_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'notification_database',
        'USER': env.str('NOTIFICATION_DATABASE_USER', default='postgres'),
        'PASSWORD': env.str('NOTIFICATION_DATABASE_PASSWORD', default='Admin123'),
        'HOST': HOST_DB,
        'PORT': PORT_DB,
    },
    'open_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'open_service_db',
        'USER': env.str('OPEN_DATABASE_USER', default='postgres'),
        'PASSWORD': env.str('OPEN_DATABASE_PASSWORD', default='Admin123'),
        'HOST': HOST_DB,
        'PORT': PORT_DB,
    }

}

DATABASE_APPS_MAPPING = {
    'app_service': 'app_db',
    'user_service': 'user_db',
    'auth_service': 'auth_db',
    'default_service': 'default',
    'express_service': 'express_db',
    'notification_service': 'notification_db',
    'open_service': 'open_db',
}

DATABASE_ROUTERS = [
    'config.routers.AppDatabaseRouter',
    'config.routers.UserDatabaseRouter',
    'config.routers.DefaultDatabaseRouter',
    'config.routers.AuthDatabaseRouter',
    'config.routers.ExpressDatabaseRouter',
    'config.routers.NotificationDatabaseRouter',
    'config.routers.OpenDatabaseRouter',
]

ROOT_URLCONF = 'config.urls'

# APPS
DJANGO_APPS = [
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'crispy_forms',
    'corsheaders',
    'rest_framework',
    'firebase_admin',
    'django_filters',
    # "django_celery_beat",
]

LOCAL_APPS = [
    'apps.app_service.apps.AppServiceConfig',
    'apps.user_service.apps.UserServiceConfig',
    'apps.auth_service.apps.AuthServiceConfig',
    'apps.notification_service.apps.NotificationServiceConfig',
    'apps.express_service.apps.ExpressServiceConfig',
    'apps.open_service.apps.OpenServiceConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = 'user_service.UserBase'
LOGIN_URL = '/api-auth/login'

AUTHENTICATION_BACKENDS = [
    'apps.auth_service.backends.PhoneBackend',
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# allow header
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': (
        'config.permission.permissions.CustomAuthenticationPermission',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
        'rest_framework.parsers.FormParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'config.authentication.standard_authentication.CustomStandardAdminAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'EXCEPTION_HANDLER': 'config.utils.custom_exception.custom_exception_handler',
}

LOG_DIR = os.path.join(ROOT_DIR, 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + '/info_logs.log',
            'formatter': 'simple',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR + '/error_logs.log',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'api_service.signals': {
            'handlers': ['file_info'],
            'level': 'INFO',
            'propagate': False,
        },
        '': {
            'handlers': ['file_error'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SYSTEM_NAME = "1post"

STATIC_ROOT = os.path.join(ROOT_DIR, "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    str(ROOT_DIR.path('staticfiles')),
]

MEDIA_ROOT = str(ROOT_DIR('media'))
MEDIA_URL = '/media/'

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

VERIFICATION_CODE_LIFE_SPAN = 10  # minutes
TOKEN_LIFE_SPAN = 24 * 60 * 30  # minutes
REFRESH_TOKEN_LIFE_SPAN = 2 * 30 * 24 * 60  # minutes

APP_VERSION = env('APP_VERSION', default='1.0.0')


REDIS_SENTINEL_SERVICE = env('REDIS_SENTINEL_SERVICE', default='mymaster')
REDIS_SENTINEL_HOST1 = env('REDIS_SENTINEL_HOST1', default='localhost')
REDIS_SENTINEL_HOST2 = env('REDIS_SENTINEL_HOST2', default='localhost')
REDIS_SENTINEL_HOST3 = env('REDIS_SENTINEL_HOST3', default='localhost')
REDIS_SENTINEL_PORT1 = int(os.getenv('REDIS_SENTINEL_PORT1', 26379))
REDIS_SENTINEL_PORT2 = int(os.getenv('REDIS_SENTINEL_PORT2', 26380))
REDIS_SENTINEL_PORT3 = int(os.getenv('REDIS_SENTINEL_PORT3', 26381))

SENTINEL_HOSTS  = [
    (REDIS_SENTINEL_HOST1, REDIS_SENTINEL_PORT1),
    (REDIS_SENTINEL_HOST2, REDIS_SENTINEL_PORT2),
    (REDIS_SENTINEL_HOST3, REDIS_SENTINEL_PORT3),
]

# 配置 Redis Sentinel
SENTINEL = Sentinel(
    SENTINEL_HOSTS, # Sentinel 节点列表
    socket_timeout=0.5
)


# 配置 Redis 缓存
AUTH_CACHE_ALIAS = 'auth_cache'
EXPRESS_CACHE_ALIAS = 'express_cache'
APP_CACHE_ALIAS = 'app_cache'
USER_CACHE_ALIAS = 'user_cache'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            f"redis://{REDIS_SENTINEL_HOST1}:{REDIS_SENTINEL_PORT1}/0",
        ],
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.SentinelClient',
            'SENTINELS': [
                (REDIS_SENTINEL_HOST1, REDIS_SENTINEL_PORT1),
                (REDIS_SENTINEL_HOST2, REDIS_SENTINEL_PORT2),
                (REDIS_SENTINEL_HOST3, REDIS_SENTINEL_PORT3),
            ],
            'MASTER_NAME': REDIS_SENTINEL_SERVICE,
            'SOCKET_TIMEOUT': 2,
            'SOCKET_CONNECT_TIMEOUT': 0.5,
            'SOCKET_KEEPALIVE': True,
            'CONNECTION_POOL_CLASS': 'redis.sentinel.SentinelConnectionPool',
            'CONNECTION_POOL_KWARGS': {
                'service_name': REDIS_SENTINEL_SERVICE,
                'sentinel_manager': SENTINEL,
                'max_connections': 100,
            },
            'retry_on_timeout': True,
            'IGNORE_EXCEPTIONS': True,
            'health_check_interval': 30,
            'DB': 0
        }
    },
    AUTH_CACHE_ALIAS: {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            f"redis://{REDIS_SENTINEL_HOST1}:{REDIS_SENTINEL_PORT1}/1",
        ],
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.SentinelClient',
            'SENTINELS': [
                (REDIS_SENTINEL_HOST1, REDIS_SENTINEL_PORT1),
                (REDIS_SENTINEL_HOST2, REDIS_SENTINEL_PORT2),
                (REDIS_SENTINEL_HOST3, REDIS_SENTINEL_PORT3),
            ],
            'MASTER_NAME': REDIS_SENTINEL_SERVICE,
            'SOCKET_TIMEOUT': 2,
            'SOCKET_CONNECT_TIMEOUT': 0.5,
            'SOCKET_KEEPALIVE': True,
            'CONNECTION_POOL_CLASS': 'redis.sentinel.SentinelConnectionPool',
            'CONNECTION_POOL_KWARGS': {
                'service_name': REDIS_SENTINEL_SERVICE,
                'sentinel_manager': SENTINEL,
                'max_connections': 100,
            },
            'retry_on_timeout': True,
            'IGNORE_EXCEPTIONS': True,
            'health_check_interval': 30,
            'DB': 1
        }
    },
    APP_CACHE_ALIAS: {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            f"redis://{REDIS_SENTINEL_HOST1}:{REDIS_SENTINEL_PORT1}/{REDIS_SENTINEL_SERVICE}/2",
        ],
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.SentinelClient',
            'SENTINELS': [
                (REDIS_SENTINEL_HOST1, REDIS_SENTINEL_PORT1),
                (REDIS_SENTINEL_HOST2, REDIS_SENTINEL_PORT2),
                (REDIS_SENTINEL_HOST3, REDIS_SENTINEL_PORT3),
            ],
            'MASTER_NAME': REDIS_SENTINEL_SERVICE,
            'SOCKET_TIMEOUT': 2,
            'SOCKET_CONNECT_TIMEOUT': 0.5,
            'SOCKET_KEEPALIVE': True,
            'CONNECTION_POOL_CLASS': 'redis.sentinel.SentinelConnectionPool',
            'CONNECTION_POOL_KWARGS': {
                'service_name': REDIS_SENTINEL_SERVICE,
                'sentinel_manager': SENTINEL,
                'max_connections': 100,
            },
            'retry_on_timeout': True,
            'IGNORE_EXCEPTIONS': True,
            'health_check_interval': 30,
            'DB': 2
        }
    },
    EXPRESS_CACHE_ALIAS: {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            f"redis://{REDIS_SENTINEL_HOST1}:{REDIS_SENTINEL_PORT1}/{REDIS_SENTINEL_SERVICE}/3",
        ],
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.SentinelClient',
            'SENTINELS': [
                (REDIS_SENTINEL_HOST1, REDIS_SENTINEL_PORT1),
                (REDIS_SENTINEL_HOST2, REDIS_SENTINEL_PORT2),
                (REDIS_SENTINEL_HOST3, REDIS_SENTINEL_PORT3),
            ],
            'MASTER_NAME': REDIS_SENTINEL_SERVICE,
            'SOCKET_TIMEOUT': 2,
            'SOCKET_CONNECT_TIMEOUT': 0.5,
            'SOCKET_KEEPALIVE': True,
            'CONNECTION_POOL_CLASS': 'redis.sentinel.SentinelConnectionPool',
            'CONNECTION_POOL_KWARGS': {
                'service_name': REDIS_SENTINEL_SERVICE,
                'sentinel_manager': SENTINEL,
                'max_connections': 100,
            },
            'retry_on_timeout': True,
            'IGNORE_EXCEPTIONS': True,
            'health_check_interval': 30,
            'DB': 3
        }
    },
    USER_CACHE_ALIAS: {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            f"redis://{REDIS_SENTINEL_HOST1}:{REDIS_SENTINEL_PORT1}/{REDIS_SENTINEL_SERVICE}/4",
        ],
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.SentinelClient',
            'SENTINELS': [
                (REDIS_SENTINEL_HOST1, REDIS_SENTINEL_PORT1),
                (REDIS_SENTINEL_HOST2, REDIS_SENTINEL_PORT2),
                (REDIS_SENTINEL_HOST3, REDIS_SENTINEL_PORT3),
            ],
            'MASTER_NAME': REDIS_SENTINEL_SERVICE,
            'SOCKET_TIMEOUT': 2,
            'SOCKET_CONNECT_TIMEOUT': 0.5,
            'SOCKET_KEEPALIVE': True,
            'CONNECTION_POOL_CLASS': 'redis.sentinel.SentinelConnectionPool',
            'CONNECTION_POOL_KWARGS': {
                'service_name': REDIS_SENTINEL_SERVICE,
                'sentinel_manager': SENTINEL,
                'max_connections': 100,
            },
            'retry_on_timeout': True,
            'IGNORE_EXCEPTIONS': True,
            'health_check_interval': 30,
            'DB': 4
        }
    },

}


AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY', default='')
AWS_S3_ENDPOINT_URL = env.str('AWS_S3_ENDPOINT_URL', default='')
AWS_S3_ENDPOINT_HOST = env.str('AWS_S3_ENDPOINT_HOST', default='')
AWS_S3_USE_SSL = True
AWS_DEFAULT_ACL = None
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

PUBLIC_MEDIA_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'core.storage_backends.PublicMediaStorage'

#pivate media
PRIVATE_MEDIA_LOCATION = 'private'
PRIVATE_FILE_STORAGE = 'core.storage_backends.PrivateMediaStorage'

print(f"AWS_S3_ENDPOINT_URL: {AWS_S3_ENDPOINT_URL}")
print(f"AWS_ACCESS_KEY_ID: {AWS_ACCESS_KEY_ID}")
print(f"AWS_SECRET_ACCESS_KEY: {AWS_SECRET_ACCESS_KEY}")


JWT_PRIVATE_KEY = open(os.path.join(APPS_DIR, "auth_service/token/rsa_key/private_key.pem")).read()
JWT_PUBLIC_KEY = open(os.path.join(APPS_DIR, "auth_service/token/rsa_key/public_key.pem")).read()


