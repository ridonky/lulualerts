"""
Django settings for retail_alerts project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import django_heroku


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# # LOCAL
# SECRET_KEY = str(os.getenv('SECRET_KEY'))
# REMOTE
SECRET_KEY = os.environ['SECRET_KEY']

# ADDED FOR SENDING EMAILS VIA COURIER
# # LOCAL
# AUTH_TOKEN = str(os.getenv('AUTH_TOKEN'))
# REMOTE
AUTH_TOKEN = os.environ['AUTH_TOKEN']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# # old before heroku
# ALLOWED_HOSTS = []
# # end old before heroku

# # new for heroku
# ALLOWED_HOSTS = ['https://lulualerts.herokuapp.com/']
# # end new for heroku

# Allows all hosts
IS_HEROKU = "DYNO" in os.environ


if IS_HEROKU:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = [
        'http://lulualerts.com',
        'http://www.lulualerts.com',
        'https://lulualerts.herokuapp.com',
        'http://lulualerts.herokuapp.com',
        'lulualerts.com',
        'www.lulualerts.com'
        ]

# Application definition

INSTALLED_APPS = [
    'lulu_alerts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions', 
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://lulualerts.com',
    'http://www.lulualerts.com',
    'https://lulualerts.herokuapp.com',
    'http://lulualerts.herokuapp.com',
]


ROOT_URLCONF = 'retail_alerts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'retail_alerts.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# # START LOCAL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# # END LOCAL

# START REMOTE
DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd17udcmv0dhs12',
        'USER': 'yafbiyjfcnjyjt',
        'PASSWORD' : os.environ['POSTGRES_DB_PASSWORD'],
        'HOST': 'ec2-18-214-35-70.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}
# END FOR REMOTE

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


# STATIC FILE SETTINGS - OLD I GUESS
    # STATIC_ROOT = os.path.join(BASE_DIR, 'static') # this is fine, 100%
    # STATIC_URL = "/static/" # this is fine, 90%

    # STATICFILES_DIR = [os.path.join(BASE_DIR, 'static'),] # this is spelled wrong - can change to DIRS and also test- its nto in github test

    # # for whitenoise 
    # STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    # django_heroku.settings(locals()) # NEED TO LOOK INTO! tried removing
# END STATIC FILE SETTINGS

# STATIC FILE SETTINGS _ NEW TEST _ COPY OF GITHUB EXAMPLE
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_URL = "/static/" 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') #changed from static to staticfiles
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles'),] # added this now...
# STATIC FILE SETTINGS _ END NEW TEST


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    }
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
