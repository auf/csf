import sys
import glob
import types

from os.path import abspath, dirname, join

PROJECT_DIR = abspath(dirname(__file__))

conffiles = glob.glob(join(PROJECT_DIR, 'settings', '*.py'))
conffiles.sort()

for f in conffiles:
    execfile(abspath(f))

    # from https://github.com/2general/django-split-settings/blob/master/split_settings/tools.py
    # add dummy modules to sys.modules to make runserver autoreload work with settings components
    modulename = '_settings.%s' % f
    module = types.ModuleType(modulename)
    module.__file__ = f
    sys.modules[modulename] = module

from conf import *
