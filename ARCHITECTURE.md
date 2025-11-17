# N-Body GUI Architecture Overview

## Component Hierarchy

```
main.py
   ↓
NBodyApp (gui/app.py)
   ├── SimulationState (shared state)
   ├── ControlPanel (top bar)
   ├── BodyEditorPanel (left sidebar)
   └── SimulationCanvas (main canvas)
```

## Class Responsibilities

### Models (`models/`)

**CelestialBody**
- Wraps nbody.Body with metadata
- Stores: name, color, selection state, velocity setting state
- Provides: position/velocity getters/setters, mass management
- Handles: reset to initial conditions

**SimulationState**
- Central coordinator for simulation
- Manages: body collection, trajectories, mode switching
- Owns: nbody.Kosmos instance (in simulation mode)
- Tracks: time, running state, time warp multiplier

**SimulationMode (enum)**
- GOD_MODE: editing/setup
- SIMULATION_MODE: running physics

### GUI Components (`gui/`)

**NBodyApp** (main orchestrator)
- Creates and owns all GUI components
- Wires callbacks between components
- Runs animation loop (30 FPS target)
- Handles mode transitions

**SimulationCanvas**
- Matplotlib FigureCanvas wrapper
- Renders bodies and trajectories
- Handles mouse events (click, move)
- Manages zoom/pan
- Draws velocity arrows
- Callbacks: on_body_selected

**ControlPanel**
- Top control bar with mode indicator
- Start/Pause/Stop buttons
- Time warp selector (dropdown)
- Time display
- View controls (zoom buttons)
- Callbacks: on_mode_change, on_clear_all

**BodyEditorPanel**
- Left sidebar (visible only in God Mode)
- Edits body properties:
  * Name (text entry)
  * Mass (with presets: Earth, Jupiter, Sun)
  * Position (read-only display)
  * Velocity (auto-orbit OR manual)
- Auto-orbit mode:
  * Target selection
  * Clockwise/counter-clockwise
  * Automatic velocity calculation
- Manual velocity mode:
  * Mouse direction setting
  * Speed input
- Delete body button
- Callbacks: on_body_updated

### Utilities (`utils/`)

**physics.py**
- calculate_orbital_velocity(central_mass, orbiting_mass, distance)
- calculate_orbital_velocity_vector(positions, masses, clockwise)
- calculate_escape_velocity(mass, distance)
- Vector utilities (magnitude, normalize, distance)

**constants.py**
- G (gravitational constant)
- AU (astronomical unit)
- Standard masses (SOLAR_MASS, EARTH_MASS, JUPITER_MASS)
- Standard radii (for future use)

### Configuration (`config/`)

**presets.py**
- ScenarioPresets class with factory methods:
  * three_body_choreography()
  * sun_earth_moon()
  * binary_stars()
  * planetary_system()
  * chaotic_three_body()
- COLOR_PALETTE (list of hex colors)
- DEFAULT_TIME_STEP, DEFAULT_ZOOM

## Event Flow

### God Mode - Adding a Body

```
User clicks canvas
   ↓
SimulationCanvas.on_mouse_click()
   ↓
SimulationCanvas.add_new_body_at_position()
   ↓
Create CelestialBody, add to SimulationState
   ↓
SimulationCanvas.on_body_selected() callback
   ↓
BodyEditorPanel.set_body()
   ↓
Canvas renders
```

### God Mode - Auto-Orbit Setup

```
User checks "Auto Orbit" in BodyEditorPanel
   ↓
User clicks "Select Target"
   ↓
User clicks another body on canvas
   ↓
BodyEditorPanel.set_orbit_target()
   ↓
User clicks "Apply Orbit"
   ↓
calculate_orbital_velocity_vector() in physics.py
   ↓
Body velocity updated
   ↓
Canvas renders velocity arrow
```

### Mode Transition - God → Simulation

```
User clicks "Start Simulation"
   ↓
ControlPanel.toggle_mode()
   ↓
SimulationState.switch_to_simulation_mode()
   ↓
Creates nbody.Kosmos with all bodies
   ↓
Initialize trajectories
   ↓
ControlPanel.on_mode_change() callback
   ↓
NBodyApp.on_mode_change()
   ↓
Hide BodyEditorPanel
Update window title
Enable playback controls
```

### Simulation Mode - Running

```
Animation loop (33ms interval)
   ↓
Check if running and in simulation mode
   ↓
Calculate steps based on time_warp
   ↓
For each step:
   SimulationState.step_simulation()
      ↓
   nbody.Kosmos.step(time_step)
      ↓
   Update body positions from Kosmos
   Store position in trajectory
   ↓
SimulationCanvas.render()
   ↓
ControlPanel.update_time_display()
   ↓
Schedule next frame
```

### Mode Transition - Simulation → God

```
User clicks "Stop"
   ↓
ControlPanel.stop_simulation()
   ↓
SimulationState.switch_to_god_mode()
   ↓
Reset all bodies to initial conditions
Clear trajectories
Destroy Kosmos
   ↓
ControlPanel.on_mode_change() callback
   ↓
NBodyApp.on_mode_change()
   ↓
Show BodyEditorPanel
Update window title
Disable playback controls
```

## Key Design Patterns

### 1. Separation of Concerns
- **Models**: Pure data and state logic
- **GUI**: Presentation and user interaction
- **Utils**: Reusable calculations

### 2. Observer Pattern (via callbacks)
- GUI components notify each other through callbacks
- Loose coupling between components

### 3. State Pattern
- SimulationMode enum defines behavior
- Components react differently based on mode

### 4. Facade Pattern
- NBodyApp provides simple interface to complex system
- Hides inter-component wiring

### 5. Factory Pattern
- ScenarioPresets creates pre-configured body sets

## Thread Safety

- Single-threaded design (tkinter main loop)
- Animation loop uses tkinter's after() for scheduling
- No concurrent access to SimulationState

## Performance Considerations

1. **Animation Loop**: Targets 30 FPS (33ms per frame)
2. **Time Warp**: Multiplies steps per frame (clamped to 1-1000)
3. **Trajectory Storage**: Stores all positions (could be optimized)
4. **Rendering**: Full re-render each frame (matplotlib limitation)

## Extension Guidelines

### Adding a New Feature

1. **Data Changes**: Update models/
2. **UI Changes**: Update gui/ components
3. **Physics**: Add to utils/physics.py
4. **Wire Together**: Update callbacks in NBodyApp
5. **Document**: Update README.md

### Adding a New Preset

1. Add method to config/presets.py ScenarioPresets
2. Return list of CelestialBody instances
3. (Future) Add UI button to load preset
