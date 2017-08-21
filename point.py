class Point:
    def __init__(self, coords, metric):
        self.coords = coords
        self.metric = metric

    def distto(self, *others):
        return self.metric.dist(self, *others)

    def __getitem__(self, index):
        return self.coords[index]

    def __str__(self):
        return "(" + ", ".join(str(c) for c in self.coords) + ")"
    
    def __eq__(self, other):
        return self.coords == other.coords
    
    def __hash__(self):
        return hash(tuple(self.coords))
    
    @staticmethod
    def importFrom(path, metric):
        points = []
        with open(path) as f:
            for line in f:
                points.append(Point([int(coord) if float(coord).is_integer() else float(coord) for coord in line.split(',')], metric))
        return points
    
    @staticmethod
    def exportTo(path, points):
        with open(path, 'w') as f:
            for point in points: f.write(', '.join([str(coord) for coord in point.coords]) + '\n')

def setMetric(metric, points):
    for pt in points: pt.metric = metric
