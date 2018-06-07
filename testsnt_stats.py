import unittest
from snt import SNT
from snt_stats import SNTStats
from metric import Euclidean
from point import Point
from snt_pointlocation import SNTPointLocation

class TestSNT(unittest.TestCase):
    
    def testall(self):
        points = [Point([x, 0, 1], Euclidean()) for x in [2, 11, 28, 0]]
        T = SNT(2, 1, 1, 4)
        T.construct(points, SNTPointLocation)
        stats = SNTStats(T)
        self.assertEqual(stats.levelno(), 6)
        self.assertEqual(stats.nodeno(), 12)
        self.assertEqual(stats.childno(), 12)
        self.assertEqual(stats.relno(), 26)
        self.assertEqual(stats.jumpno(), 0)
        
        points = [Point([x], Euclidean()) for x in [25, 20, 54, 30, 40, 0]]
        T = SNT(5, 1, 1)
        T.construct(points, SNTPointLocation)
        stats = SNTStats(T)
        self.assertEqual(stats.levelno(), 3)
        self.assertEqual(stats.nodeno(), 10)
        self.assertEqual(stats.childno(), 10)
        self.assertEqual(stats.relno(), 30)
        self.assertEqual(stats.jumpno(), 0)
        
        points = [Point([x, 0, 1], Euclidean()) for x in [2, 65, 69, 0]]
        T = SNT(2, 1, 1, 4)
        T.construct(points, SNTPointLocation)
        stats = SNTStats(T)
        self.assertEqual(stats.jumpno(), 2)
    
if __name__ == '__main__':
    unittest.main()
    
