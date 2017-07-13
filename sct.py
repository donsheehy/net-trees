import math
from sct_node import *
from sct_pointlocation import *

class SCT:
    def __init__(self, tau, cp, cc):
        self.tau = tau
        self.cp = cp
        self.cc = cc
        self.cr = (2 * cc * tau) / (tau - 2)
        self.root = None

    def setroot(self, point):
        self.root = SCTNode(point, 2 ** 100)

    def construct(self, points):
        # Should shuffle the points first!!
        self.setroot(points.pop())
        self.ploc = SCTPointLocation(self, points)
        for p in points:
            self.insert(p)

    def insert(self, point, closest = None):
        closest = closest or self.ploc.nn(point)
        level = math.ceil(math.log(dist(closest, point) / self.cr, self.tau) )
        if level < closest.level:
            closest = self.splitbelow(closest, level)
        node = SCTNode(point, level)
        self.update(node, closest)
        while not self.iscovered(node):
            node = self.promote(node)

    def promote(self, node):
        newnode = SCTNode(node.point, node.level + 1)
        self.update(newnode, node.par)
        return newnode

    def update_rel(self, node, closest):
        for other in ch(rel(par(closest))):
            if self.isrel(node, other):
                if other.level < node.level:
                    other = self.splitabove(other, node.level)
                node.addrel(other)

    def update_ch(self, node):
        for other in ch(rel(node)):
            if dist(node, other) < dist(other, other.par):
                node.addch(other)

    def update_par(self, node):
        newpar = nearest(node, par(rel(node)))
        if newpar.level > node.level + 1:
            newpar = self.splitbelow(newpar, node.level + 1)
        node.setpar(newpar)

    def update(self, node, closest):
        self.update_rel(node, closest)
        self.update_ch(node)
        self.update_par(node)
        if hasattr(self, 'ploc'): self.ploc.update(node)

    def splitbelow(self, node, level):
        # Assumes a long edge or leaf
        newnode = SCTNode(node.point, level)
        if node.ch: newnode.addch(node.getchild())
        node.ch = set()
        newnode.setpar(node)
        if hasattr(self, 'ploc'): self.ploc.updateonsplit(newnode)
        return newnode

    def splitabove(self, node, level):
        return self.splitbelow(node.par, level)

    def iscovered(self, node):
        return dist(node, node.par) <= self.cc * (self.tau ** (node.level + 1))

    def isrel(self, node, other):
        return dist(node, other) <= self.cr * (self.tau ** node.level)

    def iscloserel(self, node, other):
        return dist(node, other) <= self.cp * (self.tau ** (node.level - 1)) / 2

    def __str__(self):
        return str(self.root)
