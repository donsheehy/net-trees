import unittest
from snt import SNT
from snt_pointlocation import SNTPointLocation
from point import *
from metrics import Euclidean
from node import Node


class TestSNTPointLocation(unittest.TestCase):
    def testinit(self):
        T = SNT(3, 1, 1)
        T.setroot(Point([0], Euclidean()))
        points = [Point([i], Euclidean()) for i in [1, 2, 4, 8]]
        ploc = SNTPointLocation(T, points)
        for p in points:
            self.assertEqual(ploc._nn[p], T.root)
        self.assertEqual(len(ploc._rnn_in), 1)
        self.assertEqual(len(ploc._rnn_out), 1)
        self.assertEqual(ploc._rnn_in[T.root], set(points))
        self.assertEqual(len(ploc._rnn_out[T.root]), 0)
        
    def testaddnode(self):
        T = SNT(3, 1, 1)
        T.setroot(Point([0], Euclidean()))
        ploc = SNTPointLocation(T, [])
        a = Node(Point([1], Euclidean()), 2)
        ploc.addnode(a)
        self.assertEqual(ploc._rnn_in[a], set())
        self.assertEqual(ploc._rnn_out[a], set())
        
    def testrnn(self):
        T = SNT(3, 1, 1)
        T.setroot(Point([0], Euclidean()))
        ploc = SNTPointLocation(T, [])
        a = Point([1], Euclidean())
        b = Point([2], Euclidean())
        c = Point([3], Euclidean())
        d = Point([4], Euclidean())
        n = Node(Point([10], Euclidean()), 3)
        ploc.addnode(n)
        ploc._rnn_in[T.root] = {a}
        ploc._rnn_out[T.root] = {b}
        ploc._rnn_in[n] = {c}
        ploc._rnn_out[n] = {d}
        self.assertEqual(ploc.rnn_in(T.root), {a})
        self.assertEqual(ploc.rnn_out(T.root), {b})
        self.assertEqual(ploc.rnn_in(n), {c})
        self.assertEqual(ploc.rnn_out(n), {d})
        self.assertEqual(ploc.rnn_in([T.root, n]), {a, c})
        self.assertEqual(ploc.rnn_out([T.root, n]), {b, d})
        self.assertEqual(ploc.rnn([T.root, n]), {a, b, c, d})
    
    def testupdateonsplit(self):
        T = SNT(3, 1, 1)
        T.tau = 2
        T.cr = 3
        r = Point([0], Euclidean())
        T.setroot(r)
        ploc = SNTPointLocation(T, [])
        a = Point([1], Euclidean())
        b = Point([8], Euclidean())
        c = Point([13], Euclidean())
        d = Point([30], Euclidean())
        e = Point([63], Euclidean())
        f = Point([96], Euclidean())
        n1 = Node(r, 7)
        n2 = Node(r, 3)
        n1.addch(n2)
        ploc._rnn_in[n1] = {a, b, c, d}
        ploc._rnn_out[n1] = {e, f}
        ploc._nn[a] = ploc._nn[b] = ploc._nn[c] = ploc._nn[d] = ploc._nn[e] = ploc._nn[f] = n1
        ploc.updateonsplit(n2)
        self.assertEqual(ploc._rnn_in[n1], {d})
        self.assertEqual(ploc._rnn_out[n1], {e, f})
        self.assertEqual(ploc._rnn_in[n2], {a})
        self.assertEqual(ploc._rnn_out[n2], {b, c})
        
    def testupdate(self):
        T = SNT(3, 1, 1)
        T.cr = 2
        p1 = Point([0], Euclidean())
        p2 = Point([10], Euclidean())
        p3 = Point([40], Euclidean())
        p4 = Point([120], Euclidean())
        p5 = Point([130], Euclidean())
        p6 = Point([160], Euclidean())
        p7 = Point([20], Euclidean())
        p8 = Point([26], Euclidean())
        p9 = Point([38], Euclidean())
        p10 = Point([-60], Euclidean())
        p11 = Point([70], Euclidean())
        p12 = Point([300], Euclidean())
        p13 = Point([80], Euclidean())
        p14 = Point([105], Euclidean())
        p15 = Point([140], Euclidean())
        n1 = Node(p1, 4)
        n2 = Node(p1, 3)
        n3 = Node(p1, 2)
        n4 = Node(p3, 3)
        n5 = Node(p2, 2)
        n6 = Node(p6, 4)
        n7 = Node(p6, 3)
        n8 = Node(p5, 3)
        n9 = Node(p5, 2)
        n10 = Node(p4, 2)
        n1.addch(n2)
        n1.addch(n4)
        n2.addch(n3)
        n2.addch(n5)
        n6.addch(n7)
        n6.addch(n8)
        n8.addch(n9)
        n8.addch(n10)
        n1.addrel(n6)
        n2.addrel(n4)
        n3.addrel(n5)
        n7.addrel(n8)
        n9.addrel(n10)
        ploc = SNTPointLocation(T, [])
        ploc._nn[p7] = ploc._nn[p8] = n5
        ploc._nn[p9] = n2
        ploc._nn[p10] = ploc._nn[p11] = n1
        ploc._nn[p12] = n6
        ploc._nn[p13] = n8
        ploc._nn[p14] = n10
        ploc._nn[p15] = n9
        ploc._rnn_out[n1] = {p10, p11}
        ploc._rnn_out[n2] = {p9}
        ploc._rnn_out[n3] = set()
        ploc._rnn_out[n5] = {p7, p8}
        ploc._rnn_out[n6] = {p12}
        ploc._rnn_out[n7] = set()
        ploc._rnn_out[n8] = {p13}
        ploc._rnn_out[n9] = {p15}
        ploc._rnn_out[n10] = {p14}
        ploc._rnn_in[n1] = ploc._rnn_in[n2] = ploc._rnn_in[n3] = ploc._rnn_in[n5] = set()
        ploc._rnn_in[n6] = ploc._rnn_in[n7] = ploc._rnn_in[n8] = ploc._rnn_in[n9] = ploc._rnn_in[n10] = set()
        ploc.update(n4)
        self.assertEqual(ploc._rnn_in[n4], {p9})
        self.assertEqual(ploc._rnn_out[n4], {p8, p11, p13})
        self.assertTrue(ploc._nn[p8] == ploc._nn[p9] == ploc._nn[p11] == ploc._nn[p13] == n4)
        self.assertEqual(ploc._rnn_out[n1], {p10})
        self.assertEqual(ploc._rnn_out[n2], set())
        self.assertEqual(ploc._rnn_out[n5], {p7})
        self.assertEqual(ploc._rnn_out[n6], {p12})
        self.assertEqual(ploc._rnn_out[n8], set())
        self.assertEqual(ploc._rnn_out[n9], {p15})
        self.assertEqual(ploc._rnn_out[n10], {p14})
        self.assertEqual(ploc._nn[p7], n5)
        self.assertEqual(ploc._nn[p10], n1)
        self.assertEqual(ploc._nn[p12], n6)
        self.assertEqual(ploc._nn[p14], n10)
        self.assertEqual(ploc._nn[p15], n9)
    
if __name__ == '__main__':
    unittest.main()
