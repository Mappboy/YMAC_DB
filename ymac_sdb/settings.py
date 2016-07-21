"""
Django settings for ymac_sdb project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
FOR Some Reason the spatial server couldn't load the GEOS plugin
had to include it manually in this file
GEOS_LIBRARY_PATH = 'C:\\OSGeo4W64\\bin\\geos_c.dll'

MAybe include:
    - https://github.com/django-import-export/django-import-export
    - https://github.com/divio/django-filer
    - http://django-guardian.readthedocs.io/en/stable/api/guardian.admin.html
"""

import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$6a*9_a&4e3)-2%q)w4ij#!rsrsabo#yr)@z67u3l$099)kmk-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'ymac_db.apps.YmacDbConfig',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'dal',
    'dal_select2',
    'import_export',
    # 'grappelli',
    'suit',
    # 'material',
    # 'material.frontend',
    # 'material.admin',
    # 'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'bootstrap3',
    'debug_toolbar',
    'leaflet',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ymac_sdb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Included this for suit
                'django.core.context_processors.request',
            ],
        },
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '192.168.0.141:11211',
    }
}

WSGI_APPLICATION = 'ymac_sdb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ymacspatial',
        'USER': 'spuser',
        'PASSWORD': 'Yamatji01',
        'HOST': '192.168.0.141',
        'PORT': '5438'
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

# LDAP AUTH INTEGRATION
# AUTH_LDAP_SERVER_URI = "ldap://192.168.0.36:389"
# AUTH_LDAP_BIND_DN = "svc_spatial@yamatji.org.au"
# AUTH_LDAP_BIND_PASSWORD = "Yamatji_01Spatial"
# AUTHENTICATION_BACKENDS = [
#    'django_auth_ldap.backend.LDAPBackend',
#    'django.contrib.auth.backends.ModelBackend',
# ]

# EMAIL CONFIG
# https://docs.djangoproject.com/en/1.9/topics/email/
EMAIL_HOST = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""
EMAIL_SUBJECT_PREFIX = ""
EMAIL_USE_SSL = ""

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-au'

TIME_ZONE = 'Australia/Perth'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (-27, 121),
    'DEFAULT_ZOOM': 6,
}

SUIT_CONFIG = {
    'ADMIN_NAME': 'Spatial Database'
}

GRAPPELLI_ADMIN_TITLE = 'YMAC Spatial Database'

STATIC_URL = '/static/'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
