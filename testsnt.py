import unittest
from snt import SNT
from point import Point
from metric import Euclidean
from node import Node
from snt_verify import SNTVerify
import random
# from snt_pointlocation import SNTPointLocation as PL
from pointlocation import SinglePathPointLocation as PL

class TestSNT(unittest.TestCase):
    def testinit(self):
        T = SNT(5, 1, 2)
        self.assertEqual(T.tau, 5)
        self.assertEqual(T.cp, 1)
        self.assertEqual(T.cc, 2)
        self.assertEqual(T.cr, 20)
        self.assertTrue(hasattr(T, 'cr'))
        self.assertTrue(hasattr(T, 'root'))

    def testsetroot(self):
        T = SNT(3, 1, 2, 2)
        rootpoint = Point([1, 2, 3, 4, 5], Euclidean())
        T.setroot(rootpoint)
        self.assertEqual(T.root.point, rootpoint)
        self.assertEqual(T.root.level, float('inf'))
        self.assertEqual(T.root.getchild().point, rootpoint)
        self.assertEqual(T.root.getchild().level, float('-inf'))

    def testsplitbelow_root(self):
        T = SNT(3, 1, 1)
        T.setroot(Point([0], Euclidean()))
        n = T.splitbelow(T.root, 1)
        self.assertEqual(n.point, T.root.point)
        self.assertEqual(n.level, 1)
        self.assertEqual(n.par, T.root)
        self.assertEqual(T.root.ch, {n})
        self.assertTrue(n in T.root.ch)
        self.assertEqual(n.getchild().level, float('-inf'))
        self.assertEqual(n.rel, {n})

    def testsplitbelow_leaf(self):
        T = SNT(3, 1, 1)
        T.setroot(Point([0], Euclidean()))
        a = T.splitbelow(T.root, 10)
        n = T.splitbelow(a, 0)
        self.assertEqual(n.point, a.point)
        self.assertEqual(n.level, 0)
        self.assertEqual(n.par, a)
        self.assertEqual(a.ch, {n})
        self.assertTrue(n in a.ch)
        self.assertTrue(n not in T.root.ch)
        self.assertEqual(n.getchild().level, float('-inf'))
        self.assertEqual(n.rel, {n})

    def testsplitbelow_actualsplit(self):
        T = SNT(3, 1, 1)
        T.setroot(Point([0], Euclidean()))
        a = T.splitbelow(T.root, 10)
        b = T.splitbelow(a, 0)
        n = T.splitbelow(a, 5)
        self.assertEqual(n.level, 5)
        self.assertEqual(n.ch, {b})
        self.assertEqual(n.par, a)
        self.assertEqual(b.par, n)
        self.assertEqual(a.ch, {n})

    def testsplitabove(self):
        T = SNT(4, 1, 1, 2)
        T.setroot(Point([0], Euclidean()))
        a = T.splitbelow(T.root, 10)
        b = T.splitbelow(a, 0)
        n = T.splitabove(b, 5)
        self.assertEqual(n.level, 5)
        self.assertEqual(n.ch, {b})
        self.assertEqual(n.par, a)
        self.assertEqual(b.par, n)
        self.assertEqual(a.ch, {n})
        
    def testiscovered(self):
        T = SNT(3, 1, 1)
        metric = Euclidean()
        a = Node(Point([0, 0], metric), 2)
        b = Node(Point([0, 12], metric), 1)
        c = Node(b.point, 0)
        a.addch(b)
        b.addch(c)
        self.assertTrue(T.iscovered(c))
        self.assertEqual(metric.counter, 0)
        self.assertFalse(T.iscovered(b))
        T.cc = 2
        self.assertTrue(T.iscovered(b))
        
    def testisrel(self):
        T = SNT(3, 1, 1, 4)
        metric = Euclidean()
        a = Node(Point([0, 0], metric), 2)
        b = Node(Point([0, 35], metric), 2)
        c = Node(Point([0, 37], metric), 2)
        self.assertTrue(T.isrel(a, a))
        self.assertEqual(metric.counter, 0)
        self.assertTrue(T.isrel(a, b))
        self.assertFalse(T.isrel(a, c))
        self.assertEqual(metric.counter, 2)

    def testinsert_onepointafterroot(self):
        T = SNT(4, 1, 1, 4)
        metric = Euclidean()
        T.setroot(Point([0, 0], metric))
        T.insert(Point([6, 0], metric), T.root)
        #  Check root got split below
        a = next(iter(T.root.ch))
        self.assertEqual(a.point, T.root.point)
        self.assertEqual(a.level, 2)
        self.assertEqual(len(a.ch), 2)
        b, c = tuple(child for child in a.ch)
        self.assertTrue(b.point is not c.point)
        self.assertEqual(b.level, 1)
        self.assertEqual(c.level, 1)
        self.assertEqual(b.getchild().level, float('-inf'))
        self.assertEqual(c.getchild().level, float('-inf'))
        
    def testinsert(self):
        T = SNT(2, 1, 1, 4)
        p1 = Point([0], Euclidean())
        p2 = Point([2], Euclidean())
        p3 = Point([11], Euclidean())
        p4 = Point([28], Euclidean())
        T.setroot(p1)
        T.insert(p2, T.root)
        T.insert(p3, T.root)
        T.insert(p4, [ch for ch in T.root.getchild().ch if ch.point == p3][0])
        self.assertEqual(T.root.getchild().point, p1)
        self.assertEqual(T.root.getchild().level, 5)
        n1 = [ch for ch in T.root.getchild().ch if ch.point == p1][0]
        n2 = [ch for ch in T.root.getchild().ch if ch.point == p4][0]
        self.assertTrue(n1.level == n2.level == 4)
        self.assertEqual(n2.getchild().point, p4)
        self.assertEqual(n2.getchild().level, 3)
        self.assertEqual(n2.getchild().getchild().level, float('-inf'))
        n3 = [ch for ch in n1.ch if ch.point == p1][0]
        n4 = [ch for ch in n1.ch if ch.point == p3][0]
        self.assertTrue(n3.level == n4.level == 3)
        self.assertEqual(n4.getchild().point, p3)
        self.assertEqual(n4.getchild().level, 2)
        self.assertEqual(n4.getchild().getchild().level, float('-inf'))
        self.assertEqual(n3.getchild().point, p1)
        self.assertEqual(n3.getchild().level, 2)
        self.assertEqual(n3.getchild().getchild().point, p1)
        self.assertEqual(n3.getchild().getchild().level, 1)
        n5 = [ch for ch in n3.getchild().getchild().ch if ch.point == p1][0]
        n6 = [ch for ch in n3.getchild().getchild().ch if ch.point == p2][0]
        self.assertTrue(n5.level == n6.level == 0)
        self.assertEqual(n5.getchild().point, p1)
        self.assertEqual(n5.getchild().level, -1)
        self.assertEqual(n6.getchild().point, p2)
        self.assertEqual(n6.getchild().level, -1)
        self.assertEqual(n5.getchild().getchild().level, float('-inf'))
        self.assertEqual(n6.getchild().getchild().level, float('-inf'))
        

    def testconstruct(self):
        T = SNT(2, 1, 1, 4)
        p1 = Point([0], Euclidean())
        p2 = Point([2], Euclidean())
        p3 = Point([11], Euclidean())
        p4 = Point([28], Euclidean())
        T.construct([p2, p3, p4, p1], PL)
        self.assertEqual(T.root.getchild().point, p1)
        self.assertEqual(T.root.getchild().level, 5)
        n1 = [ch for ch in T.root.getchild().ch if ch.point == p1][0]
        n2 = [ch for ch in T.root.getchild().ch if ch.point == p4][0]
        self.assertTrue(n1.level == n2.level == 4)
        self.assertEqual(n2.getchild().point, p4)
        self.assertEqual(n2.getchild().level, 3)
        self.assertEqual(n2.getchild().getchild().level, float('-inf'))
        n3 = [ch for ch in n1.ch if ch.point == p1][0]
        n4 = [ch for ch in n1.ch if ch.point == p3][0]
        self.assertTrue(n3.level == n4.level == 3)
        self.assertEqual(n4.getchild().point, p3)
        self.assertEqual(n4.getchild().level, 2)
        self.assertEqual(n4.getchild().getchild().level, float('-inf'))
        self.assertEqual(n3.getchild().point, p1)
        self.assertEqual(n3.getchild().level, 2)
        self.assertEqual(n3.getchild().getchild().point, p1)
        self.assertEqual(n3.getchild().getchild().level, 1)
        n5 = [ch for ch in n3.getchild().getchild().ch if ch.point == p1][0]
        n6 = [ch for ch in n3.getchild().getchild().ch if ch.point == p2][0]
        self.assertTrue(n5.level == n6.level == 0)
        self.assertEqual(n5.getchild().point, p1)
        self.assertEqual(n5.getchild().level, -1)
        self.assertEqual(n6.getchild().point, p2)
        self.assertEqual(n6.getchild().level, -1)
        self.assertEqual(n5.getchild().getchild().level, float('-inf'))
        self.assertEqual(n6.getchild().getchild().level, float('-inf'))
        
    def testconstructwithverification(self):
        points = [Point([x, 0, 1], Euclidean()) for x in [8, 1, 2, 32, 64, 81, 80, 160]]
        T = SNT(4, 1, 1, 4)
        T.construct(points, PL)
        ver = SNTVerify(T, points)
        ver.populate()
        self.assertTrue(ver.relativescorrect())
        self.assertTrue(ver.issemicompressed())
        self.assertTrue(ver.islocalnettree())
        self.assertFalse(ver.isglobalnettree())
        T.cc = 4 / 3
        T.cp = 1 / 6
        self.assertTrue(ver.isglobalnettree())
        
        points = [Point([x], Euclidean()) for x in [7, 44, 30, 24, 76]]  
        T = SNT(5, 1, 1)
        T.construct(points, PL)
        ver = SNTVerify(T, points)
        ver.populate()
        self.assertTrue(ver.relativescorrect())
        self.assertTrue(ver.issemicompressed())
        self.assertTrue(ver.islocalnettree())
        T.cc = 5 / 4
        T.cp = 1 / 4
        self.assertTrue(ver.isglobalnettree())
        
        points = [Point([x], Euclidean()) for x in [25, 20, 54, 30, 40, 0]] 
        T = SNT(5, 1, 1)
        T.construct(points, PL)
        ver = SNTVerify(T, points)
        ver.populate()
        self.assertTrue(ver.relativescorrect())
        self.assertTrue(ver.issemicompressed())
        self.assertTrue(ver.islocalnettree())
        T.cc = 5 / 4
        T.cp = 1 / 4
        self.assertTrue(ver.isglobalnettree())
        
        points = [Point([x], Euclidean()) for x in [-55,93,-90,-14,-13,-12]]
        T = SNT(7, 1, 1)
        T.construct(points, PL)
        ver = SNTVerify(T, points)
        ver.populate()
        self.assertTrue(ver.relativescorrect())        
        self.assertTrue(ver.islocalnettree())
        self.assertTrue(ver.issemicompressed())
        
        metric = Euclidean()
        points = [Point([random.randint(-10000, 10000) for _ in range(2)], metric) for _ in range(200)] 
        tmp = list()
        for p in points:
            if p in tmp:
                print('duplicate:', p)
            else:
                tmp.append(p)
        points = tmp
        tau = 7
        T = SNT(tau, 1, 1)
        T.construct(points, PL)
        ver = SNTVerify(T, points)
        ver.populate()
        self.assertTrue(ver.relativescorrect())        
        self.assertTrue(ver.islocalnettree())
        self.assertTrue(ver.issemicompressed())
        T.cc = tau / (tau - 1)
        T.cp = (tau - 3) / (2 * (tau - 1))
        self.assertTrue(ver.isglobalnettree())

if __name__ == '__main__':
    unittest.main()
