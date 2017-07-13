import unittest
from point import Point


class TestPoint(unittest.TestCase):
    def testinitandgetitem(self):
        p = Point(3,5,1)
        self.assertEqual(p[0], 3)
        self.assertEqual(p[1], 5)
        self.assertEqual(p[2], 1)

    def testsqdistto(self):
        p = Point(0,0,0)
        q = Point(1,2,3)
        r = Point(2,3,3)
        self.assertEqual(p.sqdistto(q), q.sqdistto(p))
        self.assertEqual(p.sqdistto(q), 14)
        self.assertEqual(p.sqdistto(r), 22)
        self.assertEqual(q.sqdistto(r), 2)

    def testdistto(self):
        p = Point(0,0)
        q = Point(3,4)
        r = Point(12,5)
        self.assertEqual(p.distto(q), q.distto(p))
        self.assertEqual(p.distto(q), 5)
        self.assertEqual(p.distto(r), 13)

    def testdistto_pointlikeobject(self):
        class MyPoint:
            def __init__(self, point):
                self.point = point
        p = Point(0,0)
        q = MyPoint(Point(3,4))
        self.assertEqual(p.distto(q), 5)
        self.assertEqual(p.sqdistto(q), 25)

if __name__ == '__main__':
    unittest.main()
