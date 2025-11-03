"""
N-body simulation package.

This package provides classes and utilities for simulating gravitational
interactions between multiple celestial bodies.
"""

from nbody.constants import G, scoeff, fcoeff
from nbody.body import Body
from nbody.box import Box
from nbody.stack import Stack
from nbody.gnode import GNode
from nbody.gadget import Gadget
from nbody.simulation import Simulation
from nbody.fast_simulation import FastSimulation

__version__ = "0.1.0"

__all__ = [
    "G",
    "scoeff",
    "fcoeff",
    "Body",
    "Box",
    "Stack",
    "GNode",
    "Gadget",
    "Simulation",
    "FastSimulation",
]

