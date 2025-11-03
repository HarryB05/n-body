"""
FastSimulation class using Barnes-Hut algorithm for efficient n-body simulations.
"""

from nbody.simulation import Simulation
from nbody.gadget import Gadget


class FastSimulation(Simulation):
    """
    Fast n-body simulation using Barnes-Hut algorithm.
    
    Uses a quadtree (Gadget) to approximate gravitational forces,
    reducing computational complexity from O(n²) to O(n log n).
    """
    
    def run(self, test=None): 
        """
        Run the simulation using Barnes-Hut approximation.
        
        The t-th entry in the list is the position of Bodies after the t-th timestep
        has been simulated. Simulation uses a Gadget to approximate for each body
        the list of other bodies gravitationally affecting its trajectory.
        
        Args:
            test: optional array to store the bodies used for each body (for debugging)
            
        Returns:
            List of lists, where each inner list contains Body objects at that timestep
        """
        pss = [None] * (self.timesteps + 1)
        pss[0] = self.bodies
        for t in range(self.timesteps):
            # Calculate the current Gadget
            g = Gadget.fromBodies(pss[t])
            # For every Body in the current timestep, add its next position in next timestep
            # but using the gadget g
            A = pss[t][:]
            for i in range(len(A)):
                new_ps = FastSimulation.getBodies(g, A[i])
                A[i] = A[i].next(new_ps, self.dt)
                if test is not None:
                    test[i] = new_ps
            pss[t + 1] = A
        return pss

    @staticmethod
    def BarnesHut(n, p):
        """
        Barnes-Hut criterion deciding whether node n should be opened when calculating
        the gravitational forces exerted on body p.
        
        By default, if p is in n then we open.
        
        Args:
            n: GNode to check
            p: Body to calculate forces for
            
        Returns:
            True if the node should be opened (examined), False if it can be approximated
        """
        theta = 0.7
        if n.box.isIn(p):
            return True
        sqDist = (n.COM.x - p.x) ** 2 + (n.COM.y - p.y) ** 2
        return n.box.maxSide ** 2 / sqDist >= theta ** 2
        
    @staticmethod
    def getBodies(g, p, shouldOpen=BarnesHut):
        """
        Get bodies from gadget g in an optimal way.
        
        Uses criterion shouldOpen and body p to decide whether nodes in the gadget
        should be "opened" (i.e. their subnodes examined) or not (i.e. the whole
        subtree approximated by its COM).
        
        Args:
            g: Gadget to query
            p: Body reference point
            shouldOpen: function determining whether to open a node (default: BarnesHut)
            
        Returns:
            List of Body objects (either actual bodies or COM approximations)
        """
        # TODO: Implement this method
        return []

