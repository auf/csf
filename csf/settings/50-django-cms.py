from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS


TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.request",
    'django.contrib.messages.context_processors.messages',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
)

MIDDLEWARE_CLASSES += (
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

INSTALLED_APPS = (
    "djangocms_admin_style",
) + INSTALLED_APPS

INSTALLED_APPS += (
    "cms",
    "cms.stacks",
    "cms.publisher",
    'cms.plugins.picture',
    "cms.plugins.link",
    "djangocms_text_ckeditor",
    "cmsplugin_youtube",
    "menus",
    "mptt",
    "sekizai",
    "south",
)

gettext = lambda s: s

CMS_LANGUAGES = {
    1: [
        {
            'code': 'fr',
            'name': gettext('French'),
            'public': True,
            'fallbacks': ['pt'],
        },
        {
            'code': 'pt',
            'name': gettext('Portugues'),
            'public': True,
            'fallbacks': ['fr'],
        },
    ],
    'default': {
        'fallbacks': ['fr', 'pt'], 
        'redirect_on_fallback':False,
        'public': True,
        'hide_untranslated': False,
    }
}

CMS_TEMPLATES = (
    ('1col.html', gettext('homepage')),
    ('2col.html', gettext('two columns')),
    ('2col-withform.html', gettext('two columns with form')),
)
