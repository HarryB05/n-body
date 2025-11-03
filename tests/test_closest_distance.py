"""
Tests for Simulation.closestDistance method.
"""

import sys
from pathlib import Path

# Try importing directly first (if package is installed)
try:
    from nbody import Body, Simulation
    from nbody.constants import GREEN, RED, END
except ImportError:
    # If not installed, add src to path
    test_dir = Path(__file__).parent
    src_dir = test_dir.parent / 'src'
    sys.path.insert(0, str(src_dir))
    from nbody import Body, Simulation
    from nbody.constants import GREEN, RED, END

# Import the test runner
from test_runner import run_tests


def test_no_bodies():
    """Test with no bodies - should return None."""
    sim = Simulation([])
    result = sim.closestDistance()
    try:
        assert result is None, f"   Expected None, got {result}"
        return True, f"{GREEN}   ✓ Passed{END}"
    except AssertionError as e:
        return False, f"{RED}   ✗ Failed: {e}{END}"


def test_one_body():
    """Test with one body - should return None."""
    sim = Simulation([Body(1, 0, 0)])
    result = sim.closestDistance()
    try:
        assert result is None, f"   Expected None, got {result}"
        return True, f"{GREEN}   ✓ Passed{END}"
    except AssertionError as e:
        return False, f"{RED}   ✗ Failed: {e}{END}"


def test_two_stationary_bodies():
    """Test with two stationary bodies - distance should remain constant."""
    sim = Simulation([
        Body(1, 0, 0),
        Body(1, 10, 0)
    ], total_time=1, dt=0.01)
    
    result = sim.closestDistance()
    expected = 10.0  # Distance between (0,0) and (10,0)
    
    print(f"   Two stationary bodies at distance 10: got {result}")
    try:
        assert result is not None, "   closestDistance() returned None - method not fully implemented yet"
        assert abs(result - expected) < 0.001, f"   Expected ~{expected}, got {result}"
        return True, f"{GREEN}   ✓ Passed{END}"
    except AssertionError as e:
        return False, f"{RED}   ✗ Failed: {e}{END}"


def test_two_bodies_simple():
    """Test with two bodies in a simple configuration."""
    # Two bodies starting close together
    sim = Simulation([
        Body(1, 0, 0),
        Body(1, 1, 0)
    ], total_time=0.1, dt=0.001)
    
    result = sim.closestDistance()
    print(f"   Two bodies starting at distance 1: got {result}")
    try:
        assert result is not None, "   closestDistance() returned None - method not fully implemented yet"
        assert result >= 0, "   Distance should be non-negative"
        return True, f"{GREEN}   ✓ Passed{END}"
    except AssertionError as e:
        return False, f"{RED}   ✗ Failed: {e}{END}"


def test_three_bodies():
    """Test with three bodies."""
    sim = Simulation([
        Body(1, 0, 0),
        Body(1, 5, 0),
        Body(1, 10, 0)
    ], total_time=0.5, dt=0.01)
    
    result = sim.closestDistance()
    print(f"   Three bodies in a line: got {result}")
    try:
        assert result is not None, "   closestDistance() returned None - method not fully implemented yet"
        assert result >= 0, "   Distance should be non-negative"
        return True, f"{GREEN}   ✓ Passed{END}"
    except AssertionError as e:
        return False, f"{RED}   ✗ Failed: {e}{END}"


def test_grid_example_coarse():
    """Test with the grid example from the question (coarse dt)."""
    P = [None] * 81
    for y in range(9):
        for x in range(9):
            P[9*y+x] = Body(1, 2*x, 2*y)
    
    sim = Simulation(P)
    result = sim.closestDistance()
    
    print(f"   Grid example (coarse dt=0.01): got {result}")
    print(f"   Expected: ~0.015527720571708991 AU")
    try:
        assert result is not None, "   closestDistance() returned None - method not fully implemented yet"
        assert result > 0, "   Distance should be positive"
        return True, f"{GREEN}   ✓ Passed{END}"
    except AssertionError as e:
        return False, f"{RED}   ✗ Failed: {e}{END}"


def test_grid_example_fine():
    """Test with the grid example from the question (fine dt)."""
    P = [None] * 81
    for y in range(9):
        for x in range(9):
            P[9*y+x] = Body(1, 2*x, 2*y)
    
    sim = Simulation(P, total_time=0.5, dt=0.0001)
    result = sim.closestDistance()
    
    print(f"   Grid example (fine dt=0.0001): got {result}")
    print(f"   Expected: ~0.00019088314702779433 AU")
    try:
        assert result is not None, "   closestDistance() returned None - method not fully implemented yet"
        assert result > 0, "   Distance should be positive"
        # Fine dt should give a smaller distance
        assert result < 0.001, "   With fine dt, should find closer approach"
        return True, f"{GREEN}   ✓ Passed{END}"
    except AssertionError as e:
        return False, f"{RED}   ✗ Failed: {e}{END}"


def test_initial_distance():
    """Test that initial configuration distances are considered."""
    # Two bodies starting at known distance
    sim = Simulation([
        Body(1, 0, 0),
        Body(1, 3, 4)  # Distance = sqrt(9+16) = 5
    ], total_time=0.01, dt=0.001)
    
    result = sim.closestDistance()
    print(f"   Initial distance should be 5: got {result}")
    try:
        assert result is not None, "   closestDistance() returned None - method not fully implemented yet"
        assert abs(result - 5.0) < 0.1, f"   Expected ~5.0, got {result}"
        return True, f"{GREEN}   ✓ Passed{END}"
    except AssertionError as e:
        return False, f"{RED}   ✗ Failed: {e}{END}"


def partial():
    """
    Simple helper function to test closestDistance with given inputs.
    Just runs the simulation and prints the result.
    
    Args:
        bodies: list of Body objects
        total_time: total simulation time (default: 10)
        dt: time step (default: 0.01)
    """

    P = [None]*81
    for y in range(9):
        for x in range(9):
            P[9*y+x] = Body(1,2*x,2*y)

    sim = Simulation(P)
    result = sim.closestDistance()

    expected = 0.015527720571708991

    print(f"\nSimulation with {len(P)} bodies:")
    print(f"{'Expected:':<10} {expected} AU")
    print(f"{'Result:':<10} {result} AU")

    try:
        assert result is not None, "closestDistance() returned None - method not fully implemented yet"
        assert result > 0, "Distance should be positive"
        assert abs(result - expected) < 0.001, f"Expected ~{expected} AU, got {result} AU"
        print(f"{GREEN}   ✓ Passed{END}\n")
    except AssertionError as e:
        print(f"{RED}   ✗ Failed: {e}{END}\n")


if __name__ == "__main__":
    # TODO: verify the tests are correct
    run_tests(test_name_prefix="Testing closestDistance method")
    # partial()

