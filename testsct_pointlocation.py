import unittest
from sct import SCT
from sct_pointlocation import SCTPointLocation


class TestSCTPointLocation(unittest.TestCase):
    def testinit_empty(self):
        T = SCT(3,1,1)
        ploc = SCTPointLocation(T, [])



if __name__ == '__main__':
    unittest.main()
