import math
from snt_pointlocation import *

class SNT:
    def __init__(self, tau, cp, cc, cr=None):
        self.tau = tau
        self.cp = cp
        self.cc = cc
        self.cr = cr or max((2 * cc * tau) / (tau - 4), cc * tau)
        self.root = None

    def setroot(self, point):
        self.root = Node(point, float('inf'))
        self.splitbelow(self.root, float('-inf'))

    def construct(self, points):
        # Should shuffle the points first!!
        points = list(points)
        self.setroot(points.pop())
        self.ploc = SNTPointLocation(self, points)
        self.ploc.addnode(self.root.getchild())
        for p in points:
            self.insert(p)

    def insert(self, point, closest=None):
        closest = closest or self.ploc.nn(point)
        if hasattr(self, 'ploc'): self.ploc.removepoint(point)
        level = self.minlevel(closest, point)
        if level < closest.level:
            closest = self.splitbelow(closest, level)
        node = Node(point, level)
        self.update(node, closest)
        self.splitbelow(node, float('-inf'))
        while not self.iscovered(node):
            node = self.promote(node)

    def promote(self, node):
        newnode = Node(node.point, node.level + 1)
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

    def update_par(self, node, closest):
        newpar = nearest(node, rel(par(closest)))
        if newpar.getchild().level < node.level and self.isrel(node, newpar):
            self.splitbelow(newpar, node.level)
            node.addrel(newpar.getchild())
        node.setpar(newpar)

    def update(self, node, closest):
        if closest.par.level > closest.level + 1:
            self.splitabove(closest, closest.level + 1)
        self.update_rel(node, closest)
        self.update_ch(node)
        self.update_par(node, closest)
        if hasattr(self, 'ploc'): self.ploc.update(node)

    def splitbelow(self, node, level):
        # Assumes a long edge or leaf
        newnode = Node(node.point, level)
        if node.ch: newnode.addch(node.getchild())
        node.ch = set()
        newnode.setpar(node)
        if hasattr(self, 'ploc'): self.ploc.updateonsplit(newnode)
        return newnode

    def splitabove(self, node, level):
        return self.splitbelow(node.par, level)
    
    def minlevel(self, first, second):
        return math.ceil(math.log((first.point if isinstance(first, Node) else first)
                                  .distto(second.point if isinstance(second, Node) else second) / self.cr, self.tau))

    def iscovered(self, node):
        return True if node.point == node.par.point else dist(node, node.par) <= self.cc * (self.tau ** (node.level + 1))

    def isrel(self, node, other, computeddist=None):
        if (isinstance(other, Node) and node.point == other.point) or (isinstance(other, Point) and node.point == other):
            return True
        return (computeddist or dist(node, other)) <= self.cr * (self.tau ** node.level)

    def iscloserel(self, node, other, computeddist=None):
        return (computeddist or dist(node, other)) <= self.cp * (self.tau ** (node.level - 1)) / 2

    def __str__(self):
        return str(self.root)
