import unittest
from point import Point
from sct_node import *


class TestSCTNode(unittest.TestCase):
    def testinit(self):
        p = Point(1,2)
        n = SCTNode(p, 5)
        self.assertTrue(len(n.ch) == 0)
        self.assertTrue(len(n.rel) == 1)
        self.assertTrue(n in n.rel)
        self.assertTrue(n.par is None)
        self.assertTrue(n.point is p)
        self.assertTrue(n.level == 5)

    def testaddrel(self):
        a = SCTNode(Point(1,2), 2)
        b = SCTNode(Point(5,7), 2)
        a.addrel(b)
        self.assertTrue(b in a.rel)
        self.assertTrue(a in b.rel)

    def testaddch(self):
        a = SCTNode(Point(1,2), 2)
        b = SCTNode(Point(5,7), 2)
        c = SCTNode(Point(5,6), 3)
        a.addch(c)
        self.assertTrue(c in a.ch)
        self.assertTrue(a is c.par)
        b.addch(c)
        self.assertTrue(c in b.ch)
        self.assertTrue(b is c.par)
        self.assertTrue(c not in a.ch)

    def testsetpar(self):
        a = SCTNode(Point(1,2), 2)
        b = SCTNode(Point(5,7), 2)
        c = SCTNode(Point(5,6), 3)
        c.setpar(a)
        self.assertTrue(c in a.ch)
        self.assertTrue(a is c.par)
        c.setpar(b)
        self.assertTrue(c in b.ch)
        self.assertTrue(b is c.par)
        self.assertTrue(c not in a.ch)

    def testgetchild(self):
        b = SCTNode(Point(5,7), 2)
        c = SCTNode(Point(5,6), 3)
        b.addch(c)
        self.assertEqual(b.getchild(), c)
        d = SCTNode(Point(4,6), 3)
        b.addch(d)
        self.assertTrue(b.getchild() in {c,d})


if __name__ == '__main__':
    unittest.main()
