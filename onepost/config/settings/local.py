from .base import *  # noqa
from .base import env


DEBUG = True
SECRET_KEY = env('DJANGO_SECRET_KEY', default='Tb8iqRxXPbube2qD9nJBxMtkCYAEK0jqzLtXEczynjjHuV2h7duQk5Qox4lYoPDC')
ALLOWED_HOSTS = ["*"]

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': f'{env("REDIS_URL", default="redis://195.2.81.190:6380")}/0',  # 网站缓存使用Redis 0
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'IGNORE_EXCEPTIONS': True,
#         }
#     }
# }

