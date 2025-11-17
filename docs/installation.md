# Installation
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

## Example Install Video
Not one for now
<!-- One day ill add -->