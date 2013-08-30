# -*- encoding: utf-8 -*-

TIME_ZONE = 'America/Montreal'

LANGUAGE_CODE = 'fr'

LANGUAGES = (
    ('pt', 'Portugues'),
    ('fr', 'French'),
)

USE_I18N = True
USE_L10N = True
USE_TZ = True


MIDDLEWARE_CLASSES += (
    'django.middleware.locale.LocaleMiddleware',
)
