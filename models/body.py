"""Celestial body model wrapper around nbody.Body."""

import nbody
from typing import Optional, Tuple


class CelestialBody:
    """Wrapper class for nbody.Body with additional metadata and state."""
    
    def __init__(self, name: str, mass: float, x: float, y: float, vx: float, vy: float, color: str = "#FFFFFF"):
        """
        Initialize a celestial body.
        
        Args:
            name: Display name of the body
            mass: Mass in kg
            x: Initial x position in meters
            y: Initial y position in meters
            vx: Initial velocity in x direction (m/s)
            vy: Initial velocity in y direction (m/s)
            color: Hex color for visualization
        """
        self.name = name
        self.color = color
        self.initial_mass = mass
        self.initial_position = (x, y)
        self.initial_velocity = (vx, vy)
        
        # Create the actual nbody.Body
        self.nbody_body = nbody.Body(mass, x, y, vx, vy)
        
        # For God Mode editing
        self.is_selected = False
        self.is_setting_velocity = False
        self.velocity_arrow_start: Optional[Tuple[float, float]] = None
        
    def get_position(self) -> Tuple[float, float]:
        """Get current position as (x, y) tuple."""
        return (self.nbody_body.get_x(), self.nbody_body.get_y())
    
    def get_velocity(self) -> Tuple[float, float]:
        """Get current velocity as (vx, vy) tuple."""
        return (self.nbody_body.get_v_x(), self.nbody_body.get_v_y())
    
    def set_position(self, x: float, y: float):
        """Set body position."""
        # Need to recreate the body with new position
        vx, vy = self.get_velocity()
        mass = self.nbody_body.get_mass()
        self.nbody_body = nbody.Body(mass, x, y, vx, vy)
        
    def set_velocity(self, vx: float, vy: float):
        """Set body velocity."""
        # Need to recreate the body with new velocity
        x, y = self.get_position()
        mass = self.nbody_body.get_mass()
        self.nbody_body = nbody.Body(mass, x, y, vx, vy)
    
    def set_mass(self, mass: float):
        """Set body mass."""
        x, y = self.get_position()
        vx, vy = self.get_velocity()
        self.nbody_body = nbody.Body(mass, x, y, vx, vy)
        self.initial_mass = mass
    
    def get_mass(self) -> float:
        """Get body mass."""
        return self.nbody_body.get_mass()
    
    def reset_to_initial(self):
        """Reset body to initial conditions."""
        x, y = self.initial_position
        vx, vy = self.initial_velocity
        self.nbody_body = nbody.Body(self.initial_mass, x, y, vx, vy)
    
    def distance_to_point(self, px: float, py: float) -> float:
        """Calculate distance from body to a point."""
        x, y = self.get_position()
        return ((x - px)**2 + (y - py)**2)**0.5
    
    def __repr__(self):
        x, y = self.get_position()
        vx, vy = self.get_velocity()
        return f"CelestialBody(name='{self.name}', pos=({x:.2e}, {y:.2e}), vel=({vx:.2e}, {vy:.2e}))"
