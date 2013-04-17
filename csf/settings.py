# -*- encoding: utf-8 -*-

import os
import socket
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as \
        DEFAULT_TEMPLATE_CONTEXT_PROCESSORS
from django.conf.global_settings import STATICFILES_FINDERS as \
        DEFAULT_STATICFILES_FINDERS
from django.conf.global_settings import MIDDLEWARE_CLASSES as \
        DEFAULT_MIDDLEWARE_CLASSES
from django.conf.global_settings import AUTHENTICATION_BACKENDS as \
        DEFAULT_AUTHENTICATION_BACKENDS
from django.conf.global_settings import TEMPLATE_LOADERS as \
        DEFAULT_TEMPLATE_LOADERS

# Rapports d'erreurs
SERVER_EMAIL = 'ne-pas-repondre@auf.org'
EMAIL_SUBJECT_PREFIX = '[csf - %s] ' % socket.gethostname()
ADMINS = ()

MANAGERS = ADMINS

TIME_ZONE = 'America/Montreal'

LANGUAGE_CODE = 'fr-ca'

SITE_ID = '1'

USE_I18N = True
USE_L10N = True
USE_TZ = True

PROJECT_ROOT = os.path.dirname(__file__)
SITE_ROOT = os.path.dirname(PROJECT_ROOT)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(SITE_ROOT, 'sitestatic')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
STATICFILES_FINDERS = DEFAULT_STATICFILES_FINDERS

ROOT_URLCONF = 'csf.urls'

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'raven.contrib.django',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

TEMPLATE_LOADERS = DEFAULT_TEMPLATE_LOADERS

MIDDLEWARE_CLASSES = DEFAULT_MIDDLEWARE_CLASSES + (
    'auf.django.piwik.middleware.TrackMiddleware',
)

AUTHENTICATION_BACKENDS = DEFAULT_AUTHENTICATION_BACKENDS

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

SOUTH_TESTS_MIGRATE = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

ADMIN_TOOLS_INDEX_DASHBOARD = 'csf.dashboard.CustomIndexDashboard'

from conf import *
