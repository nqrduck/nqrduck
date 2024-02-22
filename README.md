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

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


## Contributing: Developing NQRduck modules
A template module is provided [here](https://github.com/nqrduck/nqrduck-module). It is a good starting point for developing new modules.