"""Physics calculations for orbital mechanics."""

import math
from typing import Tuple


def calculate_orbital_velocity(
    central_mass: float,
    orbiting_mass: float,
    distance: float,
    G: float = 6.67430e-11
) -> float:
    """
    Calculate circular orbital velocity for a body orbiting another.
    
    Args:
        central_mass: Mass of the central body (kg)
        orbiting_mass: Mass of the orbiting body (kg) - typically negligible
        distance: Distance between bodies (m)
        G: Gravitational constant
        
    Returns:
        Orbital velocity in m/s
    """
    if distance <= 0:
        return 0.0
    
    # For circular orbit: v = sqrt(G * M / r)
    # We use (M1 + M2) for accuracy, but typically M2 << M1
    total_mass = central_mass + orbiting_mass
    velocity = math.sqrt(G * total_mass / distance)
    
    return velocity


def calculate_escape_velocity(
    mass: float,
    distance: float,
    G: float = 6.67430e-11
) -> float:
    """
    Calculate escape velocity from a body at given distance.
    
    Args:
        mass: Mass of the body (kg)
        distance: Distance from center (m)
        G: Gravitational constant
        
    Returns:
        Escape velocity in m/s
    """
    if distance <= 0:
        return 0.0
    
    # v_escape = sqrt(2 * G * M / r)
    velocity = math.sqrt(2 * G * mass / distance)
    
    return velocity


def calculate_orbital_velocity_vector(
    central_pos: Tuple[float, float],
    orbiting_pos: Tuple[float, float],
    central_mass: float,
    orbiting_mass: float = 0.0,
    G: float = 6.67430e-11,
    clockwise: bool = False
) -> Tuple[float, float]:
    """
    Calculate velocity vector for circular orbit.
    
    Args:
        central_pos: (x, y) position of central body
        orbiting_pos: (x, y) position of orbiting body
        central_mass: Mass of central body (kg)
        orbiting_mass: Mass of orbiting body (kg)
        G: Gravitational constant
        clockwise: If True, orbit clockwise; else counter-clockwise
        
    Returns:
        (vx, vy) velocity vector in m/s
    """
    # Calculate distance and direction
    dx = orbiting_pos[0] - central_pos[0]
    dy = orbiting_pos[1] - central_pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance == 0:
        return (0.0, 0.0)
    
    # Calculate orbital speed
    speed = calculate_orbital_velocity(central_mass, orbiting_mass, distance, G)
    
    # Velocity is perpendicular to position vector
    # Normalize direction vector
    dx_norm = dx / distance
    dy_norm = dy / distance
    
    # Rotate 90 degrees (perpendicular)
    if clockwise:
        vx = speed * dy_norm
        vy = -speed * dx_norm
    else:
        vx = -speed * dy_norm
        vy = speed * dx_norm
    
    return (vx, vy)


def distance_between_points(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx**2 + dy**2)


def vector_magnitude(vx: float, vy: float) -> float:
    """Calculate magnitude of a vector."""
    return math.sqrt(vx**2 + vy**2)


def normalize_vector(vx: float, vy: float) -> Tuple[float, float]:
    """Normalize a vector to unit length."""
    mag = vector_magnitude(vx, vy)
    if mag == 0:
        return (0.0, 0.0)
    return (vx / mag, vy / mag)
