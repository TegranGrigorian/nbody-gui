"""Body editor panel for modifying body properties in God Mode."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from models import CelestialBody, SimulationState
from utils import calculate_orbital_velocity_vector, G, SOLAR_MASS, EARTH_MASS, JUPITER_MASS


class BodyEditorPanel:
    """Panel for editing body properties in God Mode."""
    
    def __init__(self, parent, simulation_state: SimulationState):
        """
        Initialize body editor panel.
        
        Args:
            parent: Parent tkinter widget
            simulation_state: Shared simulation state
        """
        self.parent = parent
        self.state = simulation_state
        self.current_body: Optional[CelestialBody] = None
        
        # Callback for when body is updated
        self.on_body_updated = None
        
        # Auto-orbit state
        self.auto_orbit_enabled = False
        self.auto_orbit_target: Optional[CelestialBody] = None
        self.is_selecting_orbit_target = False  # New flag for target selection mode
        
        # Create frame
        self.frame = ttk.Frame(parent, padding="10", relief=tk.RIDGE, borderwidth=2)
        
        self.create_widgets()
        self.show()
    
    def create_widgets(self):
        """Create editor widgets."""
        # Title
        title = ttk.Label(self.frame, text="Body Editor", 
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        self.no_selection_label = ttk.Label(self.frame, 
                                            text="No body selected\n\nClick a body or\nclick canvas to add one",
                                            font=("Arial", 10), justify=tk.CENTER)
        self.no_selection_label.pack(pady=20)
        
        # Editor content frame (hidden until body selected)
        self.editor_frame = ttk.Frame(self.frame)
        
        # Name
        name_frame = ttk.LabelFrame(self.editor_frame, text="Name", padding="5")
        name_frame.pack(fill=tk.X, pady=5)
        
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(name_frame, textvariable=self.name_var, font=("Arial", 11))
        self.name_entry.pack(fill=tk.X)
        self.name_entry.bind('<Return>', lambda e: self.apply_changes())
        
        # Mass
        mass_frame = ttk.LabelFrame(self.editor_frame, text="Mass", padding="5")
        mass_frame.pack(fill=tk.X, pady=5)
        
        mass_input_frame = ttk.Frame(mass_frame)
        mass_input_frame.pack(fill=tk.X)
        
        self.mass_var = tk.StringVar()
        self.mass_entry = ttk.Entry(mass_input_frame, textvariable=self.mass_var, width=15)
        self.mass_entry.pack(side=tk.LEFT, padx=2)
        self.mass_entry.bind('<Return>', lambda e: self.apply_changes())
        
        ttk.Label(mass_input_frame, text="kg").pack(side=tk.LEFT)
        
        # Mass presets
        preset_frame = ttk.Frame(mass_frame)
        preset_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(preset_frame, text="Earth", width=8,
                  command=lambda: self.set_mass_preset(EARTH_MASS)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="Jupiter", width=8,
                  command=lambda: self.set_mass_preset(JUPITER_MASS)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="Sun", width=8,
                  command=lambda: self.set_mass_preset(SOLAR_MASS)).pack(side=tk.LEFT, padx=2)
        
        # Position (read-only display)
        pos_frame = ttk.LabelFrame(self.editor_frame, text="Position", padding="5")
        pos_frame.pack(fill=tk.X, pady=5)
        
        self.pos_label = ttk.Label(pos_frame, text="x: 0.00e+00 m\ny: 0.00e+00 m")
        self.pos_label.pack()
        
        # Velocity section
        velocity_frame = ttk.LabelFrame(self.editor_frame, text="Velocity", padding="5")
        velocity_frame.pack(fill=tk.X, pady=5)
        
        # Auto-orbit option
        self.auto_orbit_var = tk.BooleanVar(value=False)
        auto_orbit_check = ttk.Checkbutton(velocity_frame, text="Auto Orbit", 
                                          variable=self.auto_orbit_var,
                                          command=self.toggle_auto_orbit)
        auto_orbit_check.pack(anchor=tk.W, pady=2)
        
        # Auto-orbit controls
        self.auto_orbit_frame = ttk.Frame(velocity_frame)
        
        ttk.Label(self.auto_orbit_frame, 
                 text="Click another body to orbit:").pack(anchor=tk.W)
        
        self.orbit_target_label = ttk.Label(self.auto_orbit_frame, 
                                           text="No target selected",
                                           foreground="gray")
        self.orbit_target_label.pack(anchor=tk.W, pady=2)
        
        orbit_buttons = ttk.Frame(self.auto_orbit_frame)
        orbit_buttons.pack(fill=tk.X, pady=5)
        
        ttk.Button(orbit_buttons, text="Select Target", 
                  command=self.start_orbit_selection).pack(side=tk.LEFT, padx=2)
        ttk.Button(orbit_buttons, text="Apply Orbit", 
                  command=self.apply_auto_orbit).pack(side=tk.LEFT, padx=2)
        
        # Direction option
        self.orbit_clockwise_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.auto_orbit_frame, text="Clockwise", 
                       variable=self.orbit_clockwise_var).pack(anchor=tk.W)
        
        # Manual velocity
        self.manual_vel_frame = ttk.Frame(velocity_frame)
        self.manual_vel_frame.pack(fill=tk.X, pady=5)
        
        # Velocity display
        self.vel_label = ttk.Label(self.manual_vel_frame, text="vx: 0.00 m/s\nvy: 0.00 m/s")
        self.vel_label.pack(pady=2)
        
        # Velocity magnitude input
        vel_input_frame = ttk.Frame(self.manual_vel_frame)
        vel_input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(vel_input_frame, text="Speed:").pack(side=tk.LEFT, padx=2)
        self.velocity_magnitude_var = tk.StringVar(value="0")
        self.velocity_entry = ttk.Entry(vel_input_frame, textvariable=self.velocity_magnitude_var, width=12)
        self.velocity_entry.pack(side=tk.LEFT, padx=2)
        ttk.Label(vel_input_frame, text="m/s").pack(side=tk.LEFT, padx=2)
        self.velocity_entry.bind('<Return>', lambda e: self.apply_velocity_magnitude())
        
        # Velocity arrow buttons
        vel_button_frame = ttk.Frame(self.manual_vel_frame)
        vel_button_frame.pack(fill=tk.X, pady=5)
        
        self.create_velocity_button = ttk.Button(vel_button_frame, text="Create/Edit Velocity Arrow", 
                  command=self.toggle_velocity_arrow)
        self.create_velocity_button.pack(fill=tk.X, pady=2)
        
        ttk.Button(vel_button_frame, text="Apply Speed", 
                  command=self.apply_velocity_magnitude).pack(fill=tk.X, pady=2)
        
        ttk.Label(self.manual_vel_frame, 
                 text="Click 'Create/Edit Velocity Arrow',\nthen drag the arrow on canvas\nto set direction",
                 font=("Arial", 8), foreground="gray", justify=tk.LEFT).pack(pady=2)
        
        # Action buttons
        button_frame = ttk.Frame(self.editor_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Apply Changes", 
                  command=self.apply_changes).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="Delete Body", 
                  command=self.delete_body).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
    
    def show(self):
        """Show the editor panel."""
        # Force pack with all parameters to ensure consistent positioning
        self.frame.pack_forget()  # Remove first to reset position
        self.frame.pack(side=tk.LEFT, fill=tk.Y, expand=False, anchor=tk.NW, padx=5, pady=5, before=self.parent.winfo_children()[1] if len(self.parent.winfo_children()) > 1 else None)
    
    def hide(self):
        """Hide the editor panel."""
        self.frame.pack_forget()
    
    def set_body(self, body: Optional[CelestialBody]):
        """Set the body to edit."""
        self.current_body = body
        
        if body is None:
            self.no_selection_label.pack(pady=20)
            self.editor_frame.pack_forget()
        else:
            self.no_selection_label.pack_forget()
            self.editor_frame.pack(fill=tk.BOTH, expand=True)
            self.update_display()
    
    def update_display(self):
        """Update displayed values from current body."""
        if self.current_body is None:
            return
        
        # Update name
        self.name_var.set(self.current_body.name)
        
        # Update mass
        self.mass_var.set(f"{self.current_body.get_mass():.3e}")
        
        # Update position
        x, y = self.current_body.get_position()
        self.pos_label.config(text=f"x: {x:.3e} m\ny: {y:.3e} m")
        
        # Update velocity
        vx, vy = self.current_body.get_velocity()
        self.vel_label.config(text=f"vx: {vx:.2e} m/s\nvy: {vy:.2e} m/s")
        
        # Update velocity magnitude
        magnitude = (vx**2 + vy**2)**0.5
        self.velocity_magnitude_var.set(f"{magnitude:.2f}")
    
    def apply_changes(self):
        """Apply changes to the current body."""
        if self.current_body is None:
            return
        
        try:
            # Update name
            self.current_body.name = self.name_var.get()
            
            # Update mass
            mass_str = self.mass_var.get()
            mass = float(mass_str)
            if mass <= 0:
                raise ValueError("Mass must be positive")
            self.current_body.set_mass(mass)
            
            if self.on_body_updated:
                self.on_body_updated()
                
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error: {e}")
    
    def set_mass_preset(self, mass: float):
        """Set mass to a preset value."""
        self.mass_var.set(f"{mass:.3e}")
        self.apply_changes()
    
    def toggle_auto_orbit(self):
        """Toggle auto-orbit mode."""
        self.auto_orbit_enabled = self.auto_orbit_var.get()
        
        if self.auto_orbit_enabled:
            self.auto_orbit_frame.pack(fill=tk.X, pady=5)
            self.manual_vel_frame.pack_forget()
        else:
            self.auto_orbit_frame.pack_forget()
            self.manual_vel_frame.pack(fill=tk.X, pady=5)
            self.auto_orbit_target = None
            self.orbit_target_label.config(text="No target selected", foreground="gray")
    
    def start_orbit_selection(self):
        """Start selecting an orbit target."""
        self.is_selecting_orbit_target = True
        self.orbit_target_label.config(text="Click a body on canvas...", foreground="orange")
        messagebox.showinfo("Select Target", 
                          "Click on another body in the canvas to set it as the orbit target.\n\n" +
                          "The selected body will orbit around the clicked body.")
    
    def set_orbit_target(self, target: CelestialBody):
        """Set the orbit target body."""
        if target == self.current_body:
            messagebox.showwarning("Invalid Target", "Cannot orbit itself!")
            self.is_selecting_orbit_target = False
            self.orbit_target_label.config(text="No target selected", foreground="gray")
            return
        
        self.auto_orbit_target = target
        self.is_selecting_orbit_target = False
        self.orbit_target_label.config(text=f"Target: {target.name}", foreground="blue")
    
    def apply_auto_orbit(self):
        """Apply automatic orbital velocity."""
        if self.current_body is None or self.auto_orbit_target is None:
            messagebox.showwarning("No Target", "Please select an orbit target first.")
            return
        
        try:
            # Calculate orbital velocity
            central_pos = self.auto_orbit_target.get_position()
            orbiting_pos = self.current_body.get_position()
            central_mass = self.auto_orbit_target.get_mass()
            orbiting_mass = self.current_body.get_mass()
            clockwise = self.orbit_clockwise_var.get()
            
            vx, vy = calculate_orbital_velocity_vector(
                central_pos, orbiting_pos, 
                central_mass, orbiting_mass, 
                G, clockwise
            )
            
            self.current_body.set_velocity(vx, vy)
            self.update_display()
            
            if self.on_body_updated:
                self.on_body_updated()
            
            messagebox.showinfo("Success", 
                              f"Orbital velocity applied: {(vx**2 + vy**2)**0.5:.2f} m/s")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate orbit: {e}")
    
    def toggle_velocity_arrow(self):
        """Toggle velocity arrow creation mode."""
        if self.current_body is None:
            return
        
        self.current_body.is_setting_velocity = not self.current_body.is_setting_velocity
        
        if self.current_body.is_setting_velocity:
            self.current_body.velocity_arrow_start = self.current_body.get_position()
            self.create_velocity_button.config(text="✓ Editing Arrow (drag on canvas)")
            messagebox.showinfo("Velocity Arrow Mode", 
                              "Now click and drag on the canvas to set velocity direction.\n" +
                              "The arrow will show the direction.\n" +
                              "Enter speed in the text box and click 'Apply Speed'.")
        else:
            self.create_velocity_button.config(text="Create/Edit Velocity Arrow")
        
        if self.on_body_updated:
            self.on_body_updated()
    
    def apply_velocity_magnitude(self):
        """Apply the velocity magnitude from the text input."""
        if self.current_body is None:
            return
        
        try:
            magnitude = float(self.velocity_magnitude_var.get())
            if magnitude < 0:
                raise ValueError("Speed must be non-negative")
            
            # Get current velocity to extract direction
            vx, vy = self.current_body.get_velocity()
            current_mag = (vx**2 + vy**2)**0.5
            
            if current_mag == 0:
                # No direction set, warn user
                messagebox.showwarning("No Direction", 
                                     "Please create a velocity arrow first to set the direction.")
                return
            
            # Scale to new magnitude
            scale = magnitude / current_mag
            new_vx = vx * scale
            new_vy = vy * scale
            
            self.current_body.set_velocity(new_vx, new_vy)
            self.update_display()
            
            if self.on_body_updated:
                self.on_body_updated()
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error: {e}")
    
    def start_velocity_setting(self):
        """Start manual velocity setting with mouse (deprecated - use toggle_velocity_arrow)."""
        self.toggle_velocity_arrow()
    
    def delete_body(self):
        """Delete the current body."""
        if self.current_body is None:
            return
        
        result = messagebox.askyesno("Delete Body", 
                                    f"Delete {self.current_body.name}?")
        if result:
            self.state.remove_body(self.current_body)
            self.set_body(None)
            
            if self.on_body_updated:
                self.on_body_updated()
