import json
import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = json.loads(os.getenv("DEBUG", "false"))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1 .localhost [::1]").split(" ")

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "http://127.0.0.1").split(" ")

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
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "common.middleware.UpdateVaryForConditionalGetMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "common.middleware.RemoveEmptyQueryString",
    "users.middleware.UserActiveMidlleware",
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


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASE_URL = os.getenv("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
}

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

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "select2"

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# We have enabled the static file collection while deploying the app
# Type 1 to disable
DISABLE_COLLECTSTATIC = 0


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"

LOGIN_URL = "login"

AUTH_USER_MODEL = "users.User"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = BASE_DIR / "static"

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "assets",  # place for favicon.ico
]

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "media/"

# ----Yandex s3 api----
ENABLED_YANDEX_STORAGE = json.loads(os.getenv("ENABLED_YANDEX_STORAGE", "false"))

if ENABLED_YANDEX_STORAGE:
    STATICFILES_STORAGE = "common.custom_storage.StaticYandexCloudStorage"

    DEFAULT_FILE_STORAGE = "common.custom_storage.MediaYandexCloudStorage"

    YANDEX_OBJECT_STORAGE_BUCKET_NAME = os.getenv("YANDEX_OBJECT_STORAGE_BUCKET_NAME")

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")

    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")

    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")


# Set the default value for ChoiceFilter.empty_label
FILTERS_EMPTY_CHOICE_LABEL = "Не выбрано"

USER_ONLINE_TIMEOUT = json.loads(os.getenv("USER_ONLINE_TIMEOUT", "60"))

USER_LAST_SEEN_TIMEOUT = json.loads(os.getenv("USER_LAST_SEEN_TIMEOUT", "86400"))

# ----The settings for base group of users on the site----
BASE_GROUP = os.getenv("BASE_GROUP", "base_members_of_site")

PERMISSIONS_FOR_BASE_GROUP = json.loads(
    os.getenv("PERMISSIONS_FOR_BASE_GROUP", "false")
)

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

EMAIL_USE_TLS = json.loads(os.getenv("EMAIL_USE_TLS", "true"))

EMAIL_HOST = os.getenv("EMAIL_HOST")

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

EMAIL_PORT = json.loads(os.getenv("EMAIL_PORT", "25"))

INTERNAL_IPS = [
    "127.0.0.1",
]
