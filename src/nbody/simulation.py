"""
Simulation class for running n-body simulations.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from nbody.body import Body


class Simulation:
    """Basic n-body simulation using direct force calculation."""
    
    def __init__(self, Bodies, total_time=10, dt=0.01):
        """
        Initialize a simulation.
        
        Args:
            Bodies: list of Body objects to simulate
            total_time: total simulation time in years (default: 10)
            dt: time step in years (default: 0.01)
        """
        self.bodies = Bodies
        self.total_time = total_time
        self.dt = dt
        self.timesteps = int(total_time / dt)
        
    def run(self):
        """
        Run the simulation and produce an array of arrays of Bodies.
        
        The t-th entry in the list is the position of Bodies after the t-th timestep
        has been simulated.
        
        Returns:
            List of lists, where each inner list contains Body objects at that timestep
        """
        pss = [None] * (self.timesteps + 1)
        pss[0] = self.bodies
        for t in range(self.timesteps):
            # For every Body in the current timestep, add its next position in next timestep
            pss[t + 1] = [pss[t][i].next(pss[t], self.dt) for i in range(len(self.bodies))]
        return pss
    
    def closestDistance(self):
        """
        Find the closest distance between any two bodies during the simulation.
        
        Returns:
            Minimum distance between any two bodies over all timesteps
        """
        if len(self.bodies) < 2:
            return None

        positions = self.run()

        min_sq_distance = float('inf')

        for timestep_bodies in positions:
            for i in range(len(timestep_bodies)):
                for j in range(i + 1, len(timestep_bodies)):
                    sq_distance = timestep_bodies[i].squareDist(timestep_bodies[j])

                    if sq_distance < min_sq_distance:
                        min_sq_distance = sq_distance

        return min_sq_distance ** 0.5
    
    def show(self, x0, y0, x1, y1):
        """
        Show an animation of the simulation using matplotlib.
        
        Args:
            x0, y0: lower-left corner of view window
            x1, y1: upper-right corner of view window
        """
        pss = self.run()
        # Get figure and axes objects
        fig, ax = plt.subplots()
        # Set some reasonable zoom on axes
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        # Put labels on the window for Bodies with different colours
        scatter = []
        for i in range(len(self.bodies)):
            scatter.append(ax.scatter([], [], marker='o', label=f'Body {i}'))
        # Add timestep text to the legend
        time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                           verticalalignment='top', 
                           bbox=dict(boxstyle='round', 
                                   facecolor='wheat', alpha=0.5))
        # Update function from one position to the next
        def update(frame):
            for i in range(len(self.bodies)):
                scatter[i].set_offsets([pss[frame][i].x, pss[frame][i].y])
            time_text.set_text(f'Timestep: {frame}')                
            return scatter + [time_text]
        # Generate and show the animation
        a = FuncAnimation(fig, update, frames=len(pss), interval=1, blit=True, repeat=False)
        plt.xlabel("X coordinate (AU)")
        plt.ylabel("Y coordinate (AU)")
        plt.title("Celestial body trajectories")
        plt.legend()
        plt.show()

