"""
#Django settings for main project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from firebase_admin import initialize_app

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!

AUTH_USER_MODEL = "users.User"
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_hosts",
    "django_filters",
    "rest_framework",
    "corsheaders",
    "fcm_django",
    "drf_yasg",
    "knox",
    "users.apps.UserConfig",
    "admin_panel",
]

MIDDLEWARE = [
    "django_hosts.middleware.HostsRequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_hosts.middleware.HostsResponseMiddleware",
]

ROOT_URLCONF = "main.urls"
ROOT_HOSTCONF = "main.urls.hosts"
DEFAULT_HOST = "default"

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
                "main.custom.context_processors.dashboard",
            ],
            "libraries": {"template_filters": "main.custom.template_tags"},
        },
    }
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("knox.auth.TokenAuthentication",),
    "DATETIME_FORMAT": "%m/%d/%Y %H:%M:%S",
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

REST_KNOX = {"TOKEN_TTL": None}  # tokens never expire

WSGI_APPLICATION = "main.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

AUTHENTICATION_BACKENDS = [
    "main.custom.backend.CustomModelBackend",
    "django.contrib.auth.backends.ModelBackend",
]


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "staticfiles"
STATICFILES_DIRS = ["templates/static/"]

MEDIA_URL = "/media/"
MEDIA_ROOT = "mediafiles"

# fcm django config
FIREBASE_KEY = "firebase-admin.json"

FIREBASE_KEY_PATH = BASE_DIR / FIREBASE_KEY

FIREBASE_APP = initialize_app()

FCM_DJANGO_SETTINGS = {
    # default: _('FCM Django')
    "APP_VERBOSE_NAME": "Installed Devices",
    # Your firebase API KEY
    "FCM_SERVER_KEY": "",
    # true if you want to have only one active device per registered user at a time
    # default: False
    "ONE_DEVICE_PER_USER": False,
    # devices to which notifications cannot be sent,
    # are deleted upon receiving error response from FCM
    # default: False
    "DELETE_INACTIVE_DEVICES": False,
}


LOGIN_URL = 'admin:login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'admin:login'
