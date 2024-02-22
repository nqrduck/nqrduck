# NQRduck 

## Installation
### Requirements
- Python 3.6+
- pip
- virtualenv

### Setup
1. Clone the repository
2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. Install the package with `pip install .[all]` to install all available NQRduck modules. This should install all other dependencies as well.
4. Run the program with `nqrduck`.

## Usage
Individual features of the software can be installed as separate Python packages, like spectrometer control, pulse sequence programming or simulation of magnetic resonance experiments. The available functionality of the NQRduck program therefore depends on the installed packages.

The UI is structured as follows:

<img src="docs/img/ui_structure_v2.png" alt="drawing" width="800">

The UI is separated into different areas. Section 'a', highlighted in red, represents the menu bar used for general settings of the program and spectrometer selection. Section 'b', outlined in green, allows switching among various modules within the main view of the core, with the active module displayed in bold. Section 'c', depicted in blue, is the active module's view. The currently active module in the figure is the [nqrduck-measurement](https://github.com/nqrduck/nqrduck-measurement) module used for single frequency mangetic resonance experiments. The overall application is part of the NQRduck core and opens when the NQRduck core is started. 

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


## Contributing: Developing NQRduck modules
A template module is provided [here](https://github.com/nqrduck/nqrduck-module). It is a good starting point for developing new modules.