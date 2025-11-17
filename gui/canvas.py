"""Simulation canvas for rendering and interaction."""

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyArrow
import math
from typing import Optional, Tuple, Callable

from models import CelestialBody, SimulationState
from models.simulation_state import SimulationMode
from utils import AU


class SimulationCanvas:
    """Canvas for displaying and interacting with the simulation."""
    
    def __init__(self, parent, simulation_state: SimulationState):
        """
        Initialize the simulation canvas.
        
        Args:
            parent: Parent tkinter widget
            simulation_state: Shared simulation state
        """
        self.parent = parent
        self.state = simulation_state
        
        # Callbacks for mode changes
        self.on_body_selected: Optional[Callable[[CelestialBody], None]] = None
        
        # Canvas state
        self.zoom_level = 3.0  # AU multiplier for view
        self.center_x = 0.0
        self.center_y = 0.0
        
        # Camera tracking modes
        self.auto_zoom_to_cog = False
        self.capture_all_bodies = False
        self.focus_body_mode = False
        self.focused_body: Optional[CelestialBody] = None
        self.frame_counter = 0
        
        # Interaction state
        self.velocity_arrow: Optional[FancyArrow] = None
        self.velocity_start_pos: Optional[Tuple[float, float]] = None
        
        # Panning state (for simulation mode)
        self.is_panning = False
        self.pan_start_x = 0.0
        self.pan_start_y = 0.0
        self.pan_center_x_start = 0.0
        self.pan_center_y_start = 0.0
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Setup plot
        self.setup_plot()
        
        # Bind mouse events
        self.canvas.mpl_connect('button_press_event', self.on_mouse_click)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        
        # Plot elements storage
        self.body_artists = {}
        self.trail_artists = {}
        
        # Dragging state
        self.is_dragging_arrow = False
        
    def setup_plot(self):
        """Setup the plot appearance."""
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_facecolor('#0a0a0a')
        self.fig.patch.set_facecolor('#1a1a1a')
        self.update_view_limits()
        
    def update_view_limits(self):
        """Update the view limits based on zoom and center."""
        limit = self.zoom_level * AU
        self.ax.set_xlim(self.center_x - limit, self.center_x + limit)
        self.ax.set_ylim(self.center_y - limit, self.center_y + limit)
        self.ax.set_xlabel('X Position (m)', color='white')
        self.ax.set_ylabel('Y Position (m)', color='white')
        self.ax.tick_params(colors='white')
        
    def on_mouse_click(self, event):
        """Handle mouse click events."""
        if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
            return
        
        click_x, click_y = event.xdata, event.ydata
        
        if self.state.mode == SimulationMode.GOD_MODE:
            self.handle_god_mode_click(click_x, click_y, event.button)
        elif self.state.mode == SimulationMode.SIMULATION_MODE:
            # Start panning in simulation mode
            if event.button == 1:  # Left click
                self.is_panning = True
                self.pan_start_x = click_x
                self.pan_start_y = click_y
                self.pan_center_x_start = self.center_x
                self.pan_center_y_start = self.center_y
    
    def on_mouse_release(self, event):
        """Handle mouse release events."""
        # Handle panning end (even if mouse is outside axes)
        if self.state.mode == SimulationMode.SIMULATION_MODE and self.is_panning:
            self.is_panning = False
            return
        
        if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
            return
        
        if self.state.mode == SimulationMode.GOD_MODE:
            # Check if we were dragging a velocity arrow
            selected = self.state.get_selected_body()
            if selected and selected.is_setting_velocity and self.is_dragging_arrow:
                # Set the final velocity based on arrow
                end_x, end_y = event.xdata, event.ydata
                start_x, start_y = selected.get_position()
                
                # Calculate velocity vector (scale: 1 AU = 30 km/s)
                scale = 30000.0 / AU
                vx = (end_x - start_x) * scale
                vy = (end_y - start_y) * scale
                
                selected.set_velocity(vx, vy)
                
                # Update the editor display
                if self.on_body_selected:
                    self.on_body_selected(selected)
                
                self.is_dragging_arrow = False
                self.render()
    
    def handle_god_mode_click(self, x: float, y: float, button: int):
        """Handle clicks in God Mode."""
        # Check if clicking on existing body
        clicked_body = self.find_body_at_position(x, y)
        
        # Check if we're in orbit target selection mode
        if hasattr(self, 'body_editor_ref') and self.body_editor_ref and self.body_editor_ref.is_selecting_orbit_target:
            if clicked_body:
                # Set this body as the orbit target
                self.body_editor_ref.set_orbit_target(clicked_body)
                self.render()
                return
            else:
                # Clicked empty space, cancel selection
                from tkinter import messagebox
                messagebox.showinfo("Selection Cancelled", "Click on a body to set as orbit target.")
                return
        
        # Check if we're in velocity setting mode
        selected = self.state.get_selected_body()
        if selected and selected.is_setting_velocity:
            # Start dragging the velocity arrow
            self.is_dragging_arrow = True
            return
        
        if clicked_body:
            # Select the body
            self.state.deselect_all()
            clicked_body.is_selected = True
            if self.on_body_selected:
                self.on_body_selected(clicked_body)
        else:
            # Add new body at click location
            if button == 1:  # Left click
                self.add_new_body_at_position(x, y)
        
        self.render()
    
    def find_body_at_position(self, x: float, y: float, tolerance: float = 0.1) -> Optional[CelestialBody]:
        """Find a body near the given position."""
        tolerance_meters = tolerance * AU
        
        for body in self.state.bodies:
            bx, by = body.get_position()
            distance = math.sqrt((bx - x)**2 + (by - y)**2)
            if distance < tolerance_meters:
                return body
        return None
    
    def add_new_body_at_position(self, x: float, y: float):
        """Add a new body at the given position."""
        from utils import EARTH_MASS
        
        # Create a new body with default properties
        body_num = len(self.state.bodies) + 1
        colors = ['#FDB813', '#FF6B35', '#FF0000', '#4A90E2', '#00FF00', '#FF00FF', '#FFFF00']
        color = colors[body_num % len(colors)]
        
        new_body = CelestialBody(
            name=f"Body {body_num}",
            mass=EARTH_MASS,
            x=x,
            y=y,
            vx=0.0,
            vy=0.0,
            color=color
        )
        
        self.state.add_body(new_body)
        self.state.deselect_all()
        new_body.is_selected = True
        
        if self.on_body_selected:
            self.on_body_selected(new_body)
        
        self.render()
    
    def on_mouse_move(self, event):
        """Handle mouse movement."""
        if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
            return
        
        # Handle panning in simulation mode
        if self.state.mode == SimulationMode.SIMULATION_MODE and self.is_panning:
            current_x, current_y = event.xdata, event.ydata
            
            # Calculate pan offset
            dx = current_x - self.pan_start_x
            dy = current_y - self.pan_start_y
            
            # Update center position (subtract because we're moving the view)
            self.center_x = self.pan_center_x_start - dx
            self.center_y = self.pan_center_y_start - dy
            
            # Disable auto-tracking when user pans
            if self.auto_zoom_to_cog or self.capture_all_bodies or self.focus_body_mode:
                self.auto_zoom_to_cog = False
                self.capture_all_bodies = False
                self.focus_body_mode = False
                self.focused_body = None
                # Update control panel buttons if they exist
                if hasattr(self, 'control_panel_ref'):
                    self.control_panel_ref.update_camera_buttons()
            
            self.update_view_limits()
            self.render()
            return
        
        if self.state.mode == SimulationMode.GOD_MODE:
            # Check if any body is in velocity-setting mode
            selected = self.state.get_selected_body()
            if selected and selected.is_setting_velocity:
                # Update velocity arrow as we drag
                start_x, start_y = selected.get_position()
                end_x, end_y = event.xdata, event.ydata
                
                # Remove old arrow if exists
                if self.velocity_arrow:
                    self.velocity_arrow.remove()
                    self.velocity_arrow = None
                
                # Remove old velocity text if exists
                for txt in self.ax.texts[:]:
                    if hasattr(txt, 'is_velocity_text'):
                        txt.remove()
                
                # Draw new arrow
                dx = end_x - start_x
                dy = end_y - start_y
                
                # Only draw if we have some distance
                distance = (dx**2 + dy**2)**0.5
                if distance > 0.01 * AU:
                    self.velocity_arrow = self.ax.arrow(
                        start_x, start_y, dx, dy,
                        head_width=0.1*AU, head_length=0.15*AU,
                        fc='yellow', ec='yellow', linewidth=3, alpha=0.8, zorder=10
                    )
                    
                    # Show velocity magnitude as text near arrow tip
                    # Scale: 1 AU = 30 km/s
                    scale = 30000.0 / AU
                    velocity = distance * scale
                    
                    # Position text at midpoint of arrow
                    text_x = start_x + dx * 0.6
                    text_y = start_y + dy * 0.6
                    
                    vel_text = self.ax.text(text_x, text_y, f"{velocity:.0f} m/s",
                                          color='yellow', fontsize=10, fontweight='bold',
                                          ha='center', va='bottom', zorder=11,
                                          bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
                    vel_text.is_velocity_text = True
                    
                    self.canvas.draw_idle()
    
    def render(self):
        """Render all bodies and trails."""
        # Clear previous artists
        for artist in list(self.body_artists.values()):
            artist.remove()
        for artist in list(self.trail_artists.values()):
            artist.remove()
        self.body_artists.clear()
        self.trail_artists.clear()
        
        # Clear velocity arrow if exists
        if self.velocity_arrow:
            self.velocity_arrow.remove()
            self.velocity_arrow = None
        
        # Clear ALL text objects (labels and velocity text)
        for txt in self.ax.texts[:]:
            txt.remove()
        
        # Clear all patches (selection circles, etc.)
        for patch in self.ax.patches[:]:
            patch.remove()
        
        # Update camera if in simulation mode
        if self.state.mode == SimulationMode.SIMULATION_MODE:
            self.frame_counter += 1
            
            # Focus on specific body mode (highest priority)
            if self.focus_body_mode and self.focused_body and self.focused_body in self.state.bodies:
                x, y = self.focused_body.get_position()
                self.center_x = x
                self.center_y = y
                self.update_view_limits()
            # Auto zoom to center of gravity every 10 frames
            elif self.auto_zoom_to_cog and self.frame_counter % 10 == 0:
                self.center_to_cog()
            # Capture all bodies mode
            elif self.capture_all_bodies:
                self.zoom_to_capture_all()
        
        # Draw trails in simulation mode
        if self.state.mode == SimulationMode.SIMULATION_MODE:
            for i, trajectory in enumerate(self.state.trajectories):
                if len(trajectory) > 1:
                    x_vals, y_vals = zip(*trajectory)
                    trail, = self.ax.plot(x_vals, y_vals, '-', 
                                         color=self.state.bodies[i].color, 
                                         alpha=0.3, linewidth=1)
                    self.trail_artists[i] = trail
        
        # Draw bodies
        for body in self.state.bodies:
            x, y = body.get_position()
            
            # Size based on mass (logarithmic scale)
            mass_scale = math.log10(body.get_mass() / 1e24) if body.get_mass() > 0 else 1
            size = max(100, mass_scale * 50)
            
            # Only highlight if selected AND in God Mode
            if body.is_selected and self.state.mode == SimulationMode.GOD_MODE:
                size *= 1.5
                # Draw selection ring
                circle = plt.Circle((x, y), 0.15 * AU, color='white', 
                                  fill=False, linewidth=2, linestyle='--')
                self.ax.add_patch(circle)
            
            # Draw body
            scatter = self.ax.scatter([x], [y], s=size, c=[body.color], 
                                     edgecolors='white', linewidths=1, zorder=5)
            self.body_artists[body] = scatter
            
            # Draw label
            text = self.ax.text(x, y + 0.2*AU, body.name, 
                              color='white', fontsize=9, 
                              ha='center', va='bottom', zorder=6)
        
        # Draw velocity arrow ONLY in God Mode for selected body
        if self.state.mode == SimulationMode.GOD_MODE:
            selected = self.state.get_selected_body()
            if selected:
                vx, vy = selected.get_velocity()
                x, y = selected.get_position()
                
                # Show arrow if in velocity setting mode OR if velocity is non-zero
                if selected.is_setting_velocity or (vx != 0 or vy != 0):
                    # Scale velocity for visualization (1 AU per 30 km/s)
                    scale = AU / 30000.0
                    arrow_dx = vx * scale
                    arrow_dy = vy * scale
                    
                    # Only draw if arrow has some length
                    arrow_length = (arrow_dx**2 + arrow_dy**2)**0.5
                    if arrow_length > 0.01 * AU:
                        color = 'yellow' if selected.is_setting_velocity else 'cyan'
                        alpha = 0.8 if selected.is_setting_velocity else 0.6
                        linewidth = 3 if selected.is_setting_velocity else 2
                        
                        self.velocity_arrow = self.ax.arrow(x, y, arrow_dx, arrow_dy,
                                            head_width=0.1*AU, head_length=0.15*AU,
                                            fc=color, ec=color, linewidth=linewidth, 
                                            alpha=alpha, zorder=7)
        
        self.canvas.draw()
    
    def zoom_in(self):
        """Zoom in the view."""
        self.zoom_level *= 0.7
        self.update_view_limits()
        self.render()
    
    def zoom_out(self):
        """Zoom out the view."""
        self.zoom_level *= 1.3
        self.update_view_limits()
        self.render()
    
    def reset_view(self):
        """Reset view to default."""
        self.zoom_level = 3.0
        self.center_x = 0.0
        self.center_y = 0.0
        self.update_view_limits()
        self.render()
    
    def center_to_cog(self):
        """Center view on center of gravity."""
        if not self.state.bodies:
            return
        
        # Calculate center of gravity
        total_mass = 0.0
        cog_x = 0.0
        cog_y = 0.0
        
        for body in self.state.bodies:
            mass = body.get_mass()
            x, y = body.get_position()
            cog_x += mass * x
            cog_y += mass * y
            total_mass += mass
        
        if total_mass > 0:
            cog_x /= total_mass
            cog_y /= total_mass
            
            self.center_x = cog_x
            self.center_y = cog_y
            self.update_view_limits()
    
    def zoom_to_capture_all(self):
        """Zoom to capture all bodies in view."""
        if not self.state.bodies:
            return
        
        # Find bounding box of all bodies
        positions = [body.get_position() for body in self.state.bodies]
        if not positions:
            return
        
        x_coords, y_coords = zip(*positions)
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        
        # Add padding (20%)
        x_range = max_x - min_x
        y_range = max_y - min_y
        padding = 0.2
        
        min_x -= x_range * padding
        max_x += x_range * padding
        min_y -= y_range * padding
        max_y += y_range * padding
        
        # Center on midpoint
        self.center_x = (min_x + max_x) / 2
        self.center_y = (min_y + max_y) / 2
        
        # Set zoom to capture all
        x_span = (max_x - min_x) / 2
        y_span = (max_y - min_y) / 2
        max_span = max(x_span, y_span)
        
        self.zoom_level = max_span / AU if max_span > 0 else 3.0
        self.update_view_limits()
    
    def toggle_auto_zoom_cog(self):
        """Toggle auto zoom to center of gravity."""
        self.auto_zoom_to_cog = not self.auto_zoom_to_cog
        return self.auto_zoom_to_cog
    
    def toggle_capture_all(self):
        """Toggle capture all bodies mode."""
        self.capture_all_bodies = not self.capture_all_bodies
        return self.capture_all_bodies
    
    def toggle_focus_body(self):
        """Toggle focus body mode."""
        self.focus_body_mode = not self.focus_body_mode
        if not self.focus_body_mode:
            self.focused_body = None
        return self.focus_body_mode
    
    def set_focused_body(self, body: Optional[CelestialBody]):
        """Set the body to focus on."""
        self.focused_body = body
        if body is not None:
            self.focus_body_mode = True
            # Disable other camera modes
            self.auto_zoom_to_cog = False
            self.capture_all_bodies = False
        else:
            self.focus_body_mode = False
