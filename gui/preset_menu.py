"""Preset menu for loading example configurations."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class PresetMenu:
    """Hamburger menu for preset configurations."""
    
    def __init__(self, parent):
        """
        Initialize preset menu.
        
        Args:
            parent: Parent tkinter widget
        """
        self.parent = parent
        self.is_open = False
        self.on_preset_selected: Optional[Callable[[str], None]] = None
        
        # Create hamburger button
        self.hamburger_button = ttk.Button(parent, text="☰ Presets", 
                                          command=self.toggle_menu, width=10)
        self.hamburger_button.pack(side=tk.LEFT, padx=5)
        
        # Create menu frame (initially hidden)
        self.menu_frame = ttk.Frame(parent, relief=tk.RAISED, borderwidth=2)
        self.menu_frame.pack_forget()
        
        self.create_menu_items()
    
    def create_menu_items(self):
        """Create menu items."""
        title = ttk.Label(self.menu_frame, text="Load Preset Configuration", 
                         font=("Arial", 11, "bold"))
        title.pack(pady=5, padx=10)
        
        ttk.Separator(self.menu_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        # Preset buttons
        presets = [
            ("Solar System", "solar_system", "Sun, 8 planets, and Earth's moon"),
            ("Earth & Moon", "earth_moon", "Earth-Moon system orbiting the Sun"),
            ("Jupiter & Moons", "jupiter_moons", "Jupiter with its 4 Galilean moons"),
            ("Three-Body Problem", "three_body_problem", "3 suns with a planet (Liu Cixin inspired)"),
            ("Alpha Centauri", "alpha_centauri", "Triple star system"),
            ("Binary Stars", "binary_stars", "Two stars orbiting each other"),
            ("Figure-8 Orbit", "figure_8", "Stable three-body choreography"),
        ]
        
        for name, preset_id, description in presets:
            btn_frame = ttk.Frame(self.menu_frame)
            btn_frame.pack(fill=tk.X, padx=5, pady=2)
            
            btn = ttk.Button(btn_frame, text=name, 
                           command=lambda p=preset_id: self.select_preset(p),
                           width=25)
            btn.pack(side=tk.LEFT, padx=2)
            
            desc_label = ttk.Label(btn_frame, text=description, 
                                  font=("Arial", 8), foreground="gray")
            desc_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(self.menu_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        close_btn = ttk.Button(self.menu_frame, text="Close", command=self.toggle_menu)
        close_btn.pack(pady=5)
    
    def toggle_menu(self):
        """Toggle menu visibility."""
        self.is_open = not self.is_open
        
        if self.is_open:
            self.menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5, after=self.hamburger_button)
            self.hamburger_button.config(text="✕ Close")
        else:
            self.menu_frame.pack_forget()
            self.hamburger_button.config(text="☰ Presets")
    
    def select_preset(self, preset_id: str):
        """Handle preset selection."""
        if self.on_preset_selected:
            self.on_preset_selected(preset_id)
        self.toggle_menu()  # Close menu after selection
