import unittest
from sct import SCT
from point import Point
from metrics import Euclidean
from sct_node import SCTNode
from ntverify import ntverify


class TestSCT(unittest.TestCase):
    
    def testfinduncomplevels(self):
        T = SCT(2, 1, 1, 4)
        p1 = Point([0], Euclidean())
        p2 = Point([2], Euclidean())
        p3 = Point([11], Euclidean())
        p4 = Point([28], Euclidean())
        T.setroot(p1)
        T.insert(p2, T.root)
        T.insert(p3, T.root)
        T.insert(p4, [ch for ch in T.root.getchild().ch if ch.point == p3][0])
        ver = ntverify(T, [p1, p2, p3, p4])
        ver.finduncomplevels()
        self.assertEqual(len(ver.uncomplevels), 7)
        self.assertEqual(next(iter(ver.uncomplevels[5])).point, p1)
        self.assertEqual(next(iter(ver.uncomplevels[5])).level, 5)
        self.assertEqual({n.point for n in ver.uncomplevels[4]}, {p1, p4})
        self.assertEqual(len([n.level for n in ver.uncomplevels[4] if n.level == 4]), 2)
        self.assertEqual({n.point for n in ver.uncomplevels[3]}, {p1, p3, p4})
        self.assertEqual(len([n.level for n in ver.uncomplevels[3] if n.level == 3]), 3)
        self.assertEqual({n.point for n in ver.uncomplevels[2]}, {p1, p3, p4})
        self.assertEqual(len([n.level for n in ver.uncomplevels[2] if n.level == 2]), 2)
        self.assertEqual(len([n.level for n in ver.uncomplevels[2] if n.level == 3]), 1)
        self.assertEqual({n.point for n in ver.uncomplevels[1]}, {p1, p3, p4})
        self.assertEqual(len([n.level for n in ver.uncomplevels[1] if n.level == 1]), 1)
        self.assertEqual(len([n.level for n in ver.uncomplevels[1] if n.level == 2]), 1)
        self.assertEqual(len([n.level for n in ver.uncomplevels[1] if n.level == 3]), 1)
        self.assertEqual({n.point for n in ver.uncomplevels[0]}, {p1, p2, p3, p4})
        self.assertEqual(len([n.level for n in ver.uncomplevels[0] if n.level == 0]), 2)
        self.assertEqual(len([n.level for n in ver.uncomplevels[0] if n.level == 2]), 1)
        self.assertEqual(len([n.level for n in ver.uncomplevels[0] if n.level == 3]), 1)
        self.assertEqual({n.point for n in ver.uncomplevels[-1]}, {p1, p2, p3, p4})
        self.assertEqual(len([n.level for n in ver.uncomplevels[-1] if n.level == -1]), 2)
        self.assertEqual(len([n.level for n in ver.uncomplevels[-1] if n.level == 2]), 1)
        self.assertEqual(len([n.level for n in ver.uncomplevels[-1] if n.level == 3]), 1)
        
    def testfindminlevelrels(self):
        T = SCT(2, 1, 1, 4)
        p1 = Point([0], Euclidean())
        p2 = Point([2], Euclidean())
        p3 = Point([11], Euclidean())
        p4 = Point([28], Euclidean())
        T.setroot(p1)
        T.insert(p2, T.root)
        T.insert(p3, T.root)
        T.insert(p4, [ch for ch in T.root.getchild().ch if ch.point == p3][0])
        ver = ntverify(T, [p1, p2, p3, p4])
        ver.findminlevelrels()
        self.assertEqual(ver.minlevels[(p1, p1)], float('-inf'))
        self.assertEqual(ver.minlevels[(p2, p2)], float('-inf'))
        self.assertEqual(ver.minlevels[(p3, p3)], float('-inf'))
        self.assertEqual(ver.minlevels[(p4, p4)], float('-inf'))
        self.assertEqual(ver.minlevels[(p1, p2)], -1)
        self.assertEqual(ver.minlevels[(p1, p3)], 2)
        self.assertEqual(ver.minlevels[(p1, p4)], 3)
        self.assertEqual(ver.minlevels[(p2, p3)], 2)
        self.assertEqual(ver.minlevels[(p2, p4)], 3)
        self.assertEqual(ver.minlevels[(p3, p4)], 3)
    
    def testfindleaves(self):
        T = SCT(3, 1, 1)
        T.root = SCTNode(Point([0], Euclidean()), float('inf'))
        n1 = SCTNode(Point([1], Euclidean()), 3)
        n2 = SCTNode(Point([2], Euclidean()), 3)
        n3 = SCTNode(Point([3], Euclidean()), 2)
        n4 = SCTNode(Point([4], Euclidean()), 2)
        n5 = SCTNode(Point([5], Euclidean()), 1)
        n6 = SCTNode(Point([6], Euclidean()), 1)
        T.root.addch(n1)
        T.root.addch(n2)
        n1.addch(n3)
        n1.addch(n4)
        n4.addch(n5)
        n4.addch(n6)
        ver = ntverify(T, [])
        dic = dict()
        ver.findleaves(T.root, dic)
        self.assertEqual(dic[T.root], {n2, n3, n5, n6})
        self.assertEqual(dic[n1], {n3, n5, n6})
        self.assertEqual(dic[n2], {n2})
        self.assertEqual(dic[n3], {n3})
        self.assertEqual(dic[n4], {n5, n6})
        self.assertEqual(dic[n5], {n5})
        self.assertEqual(dic[n6], {n6})
        
    def testrelativescorrect(self):
        T = SCT(2, 1, 1, 4)
        p1 = Point([0], Euclidean())
        p2 = Point([2], Euclidean())
        p3 = Point([11], Euclidean())
        p4 = Point([28], Euclidean())
        T.setroot(p1)
        T.insert(p2, T.root)
        T.insert(p3, T.root)
        T.insert(p4, [ch for ch in T.root.getchild().ch if ch.point == p3][0])
        ver = ntverify(T, [p1, p2, p3, p4])
        ver.populate()
        self.assertTrue(ver.relativescorrect())
        [n for n in ver.uncomplevels[2] if n.point == p1][0].rel.discard([n for n in ver.uncomplevels[2] if n.point == p3][0])
        self.assertFalse(ver.relativescorrect())
        
    def testissemicompressed(self):
        T = SCT(2, 1, 1, 4)
        p1 = Point([0], Euclidean())
        p2 = Point([2], Euclidean())
        p3 = Point([11], Euclidean())
        p4 = Point([28], Euclidean())
        T.setroot(p1)
        T.insert(p2, T.root)
        T.insert(p3, T.root)
        T.insert(p4, [ch for ch in T.root.getchild().ch if ch.point == p3][0])
        ver = ntverify(T, [p1, p2, p3, p4])
        ver.populate()
        self.assertTrue(ver.issemicompressed())
        n1 = [n for n in ver.uncomplevels[2] if n.point == p3][0]
        n2 = SCTNode(p3, 1)
        n2.addch(n1.getchild())
        n1.addch(n2)
        ver.populate()
        self.assertFalse(ver.issemicompressed())
        
    def testislocalnettree(self):
        T = SCT(2, 1, 1, 4)
        p1 = Point([0], Euclidean())
        p2 = Point([2], Euclidean())
        p3 = Point([11], Euclidean())
        p4 = Point([28], Euclidean())
        T.setroot(p1)
        T.insert(p2, T.root)
        T.insert(p3, T.root)
        T.insert(p4, [ch for ch in T.root.getchild().ch if ch.point == p3][0])
        ver = ntverify(T, [p1, p2, p3, p4])
        ver.populate()
        self.assertTrue(ver.islocalnettree())
        p3.coords = [8]
        self.assertFalse(ver.islocalnettree())
        p3.coords = [17]
        self.assertFalse(ver.islocalnettree())
        p3.coords = [11]
        self.assertTrue(ver.islocalnettree())
        n1 = [n for n in ver.uncomplevels[3] if n.point == p1][0]
        n1.point = Point([1], Euclidean())
        self.assertFalse(ver.islocalnettree())
        
    def testisglobalnettree(self):
        T = SCT(2, 1, 1, 4)
        p1 = Point([0], Euclidean())
        p2 = Point([2], Euclidean())
        p3 = Point([11], Euclidean())
        p4 = Point([28], Euclidean())
        T.setroot(p1)
        T.insert(p2, T.root)
        T.insert(p3, T.root)
        T.insert(p4, [ch for ch in T.root.getchild().ch if ch.point == p3][0])
        ver = ntverify(T, [p1, p2, p3, p4])
        ver.populate()
        self.assertTrue(ver.isglobalnettree())
        p2.coords = [9]
        self.assertFalse(ver.isglobalnettree())
        p2.coords = [2]
        p3.coords = [10]
        self.assertFalse(ver.isglobalnettree())
        p3.coords = [11]
        self.assertTrue(ver.isglobalnettree())
        n1 = [n for n in ver.uncomplevels[3] if n.point == p1][0]
        n1.point = Point([1], Euclidean())
        self.assertFalse(ver.isglobalnettree())
    
if __name__ == '__main__':
    unittest.main()
