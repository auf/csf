import os

from django.conf.global_settings import *  # NOQA

SITE_ID = '1'

PROJECT_ROOT = os.path.dirname(__file__)
ROOT = os.path.dirname(PROJECT_ROOT)

MEDIA_ROOT = os.path.join(ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(ROOT, 'static')
STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)
