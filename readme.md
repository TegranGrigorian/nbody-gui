# NBody GUI

This project provides a GUI for simulating and visualizing n-body gravitational interactions using Python's Tkinter library. It includes features such as body editing, preset configurations, and camera controls.

## Features
* Interactive canvas for visualizing celestial bodies
* Control panel for simulation settings
* Body editor for adding and modifying celestial bodies
* Preset menu for loading predefined simulations
* Camera controls for zooming and panning

## Dependencies
- Python 3.x
- required libraries (e.g., Tkinter, NumPy)
    * install nbody module!
        * `https://github.com/TegranGrigorian/n-body-simulator`

## Installation
1. Clone the repository:

   ```shell
   git clone https://github.com/TegranGrigorian/nbody-gui
   ```
1. Install nbody module from its repository:

   ```shell
   git clone https://github.com/TegranGrigorian/n-body-simulator
   ```
   * Your directory should look like this
   ```shell
    .
    ├── nbody-gui
    ├───── * Some files
    └── n-body-simulator
        ├── pyproject.toml
        ├── README.md
        ├── requirements.txt
        └── setup.py
   ```
1. Navigate to the GUI project directory:

   ```shell
    cd nbody-gui
    ```

1. Create virtual environment (optional but recommended):

    ```shell
    virtualenv .venv --python=python3
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

1. Install required dependencies:
    ```shell
    pip install -r requirements.txt
    ```

    * Install the nbody module using pip command
    ```shell
    pip install -e ../n-body-simulator
    ```
    * **NOTE:** This is assuming that your directory looks like the one shown above. If its different, change the file path `../n-body-simulator` accordingly.
1. Run the application:
    ```shell
    python main.py
    ```

## Usage
* Use the control panel to start, pause, and reset the simulation.
* Edit celestial bodies using the body editor panel.
* Load different presets from the preset menu.

## Project Structure

### File Synopsis'
* `main.py`: Entry point of the application.
* `gui/`: Contains all GUI-related components.
* `models/`: Contains data models for celestial bodies and simulation state.
* `config/`: Contains configuration files and presets.
* `utils/`: Contains utility functions and constants.

### Tree Structure
```
nbody-gui/
├── config
│   ├── __init__.py
│   └── presets.py
├── gui
│   ├── app.py
│   ├── body_editor.py
│   ├── canvas.py
│   ├── control_panel.py
│   ├── __init__.py
│   └── preset_menu.py
├── main.py
├── models
│   ├── body.py
│   ├── __init__.py
│   └── simulation_state.py
├── readme.md
├── requirements.txt
└── utils
    ├── constants.py
    ├── __init__.py
    └── physics.py
```

## Final Notes
Thank you for downloading and using the NBody GUI application! I started this project after finishing the book "Three-Body Problem" by Cixin Liu. I wanted to visualize the chaotic life of the Trisolarans. If you encounter any issues or have suggestions for improvements, please feel free to open an issue on the GitHub repository.