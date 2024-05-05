# Changelog
## Version 0.0.9 (05-05-2024)
- On startup of the GUI, the first module from the module order is automatically displayed (`84b9e98406e12abf35fd1ceb75d72f56e5447ac4`)
- The QFileManager was renamed to FileManager since its not a PyQt class. Additionally there  is now an optional caption parameter for the file dialog (`9fc220acef1e8df8ba040be4a37746a7425928b0`)

### Version 0.0.8 (01-05-2024)
- Added install wizard for the different NQRduck modules

### Version 0.0.7 (26-04-2024)
- Implemented Formbuilder for the GUI which can be used to create easy input fields for the user

### Version 0.0.6 (23-04-2024)
- Fixed bug with platform dependency in the pyproject.toml file

### Version 0.0.5 (23-04-2024)
- All modules are now available on PyPI
- Added the  optional dependency "lime" to the pyproject.toml file allowing for control of the LimeSDR-based spectrometer
- Some linting and updating of name to the pyproject.toml file and README.md

### Version 0.0.4 (17-04-2024)
- Automatic deployment to PyPI using GitHub Actions
### Version 0.0.3 (15-04-2024)
- Initial release