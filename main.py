"""
N-Body Simulation GUI

An interactive GUI for simulating gravitational N-body systems.

Features:
- God Mode: Create and configure celestial bodies
- Simulation Mode: Run physics simulations with time warp
- Auto-orbit calculations
- Manual velocity setting with visual feedback
"""

import tkinter as tk
from gui import NBodyApp


def main():
    """Main entry point for the N-Body simulation application."""
    root = tk.Tk()
    app = NBodyApp(root)
    app.run()


if __name__ == "__main__":
    main()
