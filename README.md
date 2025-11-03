# N-Body Simulation

A Python package for simulating gravitational interactions between multiple celestial bodies using direct force calculation and the Barnes-Hut algorithm.

## Features

- **Body**: Represents celestial bodies with mass, position, and velocity
- **Simulation**: Basic n-body simulation using direct O(n²) force calculation
- **FastSimulation**: Optimized simulation using Barnes-Hut algorithm (O(n log n))
- **Gadget**: Quadtree data structure for spatial partitioning
- **Visualization**: Animated visualization of body trajectories

## Installation

```bash
pip install -r requirements.txt
```

Or install the package in development mode:

```bash
pip install -e .
```

## Project Structure

```
n-body/
├── src/
│   └── nbody/
│       ├── __init__.py          # Package exports
│       ├── constants.py          # Physical constants (G, scoeff, fcoeff)
│       ├── body.py               # Body class
│       ├── box.py                # Box class for spatial partitioning
│       ├── stack.py              # Stack data structure
│       ├── gnode.py              # GNode class for quadtree nodes
│       ├── gadget.py             # Gadget class (quadtree)
│       ├── simulation.py         # Simulation class
│       └── fast_simulation.py    # FastSimulation class (Barnes-Hut)
├── tests/                        # Test files
├── examples/                     # Example scripts
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Package configuration
└── README.md                     # This file
```

## Usage

### Basic Example

```python
from nbody import Body, Simulation

# Create a sun and a planet
bodies = [
    Body(1, 0, 0, 0, 0),           # Sun at origin
    Body(3.0e-6, 0, 1, 4.44, 4.44)  # Planet
]

# Run simulation
sim = Simulation(bodies, total_time=10, dt=0.01)
sim.show(-4, -4, 4, 4)  # Show animation
```

### Fast Simulation Example

```python
from nbody import Body, FastSimulation

# Create multiple bodies
bodies = [Body(1, 2*x, 2*y) for y in range(9) for x in range(9)]

# Run fast simulation using Barnes-Hut
sim = FastSimulation(bodies, total_time=1, dt=0.01)
sim.show(0, 0, 20, 20)
```

## Units

- **Distance**: Astronomical Units (AU). 1 AU = distance between Sun and Earth
- **Mass**: Solar Mass (M_sun). 1 M_sun = mass of the Sun
- **Time**: Year (yr). 1 yr = 1 year
- **Luminosity**: Solar Luminosity (L_sun). 1 L_sun = luminosity of the Sun
- **Velocity**: AU/yr

## Development

Run tests (when implemented):

```bash
pytest tests/
```

## License

This project is for educational purposes.
