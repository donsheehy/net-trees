from snt import SNT
from point import *
from metrics import *

class SNTStats:
    def __init__(self, T):
        self.T = T
        self.levels = set()
        
    # not count +infty, -infty and the highest level below +infty
    def nodeno(self):
        return self.dfssearch(self.T.root.getchild(), lambda node:1) - 1
    
    # not count -infty
    def childno(self):
        return self.dfssearch(self.T.root.getchild(),
                              lambda node:0 if node.getchild().level == float('-inf') else len(node.ch))
    
    # not count +infty, -infty and the highest level below +infty
    def relno(self):
        return self.dfssearch(self.T.root.getchild(), lambda node:len(node.rel)) - 1
    
    # not count +infty, -infty and the highest level below +infty
    def levelno(self):
        self.levels = set()
        return self.dfssearch(self.T.root.getchild(), self.levellambda) - 1
        
    def levellambda(self, node):
        if node.level in self.levels: return 0
        self.levels.add(node.level)
        return 1
    
    # not count edges from +infty and to -infty
    def jumpno(self):
        return self.dfssearch(self.T.root.getchild(),
                              lambda node:1 if len(node.ch) == 1 and node.level > node.getchild().level + 1 and 
                              node.getchild().level != float('-inf') else 0)
        
    def dfssearch(self, node, lmda):        
        if node.level == float('-inf'):
            return 0
        if (node.ch) == 1 and node.getchild().level == float('-inf'): return lmda(node)      
        count = 0
        for ch in node.ch:
            count += self.dfssearch(ch, lmda)
        return count + lmda(node)
