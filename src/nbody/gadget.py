"""
Gadget class implementing a quadtree for spatial partitioning of bodies.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from nbody.box import Box
from nbody.gnode import GNode
from nbody.stack import Stack


class Gadget:
    """Quadtree data structure for efficient spatial queries on bodies."""
    
    def __init__(self, box):
        """
        Initialize a Gadget with a root box.
        
        Args:
            box: Box object defining the root spatial region
        """
        self.root = GNode(box)
        self.size = 0
        
    def add(self, p): 
        """
        Add Body p to this Gadget.
        
        Args:
            p: Body object to add
        """
        # TODO: Implement this method
        pass
        
    def remove(self, p): 
        """
        Remove Body p from this Gadget.
        
        Args:
            p: Body object to remove
        """
        # TODO: Implement this method
        pass
        
    def __str__(self):
        """Return a string representation of the tree structure."""
        return self.root.niceStr()

    def getBodies(self):
        """
        Collect all Bodies from this Gadget and return them in an array.
        
        Returns:
            List of Body objects contained in the Gadget
        """
        A = [None] * self.size
        i = 0
        stack = Stack()
        stack.push(self.root)
        while not stack.isEmpty():
            n = stack.pop()
            if n.isLeaf():
                if n.p is not None:
                    A[i] = n.p
                    i += 1
            else:
                for c in n.children:
                    stack.push(c)
        return A   

    @staticmethod
    def fromBodies(ps):
        """
        Build a new Gadget and add all Bodies from array ps.
        
        Args:
            ps: array of Body objects
            
        Returns:
            Gadget object containing all bodies, or None if ps is empty
        """
        # Calculate bottom-left and top-right positions
        if ps == []:
            return None
        x0 = x1 = ps[0].x
        y0 = y1 = ps[0].y
        for p in ps:
            if p.x < x0:
                x0 = p.x
            elif p.x > x1:
                x1 = p.x
            if p.y < y0:
                y0 = p.y
            elif p.y > y1:
                y1 = p.y
        # Build gadget and add bodies
        g = Gadget(Box(x0, y0, x1, y1))
        for p in ps:
            g.add(p)
        return g    
    
    @staticmethod
    def _drawNode(ax, node, showCom):
        """
        Recursively draw a node and its children.
        
        Args:
            ax: matplotlib axes object
            node: GNode to draw
            showCom: if True, show center of mass markers
        """
        x0, y0, x1, y1, mx, my = node.box.asTuple()
        w = x1 - x0
        h = y1 - y0
        # Draw the node rectangle
        rect = Rectangle((x0, y0), w, h, fill=False, linewidth=0.8, alpha=0.5)
        ax.add_patch(rect)
        # Draw COM for internal nodes
        if showCom and not node.isLeaf():
            ax.plot([node.COM.x], [node.COM.y], marker='+', markersize=6)
            ax.plot([mx, node.COM.x], [my, node.COM.y], linewidth=0.3)            
        # Draw leaf contents
        if node.isLeaf(): 
            if node.p is not None:
                ax.plot([node.p.x], [node.p.y], marker='o', markersize=3)
        else:
            # Recurse into children [NE, NW, SW, SE]
            for c in node.children:
                if c is not None:
                    Gadget._drawNode(ax, c, showCom)
                
    def plot(self, figsize=(6, 6)):
        """
        Plot the quadtree structure.
        
        Args:
            figsize: (width, height) in inches
        """
        showCom = True         # Draw line with '+' from center to COM of internal nodes
        margin_ratio = 0.05    # Extra margin around the root box
        fig, ax = plt.subplots(figsize=figsize)
        # Plot node bounds
        Gadget._drawNode(ax, self.root, showCom)
        # Collect Bodies from leaves
        A = self.getBodies()
        if A != []:
            xs, ys = zip(*[(A[i].x, A[i].y) for i in range(len(A))])
            ax.plot(xs, ys, linestyle='none', marker='o', markersize=3)
        # Set view limits from root box (with margin)
        x0, y0, x1, y1, mx, my = self.root.box.asTuple()
        dx, dy = x1 - x0, y1 - y0
        pad_x = margin_ratio * max(dx, 1e-12)
        pad_y = margin_ratio * max(dy, 1e-12)
        ax.set_xlim(x0 - pad_x, x1 + pad_x)
        ax.set_ylim(y0 - pad_y, y1 + pad_y)
        ax.set_aspect('equal', adjustable='box')
        plt.tight_layout()
        plt.show()

