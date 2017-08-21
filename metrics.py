import math
from abc import ABCMeta, abstractmethod

class Metric:
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.resetcounter()
        
    def resetcounter(self):
        self.counter = 0
        
    def dist(self, first, *others):
        if len(others) == 0: raise TypeError("Metric.dist: this method should have at least two arguments")
        self.counter += 1
        minDist = self.distance(first, others[0])
        for i in range(1, len(others)):
            self.counter += 1
            currDist = self.distance(first, others[i])
            if currDist < minDist: minDist = currDist
        return minDist
    
    @abstractmethod
    def distance(self, first, second): pass
    
    def __str__(self):
        return type(self).__name__

class Euclidean(Metric):
    def distance(self, first, second):
        return math.sqrt(sum((first[i] - second[i]) ** 2 for i in range(len(first.coords))))

class Manhattan(Metric):
    def distance(self, first, second):
        return sum([abs(first[i] - second[i]) for i in range(len(first.coords))])
        
class LInfinity(Metric):
    def distance(self, first, second):
        return max([abs(first[i] - second[i]) for i in range(len(first.coords))])
         

