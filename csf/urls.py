import glob
import sys
import types

from os.path import abspath, dirname, join

PROJECT_DIR = abspath(dirname(__file__))

urlfiles = glob.glob(join(PROJECT_DIR, 'urls', '*.py'))
urlfiles.sort()

for f in urlfiles:
    execfile(abspath(f))

    # from https://github.com/2general/django-split-settings/blob/master/split_settings/tools.py
    # add dummy modules to sys.modules to make runserver autoreload work with settings components
    modulename = '_urls.%s' % f
    module = types.ModuleType(modulename)
    module.__file__ = f
    sys.modules[modulename] = module

