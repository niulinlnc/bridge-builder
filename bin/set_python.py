#!/usr/bin/env python

"""
this script just creates a python and a pip entry in bin
that have the executable bit set, and points to the 
bridgebuilders virtual environment

this is hany, when you have an OTHER virtual env active and want
to install something into bridgebuilder environment.

we put these links into a folder called python, which we exclude from git
in gitignore
so we can have the links in bin/ point to allways the same files
"""

import sys
import os
bb_home = os.sep.join( os.path.abspath(__file__).split(os.sep)[:-2])
py_exec = sys.executable
py_path = os.path.dirname(py_exec)
py_folder = '%s/python' % bb_home

class bcolors:
    """
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
# are we running in a virtual env at all?
# if not complain and terminate
venv = os.environ.get('VIRTUAL_ENV')
if not venv:
    print(bcolors.FAIL)
    print('*' * 80)
    print('please activate a virtual environment before running this script')
    print('*' * 80)
    print(bcolors.ENDC)
    sys.exit()
    

# create python folder
if not os.path.exists(py_folder):
    os.makedirs(py_folder)

# remove existing softlinks, the environ migth have changed
# and tell the good news
print(bcolors.OKGREEN)
print('*' * 80)
print('Active virtual env is:{}'.format(venv))
for p in ['python', 'pip']:
    try:
        os.unlink('%s/python/%s' % (bb_home, p))
    except:
        pass
    # and recreate them ..
    os.symlink('%s/%s' % (py_path, p), '%s/python/%s' % (bb_home, p))

    print('linked ', '%s/%s' % (py_path, p), 'to', '%s/python/%s' % (bb_home, p))
print('*' * 80, bcolors.ENDC)

    
