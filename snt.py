import math
from node import Node, dist, rel, par, ch, nearest

class SNT:
    """
    Defines a semi-compressed local net-tree.
    
    Parameters:
    ----------
    tau : float
        The scale factor.
    cp: float
        The packing constant.
    cc: float
        The covering constant.
    cr: float
        The relative constant.
    """
    def __init__(self, tau, cp, cc, cr=None):
        self.tau = tau
        self.cp = cp
        self.cc = cc
        self.cr = cr or (2 * cc * tau) / (tau - 4)
        self.root = None

    def setroot(self, point):
        """
        Initializes a net-tree with one point as a jump from level +\infty to -\infty.
        
        Parameters:
        ----------
        point : Point
            The first point to be inserted in the net-tree.
        """
        self.root = Node(point, float('inf'))
        self.splitbelow(self.root, float('-inf'))

    def construct(self, points, pointlocation):
        """
        Constructs a net-tree from a given sequence of points based an a point location algorithm.
        
        Parameters:
        ----------
        points : list
            The list of points.
        pointlocation : PointLocation    
            The point location class to be used to find the center of a point.
        """
        self.points=[points[-1]]
        points = list(points)
        self.setroot(points.pop())
        self.ploc = pointlocation(self, points)
        self.ploc.addnode(self.root.getchild())
        for p in points:
            self.points.append(p)
            self.insert(p)

    def insert(self, point, closest=None):
        """
        Insertes a point into the net-tree.
        
        Parameters:
        ----------
        point : Point
            The point to be inserted.
        closest : Node
            The center of the point. If `closest` is not provided, then the 
            point location data structure is used to find it.
        """
        closest = closest or self.ploc.nn(point)
        if hasattr(self, 'ploc'):
            dst = self.ploc.nndist(point, closest)
            # Removes the uninserted point from the point location data structure.
            # In other words, the point is removed from the mappings for the centers and cells
            self.ploc.removepoint(point)
        else: 
            dst = dist(closest, point)
        # Finding the lowest level so that the point can still be a relative of the closest node
        level = self.minlevelrelatives(closest, point, dst)
        # If the packing property does not hold at this level, 
        # then the node should be inserted in exactly one level down 
        if dst <= self.cp * self.tau ** level:
            level -= 1
        if level < closest.level:
            # If there is a jump, then we should split it
            if closest.getchild().level < level:
                closest = self.splitbelow(closest, level)
            # Otehrwise, find the node associated to the same point
            else:
                closest = [n for n in closest.ch if n.point == closest.point][0]
        node = Node(point, level)
        self.update(node, closest)
        lowest = node
        # We ensure that the nesting property is satisfied
        if len(node.ch) > 0:
            lowest = Node(node.point, node.level - 1)
            if lowest not in node.ch:
                lowest.setpar(node)
                if hasattr(self, 'ploc'): self.ploc.updateonsplit(lowest)
        self.splitbelow(lowest, float('-inf'))
        while not self.iscovered(node):
            node = self.promote(node)

    def promote(self, node):
        """
        Promotes `node` to one level up.
        
        Parameters:
        ----------
        node : Node
            The node that should be promoted.
            
        Returns:
        -------
        Node
            The promoted node at level above.
        """
        newnode = Node(node.point, node.level + 1)
        self.update(newnode, node.par)
        return newnode

    def update_rel(self, node, closest):
        """
        Updates the relative list of a given node.
        
        Parameters:
        ----------
        node : Node
            The node that its relatives should be updated.
        closest : Node
            The node closest to `node` at the same level.
        """
        for other in ch(rel(par(closest))):
            if self.isrel(node, other):
                if other.level < node.level:
                    other = self.splitabove(other, node.level)
                node.addrel(other)

    def update_ch(self, node):
        """
        Updates children of a given node.
        
        Parameters:
        ----------
        node : Node
            The node that its relatives should be updated.
        """
        for other in ch(rel(node)):
            if dist(node, other) < dist(other, other.par):
                oldpar = other.par
                node.addch(other)
                child = oldpar.getchild()
                # The old parent should not be removed from the tree because it is a relative of `node`
                # However, if it has only one child, then that child should be checked 
                # against the semi-compressed condition
                if len(oldpar.ch) == 1 and len(child.ch) == 1 and len(child.rel) == 1:
                    if hasattr(self, 'ploc'): self.ploc.updateonremoval(child)
                    oldpar.addch(child.getchild())
                    oldpar.ch.discard(child)          

    def update_par(self, node, closest):
        """
        Updates the parent of a given node.
        
        Parameters:
        ----------
        node : Node
            The node that its parent should be updated.
        closest : Node
            The node closest to `node` at the same level.
        """
        newpar = nearest(node, rel(par(closest)))
        # There may be a node in rel(par(@closest)) such that 
        # its distance to `node` is the same as the distance of `node` to `closest.par`.
        # In this case, the right parent should be the parent of `closest`, 
        # otherwise we may need to delete `closest` from the tree.
        if dist(node, newpar) == dist(node, closest.par):
            newpar = closest.par
        if newpar.getchild().level < node.level:
            self.splitbelow(newpar, node.level)
            if self.isrel(node, newpar): node.addrel(newpar.getchild())
        node.setpar(newpar)

    def update(self, node, closest):
        """
        Updates the parent, children, and relatives of the new node.
        
        Parameters:
        ----------
        node : Node
            The new inserted node.
        closest: Node
            The closest node which is at the same level of `node`.
        """
        if closest.par.level > closest.level + 1:
            self.splitabove(closest, closest.level + 1)
        self.update_rel(node, closest)
        self.update_par(node, closest)
        self.update_ch(node)
        if hasattr(self, 'ploc'): self.ploc.updateoninsertion(node)

    def splitbelow(self, node, level):
        """
        Splits a jump from below at the given level.
        
        Parameters:
        ----------
        node : Node
            The top node of a jump.
        level : int
            The level to split the jump.
        """
        newnode = Node(node.point, level)
        if node.ch: newnode.addch(node.getchild())
        node.ch = set()
        newnode.setpar(node)
        if hasattr(self, 'ploc'): self.ploc.updateonsplit(newnode)
        return newnode

    def splitabove(self, node, level):
        """
        Splits a jump from above at the given level.
        
        Parameters:
        ----------
        node : Node
            The bottom node of a jump.
        level : int
            The level to split the jump.
        """
        return self.splitbelow(node.par, level)

    def iscovered(self, node):
        """
        Tests whether the covering property for `node.par` is satisfied or not.
        
        Parameters:
        ----------
        node : Node
            The node that should be tested against the covering property.
            
        Returns:
        -------
        bool
            Returns True is the distance between `node` and its parent is 
            not greater than c_c\tau**(node.level+1).
        """
        return dist(node, node.par) <= self.cc * (self.tau ** (node.level + 1))

    def isrel(self, node, other, computeddist=None):
        """
        Determines if the distance between `node` and `other` is  at most c_r\tau**(node.level).
        
        Parameters:
        ----------
        node : Node
            A node of the tree.
        other : Node or Point
            Either a node of the tree or a point.
        computeddist : float
            If the distance between `node` and `other` is precomputed, then we do not recompute it.
            Otherwise, if computeddist==None, then the method calculates the distance.
        
        Returns:
            bool
        """
        return (computeddist or dist(node, other)) <= self.cr * (self.tau ** node.level)

    def minlevelrelatives(self, first, second, computeddist=None):
        """
        Determines the minimum level so that `first` and `second` can be relatives.
        
        Parameters:
        ----------
        first : Node
            A node of the tree.
        second : Node or Point
            A node of the tree or a point.
        computeddist : float
            If the distance between `node` and `other` is precomputed, then we do not recompute it.
            Otherwise, if computeddist==None, then the method calculates the distance.
        
        Returns:
        -------
        float
        """
        return math.ceil(math.log((computeddist or dist(first, second)) / self.cr, self.tau))

    def __str__(self):
        return str(self.root)
