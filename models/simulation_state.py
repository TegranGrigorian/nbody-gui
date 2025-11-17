"""Simulation state manager."""

import nbody
from typing import List, Optional
from enum import Enum
from .body import CelestialBody


class SimulationMode(Enum):
    """Simulation mode enumeration."""
    GOD_MODE = "god"
    SIMULATION_MODE = "simulation"


class SimulationState:
    """Manages the overall simulation state and bodies."""
    
    def __init__(self):
        """Initialize simulation state."""
        self.bodies: List[CelestialBody] = []
        self.kosmos: Optional[nbody.Kosmos] = None
        self.mode = SimulationMode.GOD_MODE
        self.is_running = False
        self.time_elapsed = 0.0  # in seconds
        self.time_step = 3600.0  # 1 hour default
        self.time_warp = 1.0  # 1x speed
        
        # Trajectory storage for visualization
        self.trajectories: List[List[tuple]] = []
        
    def add_body(self, body: CelestialBody):
        """Add a body to the simulation."""
        self.bodies.append(body)
        self.trajectories.append([])
        
    def remove_body(self, body: CelestialBody):
        """Remove a body from the simulation."""
        if body in self.bodies:
            index = self.bodies.index(body)
            self.bodies.pop(index)
            self.trajectories.pop(index)
    
    def get_selected_body(self) -> Optional[CelestialBody]:
        """Get the currently selected body."""
        for body in self.bodies:
            if body.is_selected:
                return body
        return None
    
    def deselect_all(self):
        """Deselect all bodies."""
        for body in self.bodies:
            body.is_selected = False
    
    def switch_to_simulation_mode(self):
        """Switch from God Mode to Simulation Mode."""
        if self.mode == SimulationMode.SIMULATION_MODE:
            return
        
        # Create Kosmos simulation with current bodies
        nbody_bodies = [body.nbody_body for body in self.bodies]
        self.kosmos = nbody.Kosmos(nbody_bodies)
        
        # Initialize trajectories with current positions
        for i, body in enumerate(self.bodies):
            self.trajectories[i] = [body.get_position()]
        
        self.mode = SimulationMode.SIMULATION_MODE
        self.time_elapsed = 0.0
        
    def switch_to_god_mode(self):
        """Switch from Simulation Mode back to God Mode."""
        if self.mode == SimulationMode.GOD_MODE:
            return
        
        self.mode = SimulationMode.GOD_MODE
        self.is_running = False
        self.kosmos = None
        
        # Reset bodies to initial conditions
        for body in self.bodies:
            body.reset_to_initial()
        
        # Clear trajectories
        self.trajectories = [[] for _ in self.bodies]
        self.time_elapsed = 0.0
    
    def step_simulation(self):
        """Advance simulation by one time step."""
        if self.mode != SimulationMode.SIMULATION_MODE or self.kosmos is None:
            return
        
        self.kosmos.step(self.time_step)
        self.time_elapsed += self.time_step
        
        # Update body references (Kosmos modifies the bodies)
        updated_bodies = self.kosmos.get_bodies()
        for i, body in enumerate(self.bodies):
            body.nbody_body = updated_bodies[i]
            
            # Store position for trajectory (store every step for now)
            self.trajectories[i].append(body.get_position())
    
    def clear_all(self):
        """Clear all bodies and reset state."""
        self.bodies.clear()
        self.trajectories.clear()
        self.kosmos = None
        self.is_running = False
        self.time_elapsed = 0.0
        self.mode = SimulationMode.GOD_MODE
    
    def get_time_string(self) -> str:
        """Get formatted time string."""
        days = self.time_elapsed / 86400
        years = days / 365.25
        
        if years >= 1:
            return f"{years:.2f} years"
        elif days >= 1:
            return f"{days:.2f} days"
        else:
            hours = self.time_elapsed / 3600
            return f"{hours:.2f} hours"
