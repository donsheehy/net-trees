class Point:
    def __init__(self, *coords):
        self.coords = list(coords)

    def sqdistto(self, other):
        if not isinstance(other, Point):
            other = other.point
        return sum((self[i] - other[i])**2 for i in range(len(self.coords)))

    def distto(self, other):
        return self.sqdistto(other) ** 0.5

    def __getitem__(self, index):
        return self.coords[index]

    def __str__(self):
        return "(" + ". ".join(str(c) for c in self.coords) + ")"
