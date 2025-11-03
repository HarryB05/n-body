"""
Basic simulation examples from the notebook.
"""

import math
from nbody import Body, Simulation


def sun_and_planet():
    """A sun and a planet."""
    bodies = [
        Body(1, 0, 0, 0, 0),
        Body(3.0e-6, 0, 1, 4.44, 4.44)
    ]
    sim = Simulation(bodies)
    sim.show(-4, -4, 4, 4)


def three_suns_and_planet():
    """3 suns and a planet."""
    sA = Body(10, -10, 0, 3.14, -5.44)
    sB = Body(10, 0, 0, 3.24, 5.44)
    sC = Body(10, -5, 8.660, -6.28, 0)
    p = Body(3.0e-6, -10, 6, -3, -15)
    
    bodies = [sA, sB, sC, p]
    sim = Simulation(bodies)
    sim.show(-30, -30, 30, 30)


def grid_of_bodies():
    """81 stationary bodies on a grid."""
    bodies = []
    for y in range(9):
        for x in range(9):
            bodies.append(Body(1, 2*x, 2*y))
    
    sim = Simulation(bodies, total_time=1)
    sim.show(0, 0, 20, 20)


def circular_formation():
    """42 moving bodies starting on a circle."""
    bodies = []
    for i in range(42):
        x = 50.0 * math.cos(i * 0.3)
        y = 50.0 * math.sin(i * 0.3)
        vx = 50.0 * math.cos(i * 0.7)
        vy = 50.0 * math.sin(i * 0.7)
        m = 1.0 + (i % 5)  # masses: 1..5
        bodies.append(Body(m, x, y, vx, vy))
    
    sim = Simulation(bodies)
    sim.show(-750, -750, 750, 750)


def two_circles():
    """84 moving bodies starting on two circles."""
    bodies = []
    for i in range(42):
        x = 50.0 * math.cos(i * 0.3)
        y = 50.0 * math.sin(i * 0.3)
        vx = 50.0 * math.cos(i * 0.7)
        vy = 50.0 * math.sin(i * 0.7)
        m = 1.0 + (i % 5)  # masses: 1..5
        bodies.append(Body(m, x, y, 2*vx, 2*vy))
        bodies.append(Body(m, 2*x, 2*y, vx, vy))
    
    sim = Simulation(bodies)
    sim.show(-750, -750, 750, 750)


if __name__ == "__main__":
    # Uncomment the example you want to run:
    # sun_and_planet()
    # three_suns_and_planet()
    # grid_of_bodies()
    # circular_formation()
    # two_circles()
    pass

