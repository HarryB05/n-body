"""
Test code for the three questions in the notebook.
"""

import math
from nbody import Body, Simulation, Gadget, Box, FastSimulation


def test_closest_distance():
    """Tests for Simulation.closestDistance."""
    bodies = []
    for y in range(9):
        for x in range(9):
            bodies.append(Body(1, 2*x, 2*y))
    
    sim = Simulation(bodies)
    print(sim.closestDistance())
    
    sim = Simulation(bodies, total_time=0.5, dt=0.0001)
    print(sim.closestDistance())


def test_three_body_problem():
    """Tests for Body.threeBodyProblem."""
    sA = Body(10, -10, 0, 3.14, -5.44)
    sB = Body(10, 0, 0, 3.24, 5.44)
    sC = Body(10, -5, 8.660, -6.28, 0)
    p = Body(3.0e-6, -10, 6, -3, -15)
    
    bodies = [sA, sB, sC, p]
    print(p.threeBodyProblem(sA, sB, sC, 50, 50, 50))
    print(p.threeBodyProblem(sA, sB, sC, 45, 45, 45))


def test_gadget_add_remove():
    """Tests for Gadget add and remove operations."""
    # Test 1: 4 equal-mass Bodies on the edges of a square
    bodies = [
        Body(1, 50, 50),
        Body(1, -50, 50),
        Body(1, -50, -50),
        Body(1, 50, -50)
    ]
    
    g = Gadget(Box.getBox(bodies))
    for p in bodies:
        g.add(p)
    print(g)
    g.plot()
    
    # Now remove P[0]
    g.remove(bodies[0])
    print(g)
    g.plot()
    
    # Now remove all but the last body
    g.remove(bodies[1])
    g.remove(bodies[2])
    print(g)
    g.plot()
    
    # Test 2: 4 unequal-mass Bodies on the edges of a square
    bodies2 = [
        Body(1, 100, 100, 0, 0),
        Body(2, -100, 100, 0, 0),
        Body(3, -100, -100, 0, 0),
        Body(4, 100, -100, 0, 0)
    ]
    
    g2 = Gadget(Box.getBox(bodies2))
    for p in bodies2:
        g2.add(p)
    print(g2)
    g2.plot()
    
    # Test 3: 20 Bodies spread on a circle
    bodies3 = []
    for i in range(20):
        x = 50.0 * math.cos(i * 0.3)
        y = 50.0 * math.sin(i * 0.3)
        vx = 5.0 * math.cos(i * 0.7)
        vy = 5.0 * math.sin(i * 0.7)
        m = 1.0 + (i % 5)  # masses: 1..5
        bodies3.append(Body(m, x, y, vx, vy))
    
    g3 = Gadget(Box(-50, -50, 50, 50))
    for p in bodies3:
        g3.add(p)
    print(g3)
    g3.plot()
    
    for i in range(10):
        g3.remove(bodies3[i])
    print(g3)
    g3.plot()


def test_fast_simulation():
    """Tests for FastSimulation.getBodies."""
    def test_on_three_circles(n):
        bodies = []
        for i in range(n):
            x = 50.0 * math.cos(i * 0.3)
            y = 50.0 * math.sin(i * 0.3)
            vx = 50.0 * math.cos(i * 0.7)
            vy = 50.0 * math.sin(i * 0.7)
            m = 1.0 + (i % 5)  # masses: 1..5
            bodies.append(Body(m, x, y, 3*vx, 3*vy))
            bodies.append(Body(m, 2*x, 2*y, 2*vx, 2*vy))
            bodies.append(Body(m, 3*x, 3*y, vx, vy))
        
        sim = FastSimulation(bodies, total_time=0.01)
        new_ps = [None] * len(bodies)
        sim.run(test=new_ps)
        print(f"Experiment with n={n}, new_ps entries:")
        for ps in new_ps:
            print(len(ps), ps)
    
    test_on_three_circles(1)
    test_on_three_circles(3)


if __name__ == "__main__":
    # Uncomment the test you want to run:
    # test_closest_distance()
    # test_three_body_problem()
    # test_gadget_add_remove()
    # test_fast_simulation()
    pass
