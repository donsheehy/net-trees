"""
A base class for different point location algorithms
"""
from abc import ABC, abstractmethod
from node import dist, ch, rel
import functools

class PointLocation(ABC):
    def __init__(self, tree):
        self.tree = tree
        
    @abstractmethod
    def nn(self, point): 
        pass
    
    @abstractmethod
    def nndist(self, point, nn = None):
        pass
    
    @abstractmethod
    def removepoint(self, point):
        pass
    
    @abstractmethod
    def addnode(self, node):
        pass
    
    @abstractmethod
    def updateonremoval(self, node):
        pass
    
    @abstractmethod
    def updateoninsertion(self, node):
        pass
    
    @abstractmethod
    def updateonsplit(self, node):
        pass
    
class ParallelPointLocation(PointLocation):
    def __init__(self, tree, points):
        PointLocation.__init__(self, tree)
        
    def nn(self, point):
        child = self.tree.root.getchild()
        if child.level == float('-inf'):
            return self.tree.root
        return self.nnhelper(point, {child}, child.level) or self.tree.root
    
    def nnhelper(self, point, currentnodes, level):
        if point.distto(*[n.point for n in currentnodes]) > self.tree.cr * self.tree.tau ** level:    
            return None
        nextnodes = {n if n.level == level - 1 else n.par 
                     for n in ch(currentnodes) if dist(n, point) <= self.tree.cr * self.tree.tau ** level}
        nn = self.nnhelper(point, nextnodes, level - 1)
        return nn if nn else min(currentnodes, key = lambda n : point.distto(n.point))
    
    def nndist(self, point, nn = None):
        return dist(nn or self.nn(point), point)
    
    def removepoint(self, point): pass
    
    def addnode(self, node): pass
    
    def updateonremoval(self, node): pass
    
    def updateoninsertion(self, node): pass
    
    def updateonsplit(self, node): pass
    
class SinglePathPointLocation(PointLocation):
    def __init__(self, tree, points):
        PointLocation.__init__(self, tree)
        
    def nn(self, point):
        currentnode = self.tree.root
        nextnode = self.tree.root.getchild()
#         closestdist = dist(nextnode, point)
#         while closestdist <= self.tree.cr * self.tree.tau ** nextnode.level:
#             currentnode = nextnode
#             allnodes = ch(rel(currentnode))
#             nextnode = allnodes.pop()
#             closestdist = dist(nextnode, point)
#             for n in allnodes:
#                 newdist = dist(n,point)
#                 if newdist < closestdist and newdist <= self.tree.cr * self.tree.tau ** n.level:
#                     nextnode, closestdist = n, newdist
        while dist(nextnode, point) <= self.tree.cr * self.tree.tau ** nextnode.level:
            currentnode = nextnode
            allnodes = ch(rel(currentnode))
            nextlevel = max(n.level for n in allnodes)
            nextnode = min(allnodes, 
                           key = functools.partial(self.mincoveringdist, point = point, level = nextlevel))
        return currentnode
    
    def mincoveringdist(self, node, point, level):
        dst = dist(node, point)
        return dst if dst <= self.tree.cr * self.tree.tau ** level else float('inf')
    
    def nndist(self, point, nn = None):
        return dist(nn or self.nn(point), point)
    
    def removepoint(self, point): pass
    
    def addnode(self, node): pass
    
    def updateonremoval(self, node): pass
    
    def updateoninsertion(self, node): pass
    
    def updateonsplit(self, node): pass