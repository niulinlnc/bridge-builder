import importlib
import os
import sys
os.chdir(__path__[0])
files = os.listdir('.')
sys.path.insert(0, '.')
SITES_G = {}
class bcolors:
    """
    """
    FAIL = '\033[91m'
    ENDC = '\033[0m'

for file_name in files:
    try:
        n, e = file_name.split('.')
    except:
        continue
    if n != '__init__' and e == 'py':
        try:
            fun = importlib.import_module(n)
            SITES_G.update(getattr(fun, n))
        except Exception as e:
            p = os.path.abspath(file_name)
            print bcolors.FAIL, '*' * 80
            print 'could not load file:'
            print p
            print 'please fix it'
            print 'to do so you can run:'
            print 'vim %s' % os.path.abspath(file_name)
            print 'or with any editor of your choice'
            print '--->', str(e)
            print '*' * 80, bcolors.ENDC
