import unittest
from node import *
from metric import Euclidean


class TestNode(unittest.TestCase):
    def testinit(self):
        p = Point([1, 2], Euclidean())
        n = Node(p, 5)
        self.assertTrue(len(n.ch) == 0)
        self.assertTrue(len(n.rel) == 1)
        self.assertTrue(n in n.rel)
        self.assertTrue(n.par is None)
        self.assertTrue(n.point is p)
        self.assertTrue(n.level == 5)

    def testaddrel(self):
        a = Node(Point([1, 2], Euclidean()), 2)
        b = Node(Point([5, 7], Euclidean()), 2)
        a.addrel(b)
        self.assertTrue(b in a.rel)
        self.assertTrue(a in b.rel)

    def testaddch(self):
        a = Node(Point([1, 2], Euclidean()), 2)
        b = Node(Point([5, 7], Euclidean()), 2)
        c = Node(Point([5, 6], Euclidean()), 3)
        a.addch(c)
        self.assertTrue(c in a.ch)
        self.assertTrue(a is c.par)
        b.addch(c)
        self.assertTrue(c in b.ch)
        self.assertTrue(b is c.par)
        self.assertTrue(c not in a.ch)

    def testsetpar(self):
        a = Node(Point([1, 2], Euclidean()), 2)
        b = Node(Point([5, 7], Euclidean()), 2)
        c = Node(Point([5, 6], Euclidean()), 3)
        c.setpar(a)
        self.assertTrue(c in a.ch)
        self.assertTrue(a is c.par)
        c.setpar(b)
        self.assertTrue(c in b.ch)
        self.assertTrue(b is c.par)
        self.assertTrue(c not in a.ch)

    def testgetchild(self):
        b = Node(Point([5, 7], Euclidean()), 2)
        c = Node(Point([5, 6], Euclidean()), 3)
        b.addch(c)
        self.assertEqual(b.getchild(), c)
        d = Node(Point([4, 6], Euclidean()), 3)
        b.addch(d)
        self.assertTrue(b.getchild() in {c, d})
        
    def testch(self):
        a = Node(Point([1, 2], Euclidean()), 3)
        b = Node(Point([5, 7], Euclidean()), 2)
        c = Node(Point([5, 6], Euclidean()), 2)
        d = Node(Point([2, 4], Euclidean()), 1)
        a.addch(b)
        a.addch(c)
        b.addch(d)
        self.assertSetEqual(ch(a), {b, c})
        self.assertSetEqual(ch({a, b}), {b, c, d})
    
    def testpar(self):
        a = Node(Point([1, 2], Euclidean()), 3)
        b = Node(Point([5, 7], Euclidean()), 2)
        c = Node(Point([5, 6], Euclidean()), 2)
        d = Node(Point([2, 4], Euclidean()), 3)
        b.setpar(a)
        c.setpar(d)
        self.assertEqual(par(b), a)
        self.assertSetEqual(par({b, c}), {a, d})
    
    def testrel(self):
        a = Node(Point([1, 2], Euclidean()), 2)
        b = Node(Point([5, 7], Euclidean()), 2)
        c = Node(Point([5, 6], Euclidean()), 2)
        d = Node(Point([2, 4], Euclidean()), 2)
        a.addrel(b)
        c.addrel(b)
        c.addrel(d)
        self.assertSetEqual(rel(a), {a, b})
        self.assertSetEqual(rel({a, c}), {a, b, c, d})
        
    def testnearest(self):
        a = Node(Point([1, 2], Euclidean()), 3)
        b = Node(Point([1, 10], Euclidean()), 2)
        c = Node(Point([5, 6], Euclidean()), 2)
        d = Node(Point([4, 6], Euclidean()), 3)
        self.assertEqual(nearest(a, {b}), b)
        self.assertEqual(nearest(a, {b, c, d}), d)
        
    def testdist(self):
        a = Node(Point([1, 2], Euclidean()), 3)
        b = Node(Point([4, 6], Euclidean()), 2)
        self.assertEqual(dist(a, b), 5)

if __name__ == '__main__':
    unittest.main()
