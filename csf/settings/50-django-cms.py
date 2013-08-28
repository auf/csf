from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.request",
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
)

MIDDLEWARE_CLASSES += (
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

INSTALLED_APPS += (
    "cms",
    "menus",
    "mptt",
    'cms.plugins.text',
    "sekizai",
    "south"
)

gettext = lambda s: s

CMS_LANGUAGES = {
    1: [
        {
            'code': 'pt',
            'name': gettext('Portugues'),
            'public': True,
            'fallbacks': ['fr'],
        },
    ],
    2: [
        {
            'code': 'fr',
            'name': gettext('Dutch'),
            'public': True,
            'fallbacks': ['pt'],
        },
    ],
    'default': {
        'fallbacks': ['pt', 'fr'],
        'redirect_on_fallback':True,
        'public': False,
        'hide_untranslated': False,
    }
}

CMS_TEMPLATES = (
    ('simple.html', 'Simple'),
    ('2col.html', '2col'),
    ('hero.html', 'hero'),
)
