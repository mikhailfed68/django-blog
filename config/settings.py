"""
Settings file for django-blog project.

For more information on this settings, see README.md
https://github.com/MichaelFed68/django-blog#for-developers
"""

import json
import os
import socket
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# Security settings
SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = json.loads(os.getenv("DEBUG", "false"))

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "127.0.0.1 .localhost [::1]",
).split(" ")

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "http://127.0.0.1 http://localhost",
).split(" ")

CSRF_COOKIE_SECURE = json.loads(os.getenv("CSRF_COOKIE_SECURE", "true"))

SESSION_COOKIE_SECURE = json.loads(os.getenv("SESSION_COOKIE_SECURE", "true"))

CSRF_COOKIE_HTTPONLY = json.loads(os.getenv("CSRF_COOKIE_HTTPONLY", "true"))

SESSION_COOKIE_HTTPONLY = json.loads(os.getenv("SESSION_COOKIE_HTTPONLY", "true"))

SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")

SESSION_ENGINE = os.getenv("SESSION_ENGINE", "django.contrib.sessions.backends.cache")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.humanize",
    "django.contrib.admindocs",
    "debug_toolbar",
    "django_select2",
    "bootstrap5",
    "sorl.thumbnail",
    "django_filters",
    "storages",
    "tinymce",
    "django_cleanup.apps.CleanupConfig",
    "users",
    "blog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "common.middleware.RemoveEmptyQueryString",
    "users.middleware.UserActiveMidlleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": {
                "url_replacer": "templatetags.url_replacer",
            },
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
}

# Cache settings
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.getenv("REDIS_URL"),
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

CACHE_MIDDLEWARE_SECONDS = json.loads(os.getenv("CACHE_MIDDLEWARE_SECONDS", "0"))

CACHE_MIDDLEWARE_ALIAS = os.getenv("CACHE_MIDDLEWARE_ALIAS", "default")

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "select2"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"

LOGIN_URL = "login"

AUTH_USER_MODEL = "users.User"


# Set the default value for ChoiceFilter.empty_label
FILTERS_EMPTY_CHOICE_LABEL = "Не выбрано"


# Online system settings
USER_ONLINE_TIMEOUT = json.loads(os.getenv("USER_ONLINE_TIMEOUT", "60"))

USER_LAST_SEEN_TIMEOUT = json.loads(os.getenv("USER_LAST_SEEN_TIMEOUT", "86400"))


# Settings for base group of users on the site
BASE_GROUP = os.getenv("BASE_GROUP", "base_members_of_site")

PERMISSIONS_FOR_BASE_GROUP = json.loads(
    os.getenv("PERMISSIONS_FOR_BASE_GROUP", "false")
)

# Default settings for base group
if not PERMISSIONS_FOR_BASE_GROUP:
    PERMISSIONS_FOR_BASE_GROUP = [
        "add_article",
        "change_article",
        "delete_article",
        "view_article",
        "add_blog",
        "view_blog",
        "view_language",
        "change_profile",
        "delete_profile",
        "view_profile",
    ]


# Setting Email configuration for sending reset email
ENABLED_EMAIL = json.loads(os.getenv("ENABLED_EMAIL", "false"))

if ENABLED_EMAIL:
    EMAIL_USE_TLS = json.loads(os.getenv("EMAIL_USE_TLS", "true"))

    EMAIL_HOST = os.getenv("EMAIL_HOST")

    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")

    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

    EMAIL_PORT = json.loads(os.getenv("EMAIL_PORT", "25"))
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Setting for django-debug-tool-bar
if DEBUG:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [f"{ip[:-1]}1" for ip in ips] + ["127.0.0.1"]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
# Yandex S3 API
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
# https://cloud.yandex.com/en/docs/storage/s3/
ENABLED_YANDEX_STORAGE = json.loads(os.getenv("ENABLED_YANDEX_STORAGE", "false"))

if ENABLED_YANDEX_STORAGE:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")

    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    AWS_DEFAULT_ACL = "public-read"

    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")

    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")

    YANDEX_OBJECT_STORAGE_BUCKET_NAME = os.getenv("YANDEX_OBJECT_STORAGE_BUCKET_NAME")

    YANDEX_S3_DOMAIN = os.getenv("YANDEX_S3_DOMAIN")

    AWS_S3_CUSTOM_DOMAIN = f"{YANDEX_OBJECT_STORAGE_BUCKET_NAME}{YANDEX_S3_DOMAIN}"

    # S3 static settings
    STATIC_LOCATION = "static"

    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"

    STATICFILES_STORAGE = "common.custom_storage.StaticYandexCloudStorage"

    # S3 public media settings
    PUBLIC_MEDIA_LOCATION = "media"

    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"

    DEFAULT_FILE_STORAGE = "common.custom_storage.MediaYandexCloudStorage"
else:
    NAME_STATIC_DIR = os.getenv("NAME_STATIC_DIR", "static")

    STATIC_ROOT = BASE_DIR / NAME_STATIC_DIR

    STATIC_URL = f"{NAME_STATIC_DIR}/"

    NAME_MEDIA_DIR = os.getenv("NAME_MEDIA_DIR", "media")

    MEDIA_ROOT = BASE_DIR / NAME_MEDIA_DIR

    MEDIA_URL = f"{NAME_MEDIA_DIR}/"


STATICFILES_DIRS = [
    BASE_DIR / "assets",  # place for favicon.ico
]
