import unittest
import os
import sys

bb_home = os.sep.join( __file__.split(os.sep)[:-2])
sys.path.insert(0, bb_home)

class CreateSite(unittest.TestCase):
    def test_load_create_site(self):
        """
        just make sure we can start ..
        """
        from config import BB_HOME as bh
        self.assertEqual(bh, bb_home)
    

if __name__ == '__main__':
    unittest.main()