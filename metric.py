"""
Defines classes to deal with general metric spaces
"""
import math
from abc import ABC, abstractmethod
import functools

class Metric(ABC):
    """
    An abstract base class for any arbitrary metric which delegates the distance 
    computation to its concrete subclasses

    Parameters
    ----------
    cachedist : bool
        Determines whether the computed distances should be stored in 
        a dictionary to avoid recalculations
    """
    def __init__(self, cachedist):
        self.cachedist = cachedist
        self.distdict = dict()
        self.reset()
        
    def reset(self):
        """
        Resets the counter tracing the number of distance computations 
        and clears the dictionary storing the computed distances
        """
        self.counter = 0
        self.distdict.clear()
        
    def dist(self, first, *others):
        """
        Computes the minimum distance of a point to other points
        
        Parameters
        ----------
        first : Point
            the first point
        others: variable length argument list of type Point
        
        Returns:
        -------
        float
            the minimum distance
        """
        if len(others) == 0: raise TypeError("Metric.dist: this method should have at least two arguments")
        return min(map(functools.partial(self.getdist, first), others))
    
    def getdist(self, first, second):
        """
        Computes the distance between two points
        
        Parameters
        ----------
        first : Point
            the first point
        second: Point
            the second point
            
        Returns:
        -------
        float
            the distance
        """
        dist = self.distdict.get((id(first), id(second)), None) if self.cachedist else None
        if not dist:
            dist = 0
            if first != second:
                dist = self.distance(first, second)
                self.counter += 1
            if self.cachedist: 
                self.distdict[(id(first), id(second))] = dist
        return dist        
    
    @abstractmethod
    def distance(self, first, second):
        """
        Returns the distance between two points in a certain metric.
        To be implemented by concerete metric subclasses.
        
        Parameters:
        ----------
        first : Point
            The first point.
        second : Point
            The second point
        
        Returns:
        -------
        float
            The distance between the first and the second points
        """
        pass
    
    def __str__(self):
        return type(self).__name__

class Euclidean(Metric):
    def __init__(self, cachedist=False):
        Metric.__init__(self, cachedist)
    def distance(self, first, second):
        return math.sqrt(sum((first[i] - second[i]) ** 2 for i in range(len(first.coords))))


class Manhattan(Metric):
    def __init__(self, cachedist=False):
        Metric.__init__(self, cachedist)
    def distance(self, first, second):
        return sum([abs(first[i] - second[i]) for i in range(len(first.coords))])

        
class LInfinity(Metric):
    def __init__(self, cachedist=False):
        Metric.__init__(self, cachedist) 
    def distance(self, first, second):
        return max([abs(first[i] - second[i]) for i in range(len(first.coords))])

