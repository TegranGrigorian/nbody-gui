"""Configuration and preset scenarios."""

from models import CelestialBody
from utils import SOLAR_MASS, EARTH_MASS, JUPITER_MASS, AU


# Additional constants
MOON_MASS = EARTH_MASS * 0.0123
MARS_MASS = EARTH_MASS * 0.107
VENUS_MASS = EARTH_MASS * 0.815
MERCURY_MASS = EARTH_MASS * 0.055
SATURN_MASS = JUPITER_MASS * 0.299
URANUS_MASS = EARTH_MASS * 14.536
NEPTUNE_MASS = EARTH_MASS * 17.147

# Jovian moon masses (relative to Earth)
IO_MASS = EARTH_MASS * 0.015
EUROPA_MASS = EARTH_MASS * 0.008
GANYMEDE_MASS = EARTH_MASS * 0.025
CALLISTO_MASS = EARTH_MASS * 0.018


class ScenarioPresets:
    """Predefined simulation scenarios."""
    
    @staticmethod
    def solar_system():
        """Complete Solar System with all 8 planets and Earth's moon."""
        sun = CelestialBody("Sun", SOLAR_MASS, 0, 0, 0, 0, "#FDB813")
        
        mercury = CelestialBody("Mercury", MERCURY_MASS, 
                               0.387*AU, 0, 0, 47870, "#8C7853")
        venus = CelestialBody("Venus", VENUS_MASS, 
                             0.723*AU, 0, 0, 35020, "#FFC649")
        earth = CelestialBody("Earth", EARTH_MASS, 
                             1.0*AU, 0, 0, 29780, "#4A90E2")
        moon = CelestialBody("Moon", MOON_MASS, 
                            1.0*AU + 3.844e8, 0, 0, 29780 + 1022, "#CCCCCC")
        mars = CelestialBody("Mars", MARS_MASS, 
                            1.524*AU, 0, 0, 24070, "#E27B58")
        jupiter = CelestialBody("Jupiter", JUPITER_MASS, 
                               5.203*AU, 0, 0, 13070, "#C88B3A")
        saturn = CelestialBody("Saturn", SATURN_MASS, 
                              9.537*AU, 0, 0, 9690, "#F4D03F")
        uranus = CelestialBody("Uranus", URANUS_MASS, 
                              19.191*AU, 0, 0, 6800, "#4FC3F7")
        neptune = CelestialBody("Neptune", NEPTUNE_MASS, 
                               30.069*AU, 0, 0, 5430, "#5C6BC0")
        
        return [sun, mercury, venus, earth, moon, mars, jupiter, saturn, uranus, neptune]
    
    @staticmethod
    def earth_moon():
        """Earth-Moon system orbiting the Sun."""
        sun = CelestialBody("Sun", SOLAR_MASS, 0, 0, 0, 0, "#FDB813")
        earth = CelestialBody("Earth", EARTH_MASS, AU, 0, 0, 29780, "#4A90E2")
        # Moon orbits Earth at 384,400 km
        moon = CelestialBody("Moon", MOON_MASS, 
                            AU + 3.844e8, 0, 0, 29780 + 1022, "#CCCCCC")
        return [sun, earth, moon]
    
    @staticmethod
    def jupiter_moons():
        """Jupiter with its 4 Galilean moons (Io, Europa, Ganymede, Callisto)."""
        sun = CelestialBody("Sun", SOLAR_MASS, 0, 0, 0, 0, "#FDB813")
        jupiter = CelestialBody("Jupiter", JUPITER_MASS, 
                               5.203*AU, 0, 0, 13070, "#C88B3A")
        
        # Galilean moons with velocities relative to Jupiter
        jupiter_v = 13070
        io = CelestialBody("Io", IO_MASS, 
                          5.203*AU + 4.217e8, 0, 0, jupiter_v + 17334, "#FFF59D")
        europa = CelestialBody("Europa", EUROPA_MASS, 
                              5.203*AU + 6.709e8, 0, 0, jupiter_v + 13740, "#BCAAA4")
        ganymede = CelestialBody("Ganymede", GANYMEDE_MASS, 
                                5.203*AU + 1.0704e9, 0, 0, jupiter_v + 10880, "#E0E0E0")
        callisto = CelestialBody("Callisto", CALLISTO_MASS, 
                                5.203*AU + 1.8827e9, 0, 0, jupiter_v + 8204, "#9E9E9E")
        
        return [sun, jupiter, io, europa, ganymede, callisto]
    
    @staticmethod
    def three_body_problem():
        """
        Three-Body Problem: Triple star system with a planet (Liu Cixin inspired).
        Hierarchical triple system with planet in stable P-type orbit around binary.
        """
        # Close binary pair (Alpha and Beta) - tighter orbit for more stability
        # Circular orbit around common center of mass
        
        alpha = CelestialBody("Alpha", SOLAR_MASS * 1.0, 
                             -0.3*AU, 0, 0, -30000, "#FDB813")
        beta = CelestialBody("Beta", SOLAR_MASS * 1.0, 
                            0.3*AU, 0, 0, 30000, "#FF6B35")
        
        # Distant third star (Gamma) in wide orbit - provides chaotic perturbations
        # Much further out to avoid disrupting the planet
        gamma = CelestialBody("Gamma", SOLAR_MASS * 0.8, 
                             0, 6.0*AU, -6500, 0, "#FF0000")
        
        # Planet in P-type circumbinary orbit around Alpha-Beta pair
        # Positioned well outside the binary (>3x separation) for Hill stability
        # Velocity calculated for roughly circular orbit around binary center
        planet = CelestialBody("Trisolaris", EARTH_MASS * 2.0, 
                              2.2*AU, 0, 0, 22000, "#4A90E2")
        
        return [alpha, beta, gamma, planet]
    
    @staticmethod
    def alpha_centauri():
        """
        Alpha Centauri: Triple star system (Alpha Cen A, B, and Proxima).
        A and B are binary, Proxima orbits distantly.
        """
        # Alpha Centauri A and B binary system
        alpha_a = CelestialBody("Alpha Cen A", SOLAR_MASS * 1.1, 
                               -11.2*AU, 0, 0, -22000, "#FFF9C4")
        alpha_b = CelestialBody("Alpha Cen B", SOLAR_MASS * 0.907, 
                               11.8*AU, 0, 0, 23000, "#FFE082")
        
        # Proxima Centauri - distant red dwarf companion
        proxima = CelestialBody("Proxima Cen", SOLAR_MASS * 0.123, 
                               0, 8000*AU, -500, 0, "#EF5350")
        
        return [alpha_a, alpha_b, proxima]
    
    @staticmethod
    def figure_8():
        """Figure-8 choreography - stable three-body periodic orbit."""
        mass = SOLAR_MASS
        bodies = [
            CelestialBody("Body 1", mass, -1.0*AU, 0, 0, -15000, "#FDB813"),
            CelestialBody("Body 2", mass, 1.0*AU, 0, 0, 17500, "#FF6B35"),
            CelestialBody("Body 3", mass, 0, 1.5*AU, -20000, 0, "#FF0000"),
        ]
        return bodies
    
    @staticmethod
    def binary_stars():
        """Binary star system with equal mass stars."""
        mass = SOLAR_MASS
        separation = 1.0 * AU
        velocity = 25000
        
        star1 = CelestialBody("Star A", mass, -separation/2, 0, 0, -velocity, "#FDB813")
        star2 = CelestialBody("Star B", mass, separation/2, 0, 0, velocity, "#FF6B35")
        return [star1, star2]


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
