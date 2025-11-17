"""Control panel for mode switching and simulation controls."""

import tkinter as tk
from tkinter import ttk

from models import SimulationState
from models.simulation_state import SimulationMode


class ControlPanel:
    """Control panel for switching modes and controlling simulation."""
    
    def __init__(self, parent, simulation_state: SimulationState):
        """
        Initialize control panel.
        
        Args:
            parent: Parent tkinter widget
            simulation_state: Shared simulation state
        """
        self.parent = parent
        self.state = simulation_state
        
        # Callbacks
        self.on_mode_change = None
        self.on_clear_all = None
        
        # Create frame
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(side=tk.TOP, fill=tk.X)
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create control widgets."""
        # Title
        title_frame = ttk.Frame(self.frame)
        title_frame.pack(side=tk.LEFT, padx=10)
        
        title = ttk.Label(title_frame, text="N-Body Simulator", 
                         font=("Arial", 16, "bold"))
        title.pack()
        
        # Mode indicator
        self.mode_label = ttk.Label(title_frame, text="MODE: GOD MODE", 
                                    font=("Arial", 11), foreground="green")
        self.mode_label.pack()
        
        # Separator
        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # God Mode controls
        god_frame = ttk.LabelFrame(self.frame, text="God Mode", padding="5")
        god_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(god_frame, text="Click canvas to add bodies").pack()
        ttk.Label(god_frame, text="Click body to select & edit").pack()
        
        self.clear_button = ttk.Button(god_frame, text="Clear All", command=self.clear_all)
        self.clear_button.pack(pady=5)
        
        # Simulation controls
        sim_frame = ttk.LabelFrame(self.frame, text="Simulation", padding="5")
        sim_frame.pack(side=tk.LEFT, padx=5)
        
        self.start_button = ttk.Button(sim_frame, text="▶ Start Simulation", 
                                      command=self.toggle_mode, width=18)
        self.start_button.pack(pady=2)
        
        self.play_pause_button = ttk.Button(sim_frame, text="⏸ Pause", 
                                           command=self.toggle_play_pause,
                                           state=tk.DISABLED, width=18)
        self.play_pause_button.pack(pady=2)
        
        self.stop_button = ttk.Button(sim_frame, text="⏹ Stop & Return to God Mode", 
                                     command=self.stop_simulation,
                                     state=tk.DISABLED, width=18)
        self.stop_button.pack(pady=2)
        
        # Time display
        time_frame = ttk.LabelFrame(self.frame, text="Time", padding="5")
        time_frame.pack(side=tk.LEFT, padx=5)
        
        self.time_label = ttk.Label(time_frame, text="0.00 hours", 
                                    font=("Arial", 12, "bold"))
        self.time_label.pack()
        
        # Time warp control
        warp_frame = ttk.Frame(time_frame)
        warp_frame.pack(pady=5)
        
        ttk.Label(warp_frame, text="Time Warp:").pack(side=tk.LEFT, padx=2)
        
        self.warp_var = tk.DoubleVar(value=1.0)
        self.warp_options = [0.1, 0.5, 1, 2, 5, 10, 50, 100, 1000]
        self.warp_combo = ttk.Combobox(warp_frame, textvariable=self.warp_var,
                                      values=self.warp_options, width=8, state='readonly')
        self.warp_combo.current(2)  # Start at 1x
        self.warp_combo.pack(side=tk.LEFT, padx=2)
        self.warp_combo.bind('<<ComboboxSelected>>', self.on_warp_change)
        
        ttk.Label(warp_frame, text="x").pack(side=tk.LEFT)
        
        # View controls
        view_frame = ttk.LabelFrame(self.frame, text="View", padding="5")
        view_frame.pack(side=tk.LEFT, padx=5)
        
        button_row1 = ttk.Frame(view_frame)
        button_row1.pack(pady=2)
        
        self.zoom_in_button = ttk.Button(button_row1, text="🔍+", width=5,
                                        command=self.on_zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=2)
        
        self.zoom_out_button = ttk.Button(button_row1, text="🔍-", width=5,
                                         command=self.on_zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=2)
        
        self.reset_view_button = ttk.Button(button_row1, text="Reset", width=5,
                                           command=self.on_reset_view)
        self.reset_view_button.pack(side=tk.LEFT, padx=2)
        
        button_row2 = ttk.Frame(view_frame)
        button_row2.pack(pady=2)
        
        self.auto_cog_button = ttk.Button(button_row2, text="Auto CoG", width=12,
                                         command=self.toggle_auto_cog)
        self.auto_cog_button.pack(side=tk.LEFT, padx=2)
        
        self.capture_all_button = ttk.Button(button_row2, text="Capture All", width=12,
                                            command=self.toggle_capture_all)
        self.capture_all_button.pack(side=tk.LEFT, padx=2)
        
    def toggle_mode(self):
        """Toggle between God Mode and Simulation Mode."""
        if self.state.mode == SimulationMode.GOD_MODE:
            # Check if there are bodies to simulate
            if len(self.state.bodies) == 0:
                return
            
            # Switch to simulation mode
            self.state.switch_to_simulation_mode()
            self.state.is_running = True
            
            # Update UI
            self.mode_label.config(text="MODE: SIMULATION", foreground="blue")
            self.start_button.config(state=tk.DISABLED)
            self.play_pause_button.config(state=tk.NORMAL, text="⏸ Pause")
            self.stop_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.DISABLED)
            
            if self.on_mode_change:
                self.on_mode_change()
    
    def toggle_play_pause(self):
        """Toggle play/pause in simulation mode."""
        self.state.is_running = not self.state.is_running
        
        if self.state.is_running:
            self.play_pause_button.config(text="⏸ Pause")
        else:
            self.play_pause_button.config(text="▶ Play")
    
    def stop_simulation(self):
        """Stop simulation and return to God Mode."""
        self.state.switch_to_god_mode()
        
        # Update UI
        self.mode_label.config(text="MODE: GOD MODE", foreground="green")
        self.start_button.config(state=tk.NORMAL)
        self.play_pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.NORMAL)
        self.time_label.config(text="0.00 hours")
        
        if self.on_mode_change:
            self.on_mode_change()
    
    def clear_all(self):
        """Clear all bodies."""
        if self.on_clear_all:
            self.on_clear_all()
    
    def update_time_display(self):
        """Update the time display."""
        time_str = self.state.get_time_string()
        self.time_label.config(text=time_str)
    
    def on_warp_change(self, event=None):
        """Handle time warp change."""
        self.state.time_warp = self.warp_var.get()
    
    def on_zoom_in(self):
        """Callback for zoom in button."""
        pass  # Will be connected by main app
    
    def on_zoom_out(self):
        """Callback for zoom out button."""
        pass  # Will be connected by main app
    
    def on_reset_view(self):
        """Callback for reset view button."""
        pass  # Will be connected by main app
    
    def toggle_auto_cog(self):
        """Callback for auto CoG button."""
        pass  # Will be connected by main app
    
    def toggle_capture_all(self):
        """Callback for capture all button."""
        pass  # Will be connected by main app
