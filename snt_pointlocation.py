"""
The point location structure is responsible for mapping points to their nearest
nodes.  It also maps nodes to their sets of reverse nearest neighbors (rnn's).
The rnn's are split into two groups, in and out, depending on their distance
to the node relative to the level of the node.
"""

from node import Node, ch, rel, par, dist
from pointlocation import PointLocation

class SNTPointLocation(PointLocation):
    """
    Declares a point location data structure to track cells and centers.
    
    Parameters:
    ----------
    tree : SNT
        A semi-compressed local net-tree created for one point, which consists of a jump 
        from root at level +\infty to the leaf at level -\infty.
    points: list
        A list of points that are not inserted to the tree.
    """
    def __init__(self, tree, points):
        PointLocation.__init__(self, tree)
        # A dictionary from uninserted points to nodes of the tree, which provides information about centers
        self._nn = {p : tree.root for p in points}
        # A mapping maintaining the distance of each uninserted point to its center
        self._nndist = {p : None for p in points}
        # A dictionary from nodes to uninserted points. 
        # For each node, it gives the set of all uninserted points in its inner cell
        self._rnn_in = {tree.root : set(points)}
        # A dictionary from nodes to uninserted points. 
        # For each node, it provides the set of all uninserted points in its outer cell
        self._rnn_out = {tree.root : set()}

    def rnn_in(self, nodes):
        """
        Returns the uninserted points in the inner cell of given nodes.
        
        Parameters:
        ----------
        nodes : list
            A list of nodes in the net-tree.
            
        Returns:
        -------
        set
            The uninserted points in the inner cell of given nodes.
        """
        return self._rnn_in[nodes] if isinstance(nodes, Node) else \
                set.union(*(self._rnn_in[node] for node in nodes))

    def rnn_out(self, nodes):
        """
        Returns the uninserted points in the outer cell of given nodes.
        
        Parameters:
        ----------
        nodes : list
            A list of nodes in the net-tree.
            
        Returns:
        -------
        set
            The uninserted points in the outer cell of given nodes.
        """
        return self._rnn_out[nodes] if isinstance(nodes, Node) else \
                set.union(*(self._rnn_out[node] for node in nodes))

    def rnn(self, nodes):
        """
        Returns the uninserted points in both the inner and the outer cells of given nodes.
        
        Parameters:
        ----------
        nodes : list
            A list of nodes in the net-tree.
            
        Returns:
        -------
        set
            The uninserted points in the inner and the outer cells of given nodes.
        """
        return self.rnn_in(nodes) | self.rnn_out(nodes)

    def nn(self, point):
        """
        Returns the center of an uninserted point.
        
        Parameters:
        ----------
        point : Point
            An uninserted point.
            
        Returns:
        -------
        Node
            The center of the uninserted point.
        """
        return self._nn[point]
    
    def nndist(self, point, nn = None):
        """
        Returns the distance of point to its center.
        
        Parameters:
        ----------
        point : Point
            An uninserted point.
        nn : Node
            The center of the uninserted point. If nn==None, then the data structure 
            looks up the center in its saved mapping.
            
        Returns:
        -------
        float
            The distance between the uninserted point and its center.
        """
        return self._nndist[point] or dist(nn or self._nn[point], point)
    
    def removepoint(self, point):
        """
        Removes an uninserted point from the point location data structure.
        The removed point will be inserted to the tree later.
        
        Parameters:
        ----------
        point : Point
            An uninserted point.
        """
        self._rnn_in[self.nn(point)].discard(point)
        self._rnn_out[self.nn(point)].discard(point)
        self._nn.pop(point, None)
        self._nndist.pop(point, None)

    def addnode(self, node):
        """
        Creates an inner and an outer cell for the new node.
        Whenever a new node is added to the tree, we need to create an entry for it 
        in the dictionary maintaining inner and outer cells.
        
        Parameters:
        ----------
        node : Node
            A new node recently added to the tree.
        """
        if node not in self._rnn_in:
            self._rnn_in[node] = set()
            self._rnn_out[node] = set()

    def updateonremoval(self, node):
        """
        Moves the uninserted points in the inner and outer cells of a removing node (a node to be compressed 
        later which creates a jump in the tree) to its parent cell. The parent's inner cell receives 
        all points in the node's inner cell. However, points in the outer cell of the node may belong 
        to the inner or outer cells of its parent.
        
        Parameters:
        ----------
        node : Node
            A removing node.
        """
        for point in self.rnn_out(node).copy():
            self.changernn(point, node, node.par, self.nndist(point))
            self._nn[point] = node.par
        self._rnn_out.pop(node)
        for point in self.rnn_in(node):
            self._nn[point] = node.par
        self._rnn_in[node.par].update(self._rnn_in[node])      
        self._rnn_in.pop(node)

    def updateoninsertion(self, node):
        """
        Creates a new cell for the new node and updates the cells of its neighbors. 
        The new inserted node does not split a jump. The nearby uninserted points are 
        in the cells of nearby nodes from one level up to one level down.
        
        Parameters:
        ----------
        node : Node
            The new inserted node.
        """
        self.addnode(node)
        for point in self.rnn_out(rel(par(node)) | ch(rel(par(node))) | ch(rel(node))):
            self.trytochangernn(point, node)

    def updateonsplit(self, node):
        """
        Creates a new cell for the new inserted node, which splits a jump, from the cell of its parent.
        
        Parameters:
        ----------
        node : Node
            The new inserted node.
        """
        self.addnode(node)
        # The cells of the leaves or the nodes in level -\infty are always empty
        if node.level != float('-inf'):
            for point in self.rnn(par(node)):
                self.trytochangernn(point, node)

    def changernn(self, point, fromnode, tonode, todist=None):
        """
        Changes the center of an uninserted point to a different node and moves the point 
        to the cell of that node.
        
        Parameters:
        ----------
        point : Point
            An uninserted point.
        fromnode : Node
            The current center of the uninserted point.
        tonode : Node
            The next center of the uninserted point.
        todist : float
            The precomputed distance between point and tonode.
            If todist==None, then the method computed the distance.
        """
        todist = todist or dist(tonode, point)
        self._nn[point] = tonode
        self._nndist[point] = todist
        if todist <= self.tree.cp * (self.tree.tau ** (tonode.level - 1)) / 2:
            self._rnn_in[tonode].add(point)
        else:
            self._rnn_out[tonode].add(point)
        self._rnn_in[fromnode].discard(point)
        self._rnn_out[fromnode].discard(point)

    def trytochangernn(self, point, tonode):
        """
        Determines whether an uninserted point should change its cells or not. If so, the change will happen.
        
        Parameters:
        ----------
        point : Point
            The uninserted point.
        tonode : Node
            The node that may be the new center for the uninserted point.
        """
        fromnode = self._nn[point]
        todist = self.nndist(point) if fromnode.point == tonode.point else dist(tonode, point)
        if self.tree.isrel(tonode, point, todist):
            '''
            we change the center of a point if either:
            1) the current and next centers are associated to the same point and 
                we have a split below (next center has a lower level)
            2) the current and next centers are associated with different points 
                and the next center is closer to the point than its current center
            '''
            if (fromnode.point == tonode.point and fromnode.level > tonode.level) or \
                (fromnode.point != tonode.point and todist < self.nndist(point)):
                self.changernn(point, fromnode, tonode, todist)
