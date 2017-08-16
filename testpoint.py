import unittest
from point import *
from metrics import *


class TestPoint(unittest.TestCase):
    def testinitandgetitem(self):
        p = Point([3, 5, 1], Euclidean())
        self.assertEqual(p[0], 3)
        self.assertEqual(p[1], 5)
        self.assertEqual(p[2], 1)

    def testdistto(self):
        metric = Euclidean()
        p = Point([0, 0], metric)
        q = Point([3, 4], metric)
        r = Point([12, 5], metric)
        self.assertEqual(p.distto(q), q.distto(p))
        self.assertEqual(p.distto(q), 5)
        self.assertEqual(p.distto(r), 13)
        self.assertEqual(p.distto(q, r), 5)
        self.assertEqual(metric.counter, 6)
        
        setMetric(Manhattan(), [p, q, r])
        self.assertEqual(p.distto(q), q.distto(p))
        self.assertEqual(p.distto(q), 7)
        self.assertEqual(p.distto(r), 17)
        self.assertEqual(p.distto(q, r), 7)
        
        setMetric(LInfinity(), [p, q, r])
        self.assertEqual(p.distto(q), q.distto(p))
        self.assertEqual(p.distto(q), 4)
        self.assertEqual(p.distto(r), 12)
        self.assertEqual(p.distto(q, r), 4)        

if __name__ == '__main__':
    unittest.main()
