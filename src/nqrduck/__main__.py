"""Main entry point for the NQRduck application."""

import sys
import traceback
import os
import logging
import logging.handlers
import tempfile
import argparse
import importlib.metadata
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from .core.main_model import MainModel
from .core.main_controller import MainController
from .core.main_view import MainView
from .core.install_wizard import DuckWizard
from .core.splash_screen import SplashScreen

logger = logging.getLogger(__name__)


class NQRduck(QApplication):
    """Main application for the NQRduck.

    Args:
        sys_argv (list): The system arguments
    """

    def __init__(self, sys_argv):
        """Initializes the NQRduck application."""
        super().__init__(sys_argv)

        self.setApplicationName("NQRduck")
        self.setOrganizationName("NQRduck")
        self.setOrganizationDomain("nqrduck.cool")

        self.setDesktopFileName("nqrduck")

        self.splash_screen = SplashScreen()

        # Process events to show the splash screen
        self.processEvents()

        self._main_model = MainModel()
        self.setWindowIcon(self._main_model.logo)
        self._main_controller = MainController(self._main_model)
        self._main_view = MainView(self._main_model, self._main_controller)

        # The splash screen is only shown if start application is called with a QTimer (?)
        QTimer.singleShot(1000, self.start_application)

    def start_application(self):
        """Start the application."""
        # Here the modules are loaded and signals connected
        self._main_controller.load_modules(self._main_view)

        # Start the wizard if no modules could be loaded
        if not self._main_model.loaded_modules:
            logger.warning("No modules loaded")
            # Start the install wizard if no modules are loaded
            self._main_view.install_wizard = DuckWizard([], self._main_view)
            self._main_view.install_wizard.show()
            self._main_view.install_wizard.exec()

        self._main_view.setWindowTitle("NQRduck")
        self._main_view.showMaximized()

        self._main_view.on_settings_changed()

        self.splash_screen.close()


def create_desktop_file():
    """Create the desktop file for NQRduck."""
    # We check if we are on a linux system via the home directory
    home = Path.home()
    if Path(home, ".local", "share", "applications").exists():

        desktop_file = Path(home, ".local", "share", "applications", "nqrduck.desktop")

        version = importlib.metadata.version("nqrduck")
        exectuable = Path(sys.executable).parent / "nqrduck"
        icon = Path(__file__).parent / "assets" / "logos" / "LabMallardnbg_32x32.png"

        DESKTOP_FILE_CONTENT = f"""
        [Desktop Entry]
        Version={version}
        Name=NQRduck
        Comment= A toolbox for educational magnetic resonance experiments
        Exec={exectuable}
        Icon={icon}
        Terminal=false
        Type=Application
        Categories=Education;Science;Physics;
        StartupNotify=true
        """

        try:
            with open(desktop_file, "w") as f:
                f.write(DESKTOP_FILE_CONTENT)
        
        except OSError as e:
            logger.error(f"Could not create desktop file: {e}")

def uninstall():
    """Remove the desktop file for NQRduck."""
    home = Path.home()
    desktop_file = Path(home, ".local", "share", "applications", "nqrduck.desktop")

    if desktop_file.exists():
        try:
            desktop_file.unlink()
        except OSError as e:
            logger.error(f"Could not remove desktop file: {e}")


def handle_exception(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions.

    Args:
        exc_type (type): The type of the exception
        exc_value (Exception): The exception object
        exc_traceback (traceback): The traceback object
    """
    logger.exception(
        "An unhandled exception occurred: ",
        exc_info=(exc_type, exc_value, exc_traceback),
    )
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    QMessageBox.critical(
        None, "Error", "An unhandled exception occurred:\n" + error_msg
    )

    sys.exit(1)


def main():
    """Main entry point for the NQRduck application."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="NQRduck")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall NQRduck")
    version = importlib.metadata.version("nqrduck")
    parser.add_argument("--version", action="version", version=version)
    # TODO: In future, versions this should probably be set to INFO
    parser.add_argument("--log-level", default="DEBUG", help="Set the log level")
    args = parser.parse_args()

    # Install the exception handler
    sys.excepthook = handle_exception

    # create logger
    logger = logging.getLogger()
    try:
        log_level = getattr(logging, args.log_level)
    except AttributeError:
        log_level = logging.DEBUG
    
    logger.setLevel(log_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    # Stop matplotlib from spamming the DEBUG log level
    logging.getLogger("matplotlib").setLevel(logging.WARNING)

    # Output log to log file to temp folder
    temp_folder = tempfile.gettempdir()
    # Rotate log files
    fh = logging.handlers.RotatingFileHandler(
        os.path.join(temp_folder, "nqrduck.log"), maxBytes=1000000, backupCount=5
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    fh.doRollover()
    logger.addHandler(fh)

    if args.uninstall:
        uninstall()
        sys.exit(0)

    # Create the desktop file
    create_desktop_file()

    logger.debug("Starting QApplication ...")

    application = NQRduck(sys.argv)

    exit_code = application.exec()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
