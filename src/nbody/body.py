"""
Body class representing a celestial body in the n-body simulation.
"""

from nbody.constants import G, scoeff, fcoeff


class Body:
    """Represents a celestial body with mass, position, and velocity."""
    
    def __init__(self, m, x, y, vx=0, vy=0):
        """
        Initialize a Body.
        
        Args:
            m: mass in Solar Masses (M_sun)
            x: x position in Astronomical Units (AU)
            y: y position in Astronomical Units (AU)
            vx: x velocity in AU/yr (default: 0)
            vy: y velocity in AU/yr (default: 0)
        """
        self.m = m     # mass
        self.x = x     # position
        self.y = y     # position
        self.vx = vx   # velocity
        self.vy = vy   # velocity
        
    def squareDist(self, other):
        """Calculate the squared distance to another Body."""
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def __str__(self):
        return f"Body({self.m},{self.x},{self.y},{self.vx},{self.vy})"    

    def __repr__(self):
        return str(self)    

    def asTuple(self):
        """Return body state as a tuple (m, x, y, vx, vy)."""
        return (self.m, self.x, self.y, self.vx, self.vy)    
    
    def next(self, Bodies, dt):
        """
        Compute the next position and velocity after time dt.
        
        Takes into account gravitational forces from all Bodies in the array.
        Uses Newton's law of universal gravitation.
        
        Args:
            Bodies: array of Body objects affecting this body
            dt: time step in years
            
        Returns:
            New Body object with updated position and velocity
        """
        ret = Body(self.m, self.x, self.y)
        ax = ay = 0       
        
        # For each body, compute its gravitational force and add to acceleration
        for p in Bodies:
            if p == self:
                continue  # Current Body does not affect itself
                
            # Euclidean distance squared between p and this Body
            sq_distance = self.squareDist(p)
            
            # Vector form of Newton's law of gravity
            # See: https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation
            ax += (p.x - self.x) * p.m * G / (sq_distance ** 1.5)
            ay += (p.y - self.y) * p.m * G / (sq_distance ** 1.5)
            
        # Compute displacement due to acceleration and current velocity (inertia)
        ret.x += dt * dt * ax + dt * self.vx
        ret.y += dt * dt * ay + dt * self.vy
        
        # Compute the velocity vectors
        ret.vx = (ret.x - self.x) / dt
        ret.vy = (ret.y - self.y) / dt

        return ret

    def threeBodyProblem(self, sunA, sunB, sunC, lA, lB, lC):
        """
        Predict years of stability in a 3-sun solar system.
        
        It suffices to take into account just the three suns (sunA, sunB, sunC) 
        and the planet (self).
        
        Stability is broken if one of the following criteria is violated:
        a. No scorching: lA/dA + lB/dB + lC/dC must be less than scoeff
        b. No freezing: lA/dA + lB/dB + lC/dC must be greater than fcoeff
        
        Args:
            sunA, sunB, sunC: Body objects representing the three suns
            lA, lB, lC: luminosities of sunA, sunB, sunC in L_sun
            
        Returns:
            Number of years of stability predicted
            
        Notes:
            - dA, dB, dC are the squared distances between sunA, sunB, sunC and self
            - lA, lB, lC are the luminosities of sunA, sunB, sunC respectively
        """
        # TODO: Implement this method
        pass

