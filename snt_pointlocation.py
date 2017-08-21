from node import *

"""
The point location structure is responsible for mapping points to their nearest
nodes.  It also maps nodes to their sets of reverse nearest neighbors (rnn's).
The rnn's are split into two groups, in and out, depending on their distance
to the node relative to the level of the node.
"""

class SNTPointLocation:
    def __init__(self, tree, points):
        self.tree = tree
        self._nn = {p : tree.root for p in points}
        self._rnn_in = {tree.root : set(points)}
        self._rnn_out = {tree.root : set()}

    def rnn_in(self, nodes):
        return self._rnn_in[nodes] if isinstance(nodes, Node) else \
                set.union(*(self._rnn_in[node] for node in nodes))

    def rnn_out(self, nodes):
        return self._rnn_out[nodes] if isinstance(nodes, Node) else \
                set.union(*(self._rnn_out[node] for node in nodes))

    def rnn(self, nodes):
        return self.rnn_in(nodes) | self.rnn_out(nodes)

    def nn(self, point):
        return self._nn[point]
    
    def removepoint(self, point):
        self._rnn_in[self.nn(point)].discard(point)
        self._rnn_out[self.nn(point)].discard(point)
        self._nn.pop(point, None)

    def addnode(self, node):
        if node not in self._rnn_in:
            self._rnn_in[node] = set()
            self._rnn_out[node] = set()

    def update(self, node):
        self.addnode(node)
        for point in self.rnn_out(rel(par(node)) | ch(rel(par(node))) | ch(rel(node))):
            self.trytochangernn(point, node)

    def updateonsplit(self, node):
        self.addnode(node)
        if node.level != float('-inf'):
            for point in self.rnn(par(node)):
                self.trytochangernn(point, node)

    def changernn(self, point, fromnode, tonode, todist):
        self._nn[point] = tonode
        if self.tree.iscloserel(tonode, point, todist):
            self._rnn_in[tonode].add(point)
        else:
            self._rnn_out[tonode].add(point)
        self._rnn_in[fromnode].discard(point)
        self._rnn_out[fromnode].discard(point)

    def trytochangernn(self, point, tonode):
        fromnode = self._nn[point]
        todist = point.distto(tonode.point)
        if self.tree.isrel(tonode, point, todist):
            if (fromnode.point == tonode.point and fromnode.level > tonode.level) or \
                    (fromnode.point != tonode.point and todist < fromnode.point.distto(point)):
                self.changernn(point, fromnode, tonode, todist)
