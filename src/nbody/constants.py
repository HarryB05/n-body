"""
Physical constants for n-body simulations.

Units used:
- Distance: Astronomical Units (AU). 1 AU = distance between Sun and Earth
- Mass: Solar Mass (M_sun). 1 M_sun = mass of the Sun
- Time: Year (yr). 1 yr = 1 year (one rotation of the Earth around the Sun)
- Luminosity: Solar Luminosity (L_sun). 1 L_sun = luminosity of the Sun
- Velocity: AU/yr
"""

import math

# Universal gravitational constant (AU^3/M_sun/yr^2)
G = 4 * (math.pi) ** 2

# Scorching coefficient, approx. 0.745 AU from the Sun (L_sun/AU^2)
scoeff = 22.62

# Freezing coefficient, approx. 2 AU from the Sun (L_sun/AU^2)
fcoeff = 3.14

