"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import env


DEBUG = True
SECRET_KEY = env("DJANGO_SECRET_KEY", default="K1AH9isH23modOisn6UkTIosZAkvu8hZaH5Qtk2UBBk8WxFEK7Gezg9RP9E1yvS0")
TEST_RUNNER = "django.test.runner.DiscoverRunner"


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": ""
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG  # noqa F405
TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa F405
    (
        "django.templates.loaders.cached.Loader",
        [
            "django.templates.loaders.filesystem.Loader",
            "django.templates.loaders.app_directories.Loader",
        ],
    )
]
