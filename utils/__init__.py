"""Utility functions and constants."""

from .physics import (
    calculate_orbital_velocity, 
    calculate_escape_velocity,
    calculate_orbital_velocity_vector,
    distance_between_points,
    vector_magnitude,
    normalize_vector
)
from .constants import *

__all__ = [
    'calculate_orbital_velocity',
    'calculate_escape_velocity',
    'calculate_orbital_velocity_vector',
    'distance_between_points',
    'vector_magnitude',
    'normalize_vector',
    'G',
    'AU',
    'SOLAR_MASS',
    'EARTH_MASS',
    'EARTH_RADIUS',
    'JUPITER_MASS',
]
