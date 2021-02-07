"""
Django settings for financial_server project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os

from os.path import abspath, basename, dirname, join
from os import path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@+iza+z*cv^s(=9_e7jio0^ay!04g&h)a##ah4ai*3&nj7e1)^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'financial_server.apps.permissions',
    'financial_server.apps.users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'financial_server.urls'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}

WSGI_APPLICATION = 'financial_server.wsgi.application'


# Fetch Django's project directory
DJANGO_ROOT = dirname(abspath(__file__))

# Fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# The name of the whole site
SITE_NAME = basename(DJANGO_ROOT)

# Collect static files here
STATIC_ROOT = join(DJANGO_ROOT, 'static')

# Collect media files here
MEDIA_ROOT = join(PROJECT_ROOT, 'media')


MEDIA_URL = '/media/'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# look for static assets here
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static_files'),
    os.path.join(BASE_DIR, 'node_modules'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PARSER = 'compressor.parser.LxmlParser'
COMPRESS_ENABLED = True
COMPRESS_MTIME_DELAY = 1
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, 'templates'),
]

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

# user's stuff
AUTH_USER_MODEL = 'users.User'

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

REDIS_PASSWORD = ""

THUMBNAILS = {
    'METADATA': {
        'PREFIX': 'thumbs',
        'BACKEND': 'thumbnails.backends.metadata.RedisBackend',
        'db': 2,
        'password': REDIS_PASSWORD
    },
    'STORAGE': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage'
    },
    'BASE_DIR': 'thumb',
    'SIZES': {
        'size_140x140': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 140, 'height': 140, 'method': 'fill'},
                {'PATH': 'thumbnails.processors.crop', 'width': 140, 'height': 140},
            ],
        },
        'size_400x600': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 400, 'height': 600, 'method': 'fit'},
                {'PATH': 'thumbnails.processors.crop', 'width': 400, 'height': 600},
            ],
        },
        'size_400x400': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 400, 'height': 400, 'method': 'fit'},
                {'PATH': 'thumbnails.processors.crop', 'width': 400, 'height': 400},
            ],
        },
        'size_800x800': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 800, 'height': 800, 'method': 'fit'},
                {'PATH': 'thumbnails.processors.crop', 'width': 800, 'height': 800},
            ],
        },
        'size_800x480': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 800, 'height': 480, 'method': 'fit'},
                {'PATH': 'thumbnails.processors.crop', 'width': 800, 'height': 480},
            ],
        },
        'size_480x800': {
            'FORMAT': 'webp',
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 480, 'height': 800, 'method': 'fit'},
                {'PATH': 'thumbnails.processors.crop', 'width': 480, 'height': 800},
            ],
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path.join(PROJECT_ROOT, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

try:
    from .local_settings import *  # type: ignore  # noqa
except ImportError:
    pass