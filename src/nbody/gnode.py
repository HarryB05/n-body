"""
GNode class representing a node in the quadtree (Gadget) structure.
"""

from nbody.body import Body


class GNode:
    """Represents a node in the quadtree for spatial partitioning."""
    
    def __init__(self, box):
        """
        Initialize a GNode.
        
        Args:
            box: Box object defining the spatial region of this node
        """
        self.box = box
        self.COM = None           # this node's center of mass
        self.nbodies = 0          # number of bodies contained in node
        self.p = None             # if this node is a leaf with a Body
        self.children = None      # children are: [NE, NW, SW, SE]
        self.updateCOM()

    def isLeaf(self):
        """Check if this node is a leaf (contains fewer than 2 bodies)."""
        return self.nbodies < 2
        
    def updateCOM(self):
        """Update the center of mass (COM) of this node."""
        if self.isLeaf(): 
            if self.p == None:
                self.COM = Body(0, self.box.mx, self.box.my)
            else:
                self.COM = Body(self.p.m, self.p.x, self.p.y)
            return
            
        x = y = m = 0
        for c in self.children:
            x += c.COM.x * c.COM.m
            y += c.COM.y * c.COM.m
            m += c.COM.m
        if m > 0:
            self.COM = Body(m, x / m, y / m)
        else:
            self.COM = Body(0, self.box.mx, self.box.my)

    def niceStr(self): 
        """
        Generate a nice string representation of the tree structure.
        
        Returns:
            String representation showing the tree hierarchy
        """
        S = ("├", "─", "└", "│")
        angle = S[2] + S[1] + " "
        vdash = S[0] + S[1] + " "
        
        def niceRec(ptr, acc, pre, A):
            if ptr == None:
                raise Exception("A None GNode was found")
            val = f"{len(A)}:{ptr.box},{ptr.nbodies}"
            A.append(f"({ptr.COM.m}, {ptr.COM.x}, {ptr.COM.y})")
            if ptr.children == None:
                return acc + pre + val
            if pre == vdash:
                pre2 = S[3] + "  "
            elif pre == angle:
                pre2 = "   "
            else:
                pre2 = ""
            T = [vdash, vdash, vdash, angle]
            for i in range(4):
                T[i] = niceRec(ptr.children[i], acc + pre2, T[i], A)
            return acc + pre + val + "\n" + T[0] + "\n" + T[1] + "\n" + T[2] + "\n" + T[3]
            
        A = []
        s = niceRec(self, "", "", A) + "\n"
        for i in range(len(A)):
            s += f"\n{i}{' ' * (3 - len(str(i)))}-> {A[i]}"
        return s

