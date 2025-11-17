"""Configuration and preset scenarios."""

from models import CelestialBody
from utils import SOLAR_MASS, EARTH_MASS, JUPITER_MASS, AU


class ScenarioPresets:
    """Predefined simulation scenarios."""
    
    @staticmethod
    def three_body_choreography():
        """
        Figure-8 choreography - three equal masses following the same path.
        This is a stable periodic solution to the three-body problem.
        """
        # Simplified version - exact values require precise initialization
        mass = SOLAR_MASS
        bodies = [
            CelestialBody("Body 1", mass, -1.0*AU, 0, 0, 15000, "#FDB813"),
            CelestialBody("Body 2", mass, 1.0*AU, 0, 0, -15000, "#FF6B35"),
            CelestialBody("Body 3", mass, 0, 1.5*AU, -10000, 0, "#FF0000"),
        ]
        return bodies
    
    @staticmethod
    def sun_earth_moon():
        """Simple Sun-Earth-Moon system."""
        sun = CelestialBody("Sun", SOLAR_MASS, 0, 0, 0, 0, "#FDB813")
        earth = CelestialBody("Earth", EARTH_MASS, AU, 0, 0, 29780, "#4A90E2")
        # Moon orbits Earth at 384,400 km with velocity relative to Earth
        moon = CelestialBody("Moon", EARTH_MASS * 0.0123, 
                            AU + 3.844e8, 0, 0, 29780 + 1022, "#CCCCCC")
        return [sun, earth, moon]
    
    @staticmethod
    def binary_stars():
        """Binary star system with equal mass stars."""
        mass = SOLAR_MASS
        separation = 1.0 * AU
        velocity = 25000  # m/s
        
        star1 = CelestialBody("Star A", mass, -separation/2, 0, 0, -velocity, "#FDB813")
        star2 = CelestialBody("Star B", mass, separation/2, 0, 0, velocity, "#FF6B35")
        return [star1, star2]
    
    @staticmethod
    def planetary_system():
        """Solar system-like with multiple planets."""
        sun = CelestialBody("Sun", SOLAR_MASS, 0, 0, 0, 0, "#FDB813")
        
        # Inner planets (roughly)
        mercury = CelestialBody("Mercury", EARTH_MASS * 0.055, 
                               0.39*AU, 0, 0, 47870, "#8C7853")
        venus = CelestialBody("Venus", EARTH_MASS * 0.815, 
                             0.72*AU, 0, 0, 35020, "#FFC649")
        earth = CelestialBody("Earth", EARTH_MASS, 
                             AU, 0, 0, 29780, "#4A90E2")
        mars = CelestialBody("Mars", EARTH_MASS * 0.107, 
                            1.52*AU, 0, 0, 24070, "#E27B58")
        
        # Outer planet
        jupiter = CelestialBody("Jupiter", JUPITER_MASS, 
                               5.2*AU, 0, 0, 13070, "#C88B3A")
        
        return [sun, mercury, venus, earth, mars, jupiter]
    
    @staticmethod
    def chaotic_three_body():
        """Three-body system designed for chaotic behavior."""
        bodies = [
            CelestialBody("Sun 1", SOLAR_MASS, -1.5*AU, 0, 0, -15000, "#FDB813"),
            CelestialBody("Sun 2", SOLAR_MASS, 1.5*AU, 0, 0, 15000, "#FF6B35"),
            CelestialBody("Sun 3", SOLAR_MASS, 0, 1.5*AU, -15000, 0, "#FF0000"),
        ]
        return bodies


# Color palette for bodies
COLOR_PALETTE = [
    "#FDB813",  # Golden yellow (sun-like)
    "#FF6B35",  # Orange
    "#FF0000",  # Red
    "#4A90E2",  # Blue (earth-like)
    "#00FF00",  # Green
    "#FF00FF",  # Magenta
    "#FFFF00",  # Yellow
    "#00FFFF",  # Cyan
    "#C88B3A",  # Brown (jupiter-like)
    "#CCCCCC",  # Gray (moon-like)
]


# Default simulation parameters
DEFAULT_TIME_STEP = 3600.0  # 1 hour in seconds
DEFAULT_ZOOM = 3.0  # AU
