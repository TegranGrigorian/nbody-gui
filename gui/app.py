"""Main application class that orchestrates all GUI components."""

import tkinter as tk
from tkinter import ttk

from models import SimulationState, CelestialBody
from models.simulation_state import SimulationMode
from config.presets import ScenarioPresets
from .canvas import SimulationCanvas
from .control_panel import ControlPanel
from .body_editor import BodyEditorPanel
from .preset_menu import PresetMenu


class NBodyApp:
    """Main N-Body simulation application."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the application.
        
        Args:
            root: Root tkinter window
        """
        self.root = root
        self.root.title("N-Body Simulation - God Mode")
        self.root.geometry("1600x900")
        
        # Configure button styles
        style = ttk.Style()
        style.configure('Active.TButton', background='#4A90E2', foreground='white')
        
        # Shared simulation state
        self.state = SimulationState()
        
        # Create UI components
        self.control_panel = ControlPanel(self.root, self.state)
        
        # Add preset menu to control panel frame
        self.preset_menu = PresetMenu(self.control_panel.frame)
        
        # Main content area
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Body editor on the left - always show in God Mode
        self.body_editor = BodyEditorPanel(content_frame, self.state)
        self.body_editor.show()  # Make it visible by default
        
        # Canvas in the center/right
        self.canvas = SimulationCanvas(content_frame, self.state)
        
        # Connect callbacks
        self.setup_callbacks()
        
        # Animation loop
        self.animation_running = False
        self.animation_steps_per_frame = 10
        self.start_animation_loop()
    
    def setup_callbacks(self):
        """Setup callbacks between components."""
        # Canvas callbacks
        self.canvas.on_body_selected = self.on_body_selected
        
        # Give canvas a reference to body editor for orbit target selection
        self.canvas.body_editor_ref = self.body_editor
        
        # Control panel callbacks
        self.control_panel.on_mode_change = self.on_mode_change
        self.control_panel.on_clear_all = self.clear_all_bodies
        
        # Body editor callbacks
        self.body_editor.on_body_updated = self.on_body_updated
        
        # View control callbacks
        self.control_panel.zoom_in_button.config(command=self.canvas.zoom_in)
        self.control_panel.zoom_out_button.config(command=self.canvas.zoom_out)
        self.control_panel.reset_view_button.config(command=self.canvas.reset_view)
        self.control_panel.auto_cog_button.config(command=self.toggle_auto_cog)
        self.control_panel.capture_all_button.config(command=self.toggle_capture_all)
        self.control_panel.on_focus_body_selected = self.on_focus_body_selected
        
        # Update focus body list initially
        self.control_panel.update_focus_body_list()
        
        # Preset menu callback
        self.preset_menu.on_preset_selected = self.load_preset
    
    def on_body_selected(self, body: CelestialBody):
        """Handle body selection from canvas."""
        self.body_editor.set_body(body)
    
    def on_body_updated(self):
        """Handle body updates from editor."""
        self.canvas.render()
    
    def on_mode_change(self):
        """Handle mode changes from control panel."""
        if self.state.mode == SimulationMode.SIMULATION_MODE:
            self.root.title("N-Body Simulation - Running")
            self.body_editor.hide()
        else:
            self.root.title("N-Body Simulation - God Mode")
            self.body_editor.show()
            # Reset to no selection state when returning to God Mode
            self.body_editor.set_body(None)
        
        self.canvas.render()
    
    def clear_all_bodies(self):
        """Clear all bodies from the simulation."""
        self.state.clear_all()
        
        # Reset body editor to no selection
        self.body_editor.set_body(None)
        
        # Turn off velocity arrow mode if it was on
        self.canvas.velocity_arrow = None
        self.canvas.is_dragging_arrow = False
        
        self.canvas.render()
    
    def toggle_auto_cog(self):
        """Toggle auto zoom to center of gravity."""
        is_active = self.canvas.toggle_auto_zoom_cog()
        
        # Update button appearance
        if is_active:
            self.control_panel.auto_cog_button.config(style='Active.TButton')
        else:
            self.control_panel.auto_cog_button.config(style='TButton')
    
    def toggle_capture_all(self):
        """Toggle capture all bodies mode."""
        is_active = self.canvas.toggle_capture_all()
        
        # Update button appearance
        if is_active:
            self.control_panel.capture_all_button.config(style='Active.TButton')
        else:
            self.control_panel.capture_all_button.config(style='TButton')
    
    def on_focus_body_selected(self, event=None):
        """Handle focus body selection from dropdown."""
        selected_name = self.control_panel.focus_body_var.get()
        
        if selected_name == "None":
            self.canvas.set_focused_body(None)
            # Disable other camera modes when deselecting
            self.control_panel.auto_cog_button.config(style='TButton')
            self.control_panel.capture_all_button.config(style='TButton')
        else:
            # Find the body by name
            for body in self.state.bodies:
                if body.name == selected_name:
                    self.canvas.set_focused_body(body)
                    # Disable other camera modes when focusing on a body
                    self.control_panel.auto_cog_button.config(style='TButton')
                    self.control_panel.capture_all_button.config(style='TButton')
                    break
    
    def load_preset(self, preset_id: str):
        """Load a preset configuration."""
        # Map preset IDs to methods
        preset_map = {
            'solar_system': ScenarioPresets.solar_system,
            'earth_moon': ScenarioPresets.earth_moon,
            'jupiter_moons': ScenarioPresets.jupiter_moons,
            'three_body_problem': ScenarioPresets.three_body_problem,
            'alpha_centauri': ScenarioPresets.alpha_centauri,
            'binary_stars': ScenarioPresets.binary_stars,
            'figure_8': ScenarioPresets.figure_8,
        }
        
        if preset_id in preset_map:
            # Clear existing bodies
            self.state.clear_all()
            
            # Load preset bodies
            bodies = preset_map[preset_id]()
            for body in bodies:
                self.state.add_body(body)
            
            # Reset view and render
            self.canvas.reset_view()
            self.canvas.render()
            
            # Clear body editor selection
            self.body_editor.set_body(None)
            
            # Update focus body list
            self.control_panel.update_focus_body_list()
            self.control_panel.focus_body_var.set("None")
    
    def start_animation_loop(self):
        """Start the main animation loop."""
        self.animation_running = True
        self.animation_loop()
    
    def animation_loop(self):
        """Main animation loop for simulation updates."""
        if not self.animation_running:
            return
        
        # If in simulation mode and running, step the simulation
        if self.state.mode == SimulationMode.SIMULATION_MODE and self.state.is_running:
            # Calculate steps based on time warp
            steps = int(self.animation_steps_per_frame * self.state.time_warp)
            steps = max(1, min(steps, 1000))  # Clamp between 1 and 1000
            
            for _ in range(steps):
                self.state.step_simulation()
            
            # Update display
            self.canvas.render()
            self.control_panel.update_time_display()
            
            # Schedule next frame (30 FPS target)
            delay = 33
        else:
            # Slower update when not running
            delay = 100
        
        # Use a lambda to avoid method reference issues
        self.root.after(delay, lambda: self.animation_loop())
    
    def run(self):
        """Run the application."""
        self.root.mainloop()
    
    def on_close(self):
        """Handle application close."""
        self.animation_running = False
        self.root.destroy()
