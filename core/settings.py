import os
from pathlib import Path

from django.contrib.messages import constants as messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from environ import Env

env = Env(
    DEBUG=(bool, True),
    DEBUG_PROPAGATE_EXCEPTIONS=(bool, True),
    SECRET_KEY=(str, "aliwy-w)qwg1##ln(ig)j$s6oz#vp4zq4hm11ao$j9b!h6k*8x"),
    ALLOWED_HOSTS=(list, ["*"]),
    POSTGRES_DB=(str, "kpi_terdpi"),
    POSTGRES_USER=(str, "postgres"),
    POSTGRES_PASSWORD=(str, "2004"),
    POSTGRES_HOST=(str, "localhost"),
    POSTGRES_PORT=(int, 5432),
    REDIS_HOST=(str, "localhost"),
    REDIS_PORT=(int, 6379),
    OAUTH2_CLIENT_SECRET=(str, ""),
    OAUTH2_CLIENT_ID=(int, 3),
    OAUTH2_REDIRECT_URI=(str, ""),
    OAUTH2_AUTHORIZE_URL=(str, ""),
    OAUTH2_TOKEN_URL=(str, ""),
    OAUTH2_USER_INFO_URL=(str, ""),
)
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = env.bool("DEBUG")

DEBUG_PROPAGATE_EXCEPTIONS = env.bool("DEBUG_PROPAGATE_EXCEPTIONS")

if DEBUG:
    Env.read_env(os.path.join(BASE_DIR, ".env"))

CORE_DIR = os.path.join(BASE_DIR, "core")

SECRET_KEY = env("SECRET_KEY")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# IsAuthenticatedOrReadOnly
REST_FRAMEWORK = {
    "PAGE_SIZE": 40,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# Application definition

INSTALLED_APPS = [
    "django_celery_beat",
    "parler",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "oauth",
    "social_django",
    "tinymce",
    "core",
    "category",
    "posts",
    "home",
    "index",
    "active_link",
]

PARLER_DEFAULT_LANGUAGE_CODE = "uz"

PARLER_LANGUAGES = {
    None: (
        {
            "code": "uz",
        },
        {
            "code": "ru",
        },
    ),
    "default": {
        "fallbacks": ["ru"],
        "hide_untranslated": False,
    },
}

SITE_ID = 1

LANGUAGES = (
    ("ru", _("Русский")),
    ("uz", _("O'zbekcha")),
)

AUTH_USER_MODEL = "oauth.User"

AUTHENTICATION_BACKENDS = [
    "oauth.backends.AuthBackend",
]

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

OAUTH2_CLIENT_SECRET = env("OAUTH2_CLIENT_SECRET")
OAUTH2_CLIENT_ID = env("OAUTH2_CLIENT_ID")
OAUTH2_REDIRECT_URI = env("OAUTH2_REDIRECT_URI")
OAUTH2_AUTHORIZE_URL = env("OAUTH2_AUTHORIZE_URL")
OAUTH2_TOKEN_URL = env("OAUTH2_TOKEN_URL")
OAUTH2_USER_INFO_URL = env("OAUTH2_USER_INFO_URL")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

LOGOUT_URL = "logout"

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

LOGIN_URL = reverse_lazy("oauth:login")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR / "data" / "static")
STATICFILES_DIRS = [
    os.path.join(CORE_DIR, "static"),
]
MEDIA_ROOT = os.path.join(BASE_DIR / "data" / "media")

MEDIA_URL = "/media/"

REDIS_HOST = env("REDIS_HOST")
REDIS_PORT = env("REDIS_PORT")

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}
