import socket

SESSION_COOKIE_NAME = 'sessionid_csf'

# App Formulaire
FORMULAIRE_IMAGE_MAX_SIZE = 5000 * 1024


# Rapports d'erreurs
SERVER_EMAIL = 'ne-pas-repondre@auf.org'
EMAIL_SUBJECT_PREFIX = '[csf - %s] ' % socket.gethostname()
ADMINS = ()
MANAGERS = ADMINS

ROOT_URLCONF = 'csf.urls'

INSTALLED_APPS += (
    'localeurl',
    'auf.django.auth_token',
    'south',
    'raven.contrib.django',
    'auf.django.references',
    'csf.splash',
    'csf.formulaire',
    'csf.portail',
    'csf.gestion',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'csf.context_processors.csf',
)


MIDDLEWARE_CLASSES += (
    'localeurl.middleware.LocaleURLMiddleware',
    'auf.django.auth_token.middleware.TokenAuthentification',
    'auf.django.piwik.middleware.TrackMiddleware',
)

SOUTH_TESTS_MIGRATE = False

AUTHENTICATION_BACKENDS += (
    'auf.django.auth_token.backends.TokenAuthBackend',
)

