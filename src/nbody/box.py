"""
Box class for spatial partitioning in quadtree structures.
"""


class Box:
    """Represents a rectangular spatial region for quadtree partitioning."""
    
    def __init__(self, x0, y0, x1, y1):
        """
        Initialize a Box.
        
        Args:
            x0: left boundary
            y0: bottom boundary
            x1: right boundary
            y1: top boundary
        """
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.maxSide = max(self.x1 - self.x0, self.y1 - self.y0)
        self.mx = (self.x0 + self.x1) / 2
        self.my = (self.y0 + self.y1) / 2
        
    def isIn(self, p):
        """Check if a point (Body) is inside this box."""
        return self.x0 <= p.x <= self.x1 and self.y0 <= p.y <= self.y1
    
    def asTuple(self):
        """Return box coordinates as tuple (x0, y0, x1, y1, mx, my)."""
        return (self.x0, self.y0, self.x1, self.y1, self.mx, self.my)
    
    def split4(self):
        """
        Split the box into four quadrants.
        
        Returns:
            Tuple of four Box objects: (NE, NW, SW, SE)
        """
        bNE = Box(self.mx, self.my, self.x1, self.y1)
        bNW = Box(self.x0, self.my, self.mx, self.y1)
        bSW = Box(self.x0, self.y0, self.mx, self.my)
        bSE = Box(self.mx, self.y0, self.x1, self.my)
        return (bNE, bNW, bSW, bSE)

    @staticmethod
    def getBox(P):
        """
        Build a box that encloses all Bodies from an array.
        
        Args:
            P: array of Body objects
            
        Returns:
            Box object enclosing all bodies, or None if P is empty
        """
        if len(P) == 0:
            return None
        x0 = x1 = P[0].x
        y0 = y1 = P[0].y
        for p in P: 
            if p.x < x0:
                x0 = p.x
            if p.y < y0:
                y0 = p.y
            if p.x > x1:
                x1 = p.x
            if p.y > y1:
                y1 = p.y
        return Box(x0, y0, x1, y1)    
    
    def __str__(self):
        return f"Box({self.x0},{self.y0},{self.x1},{self.y1})"

