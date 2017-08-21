from snt import SNT
from node import *
from math import ceil, log

class SNTVerify:
    def __init__(self, T, points):
        self.points = points
        self.T = T
        self.uncomplevels = dict()
        self.minlevels = dict()
        
    def populate(self):
        self.finduncomplevels()
        self.findminlevelrels()
        
    def islocalnettree(self):
        if self.T.root.getchild() is None:
            return True
        q = [self.T.root.getchild()]
        for node in q:
            # nesting
            if len(node.ch) > 0 and node.point not in [ch.point for ch in node.ch]:
                print('Violates LNT nesting')
                return False
            # parent
            for par in rel(node.par):
                if dist(node, node.par) > dist(node, par):
                    print('Violates LNT parent')
                    return False
            for ch1 in node.ch:
                q.append(ch1)
                # covering
                if dist(node, ch1) > self.T.cc * self.T.tau ** node.level:
                    print('Violates LNT covering')
                    return False
                # packing
                for ch2 in node.ch:
                    if ch1 != ch2 and dist(ch1, ch2) <= self.T.cp * self.T.tau ** max(ch1.level, ch2.level):
                        print('Violates LNT packing')
                        return False
        return True
    
    def isglobalnettree(self):
        if self.T.root.getchild() is None:
            return True
        q = [self.T.root.getchild()]
        dictnry = dict()
        self.findleaves(self.T.root, dictnry)
        for node in q:
            # nesting
            if len(node.ch) > 0 and node.point not in [ch.point for ch in node.ch]:
                print('Violates NT nesting')
                return False
            # covering
            for leaf in dictnry[node]:
                if dist(node, leaf) > self.T.cc * self.T.tau ** node.level:
                    print('Violates NT covering')
                    return False
            # packing
            others = [n.point for n in dictnry[self.T.root] - dictnry[node]]
            if len(others) > 0 and node.point.distto(*others) <= self.T.cp * self.T.tau ** node.level:
                print('Violates NT packing')
                return False
            for ch1 in node.ch:
                q.append(ch1)
        return True
    
    def findleaves(self, node, dictnry):
        leaves = [self.findleaves(ch, dictnry) for ch in node.ch]
        dictnry[node] = set().union(*leaves) if len(leaves) > 0 else {node} 
        return dictnry[node]
    
    def issemicompressed(self):
        for level in self.uncomplevels:
            for n1 in self.uncomplevels[level]:
                if len(n1.ch) > 1: 
                    continue
                relno = 0
                for n2 in self.uncomplevels[level] - {n1}:                    
                    if self.minlevels[(n1.point, n2.point)] <= level:
                        relno += 1
                if (relno == 0 and n1.level == level) or (relno > 0 and n1.level != level):
                    return False
        return True
                    
    def relativescorrect(self):
        for level in self.uncomplevels:
            for n1 in self.uncomplevels[level]:
                for n2 in self.uncomplevels[level] - {n1}:
                    if self.minlevels[(n1.point, n2.point)] <= level and (n1 not in n2.rel or n2 not in n1.rel):
                        return False
        return True
        
    def finduncomplevels(self):
        if self.T.root.getchild() is None or self.T.root.getchild().level == float('-inf'):
            return dict()
        q = [self.T.root.getchild()]
        self.uncomplevels = dict()
        dictp2n = dict()  # keeps the lowest node for each point
        for node in q:
            if dictp2n.get(node.point) is None or dictp2n[node.point].level > node.level:
                dictp2n[node.point] = node
            bottomlevel = node.level - 1 if node.getchild().level == float('-inf') else node.getchild().level        
            for i in range(bottomlevel + 1, node.level + 1):
                self.uncomplevels[i] = self.uncomplevels.get(i, set()) | {node}
            for ch1 in node.ch:
                if ch1.level > float('-inf'):
                    q.append(ch1)
        lowest = sorted(self.uncomplevels)[0]
        for node in dictp2n.values():
            for i in range(lowest, node.level):
                self.uncomplevels[i] = self.uncomplevels.get(i, set()) | {node}
        return self.uncomplevels
                
    def findminlevelrels(self):
        self.minlevels = dict()
        for p1 in self.points:
            for p2 in self.points:
                self.minlevels[(p1, p2)] = float('-inf') if p1 == p2 else self.T.minlevel(p1, p2)
        return self.minlevels
        
