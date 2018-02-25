import unittest
import os
import sys
import importlib


"""
working with frameworks having aliases is very convinient
so bridgebuilder makes it easy to maintain them across all the boxes a developer
migth need to work with:
aliases stem from several places:
1. a file with "personal" aliases
    Its name is maintained in the config  file and can be overwritten
    using bin/s -set alias='path to the alias'
    By default it is called aliases.txt
2. for each site we create, a number of aliases are constructed
    Assuming the site name is XXX, then the following aliases are created
    - XXX, this alias activates workon with named XXX
      and chdirs into the XXX's builout folder
    - xxxh chdirs into the XXX's buihomelout folder
    - XXXa this changes into the sites addons folder
    - XXXc this runs git status on all addon modules listet in 
      
"""

bb_home = os.sep.join( os.path.abspath(__file__).split(os.sep)[:-2])
sys.path.insert(0, bb_home)
sys.path.insert(0, '.')

def my_import(what):
    # import 'what' without cluttering the the global namespace
    # so we can reimport what after changing a value
    cur_dir = os.getcwd()
    os.chdir('%s/config' % bb_home)
    result = importlib.import_module('__init__')
    return getattr(result, what)
    

class CreateAliasTests(unittest.TestCase):
    def test_add_personal_alias_file_name_to_settings(self):
        """
        make sure we can change the path to the file of personal aliases
        """
        print('--------------->', my_import('BB_HOME') )

if __name__ == '__main__':
    unittest.main()