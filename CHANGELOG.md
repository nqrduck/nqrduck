# Changelog

## Version 0.0.11 (27-05-2024)

- Implemented additional customization for function selection form field (`b7fd4558a3083f6a8fbcceaa194c1696564baf7e`).

## Version 0.0.10 (18-05-2024)

- Implemented setting for darkmode in the GUI (`f5445f13ed58684987c5b81967838b5423d43683`).
- Added a on_settings_changed slot to the modules that is called when the settings are changed. This enables the different modules to react to changes in the settings. Right now the primary use is to update the Plots with the new color schemes (`8810c9837b82269f77bf7f1c88a2012c98645520`).
- When changing the settings, the appearance of the GUI is not updated immediately. Instead the user first needs to apply the changes. Then a countdown start where the user can revert the changes. If the user does not revert the changes, the new settings are applied (`00c93da4b95cb508b8a03ab760202849a5224eb1`).
- The splash screen now works with wayland (`8f5d8310e20f8ac031ca9211a555bccb06269903`).
- Automatic desktop file creation for the GUI - this also fixes the window icon with wayland. Added startup arguments for version, uninstall and log level (`2e5d0782e73fd10b6a525516a32758cdf83d4d40`).

## Version 0.0.9 (05-05-2024)

- On startup of the GUI, the first module from the module order is automatically displayed (`84b9e98406e12abf35fd1ceb75d72f56e5447ac4`)
- The QFileManager was renamed to FileManager since its not a PyQt class. Additionally there  is now an optional caption parameter for the file dialog (`9fc220acef1e8df8ba040be4a37746a7425928b0`)

## Version 0.0.8 (01-05-2024)

- Added install wizard for the different NQRduck modules

## Version 0.0.7 (26-04-2024)

- Implemented Formbuilder for the GUI which can be used to create easy input fields for the user

## Version 0.0.6 (23-04-2024)

- Fixed bug with platform dependency in the pyproject.toml file

## Version 0.0.5 (23-04-2024)

- All modules are now available on PyPI
- Added the  optional dependency "lime" to the pyproject.toml file allowing for control of the LimeSDR-based spectrometer
- Some linting and updating of name to the pyproject.toml file and README.md

## Version 0.0.4 (17-04-2024)

- Automatic deployment to PyPI using GitHub Actions

## Version 0.0.3 (15-04-2024)

- Initial release
