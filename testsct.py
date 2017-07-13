import unittest
from sct import SCT
from point import Point


class TestSCT(unittest.TestCase):
    def testinit(self):
        T = SCT(3,1,2)
        self.assertEqual(T.tau, 3)
        self.assertEqual(T.cp, 1)
        self.assertEqual(T.cc, 2)
        self.assertTrue(hasattr(T, 'cr'))
        self.assertTrue(hasattr(T, 'root'))

    def testsetroot(self):
        T = SCT(3,1,2)
        rootpoint = Point(1,2,3,4,5)
        T.setroot(rootpoint)
        self.assertEqual(T.root.point, rootpoint)

    def testsplitbelow_root(self):
        T = SCT(3,1,1)
        T.setroot(Point(0))
        n = T.splitbelow(T.root, 1)
        self.assertEqual(n.point, T.root.point)
        self.assertEqual(n.level, 1)
        self.assertEqual(n.par, T.root)
        self.assertEqual(T.root.ch, {n})
        self.assertTrue(n in T.root.ch)
        self.assertEqual(len(n.ch), 0)
        self.assertEqual(n.rel, {n})

    def testsplitbelow_leaf(self):
        T = SCT(3,1,1)
        T.setroot(Point(0))
        a = T.splitbelow(T.root, 10)
        n = T.splitbelow(a, 0)
        self.assertEqual(n.point, a.point)
        self.assertEqual(n.level, 0)
        self.assertEqual(n.par, a)
        self.assertEqual(a.ch, {n})
        self.assertTrue(n in a.ch)
        self.assertTrue(n not in T.root.ch)
        self.assertEqual(len(n.ch), 0)
        self.assertEqual(n.rel, {n})

    def testsplitbelow_actualsplit(self):
        T = SCT(3,1,1)
        T.setroot(Point(0))
        a = T.splitbelow(T.root, 10)
        b = T.splitbelow(a, 0)
        n = T.splitbelow(a, 5)
        self.assertEqual(n.level, 5)
        self.assertEqual(n.ch, {b})
        self.assertEqual(n.par, a)
        self.assertEqual(b.par, n)
        self.assertEqual(a.ch, {n})

    def testsplitabove(self):
        T = SCT(4,1,1)
        T.setroot(Point(0))
        a = T.splitbelow(T.root, 10)
        b = T.splitbelow(a, 0)
        n = T.splitabove(b, 5)
        self.assertEqual(n.level, 5)
        self.assertEqual(n.ch, {b})
        self.assertEqual(n.par, a)
        self.assertEqual(b.par, n)
        self.assertEqual(a.ch, {n})

    def testinsert_onepointafterroot(self):
        T = SCT(4,1,1)
        # The test assumes cr will equal 4
        T.setroot(Point(0,0))
        T.insert(Point(6,0), T.root)
        #  Check root got split below
        a = next(iter(T.root.ch))
        self.assertEqual(a.point, T.root.point)
        self.assertEqual(a.level, 2)
        self.assertEqual(len(a.ch), 2)
        b,c = tuple(child for child in a.ch)
        self.assertTrue(b.point is not c.point)
        self.assertEqual(b.level, 1)
        self.assertEqual(c.level, 1)
        self.assertEqual(len(b.ch), 0)
        self.assertEqual(len(c.ch), 0)

    def testconstruct(self):
        points = [Point(x, 0, 1) for x in [8,1,2,32,64,80,81,160]]
        T = SCT(4,1,1)
        T.construct(points)
        # I printed this tree and it looked right.
        # Should replace with a real test.
        # print(T)

if __name__ == '__main__':
    unittest.main()
