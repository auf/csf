# -*- encoding: utf-8 -*-

TIME_ZONE = 'America/Montreal'

LANGUAGE_CODE = 'fr'

gettext = lambda s: s

LANGUAGES = (
    ('pt', gettext(u'português')),
    ('fr', gettext(u'français')),
)

USE_I18N = True
USE_L10N = True
USE_TZ = True


MIDDLEWARE_CLASSES += (
    'django.middleware.locale.LocaleMiddleware',
)

LOCALE_INDEPENDENT_PATHS = (
    r'^/api',
)
