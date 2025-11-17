"""GUI components package."""

from .canvas import SimulationCanvas
from .control_panel import ControlPanel
from .body_editor import BodyEditorPanel
from .app import NBodyApp

__all__ = ['SimulationCanvas', 'ControlPanel', 'BodyEditorPanel', 'NBodyApp']
