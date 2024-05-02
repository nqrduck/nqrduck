"""Main entry point for the NQRduck application."""

import sys
import traceback
import os
import logging
import logging.handlers
import tempfile
from PyQt6.QtWidgets import QApplication, QMessageBox
from .core.main_model import MainModel
from .core.main_controller import MainController
from .core.main_view import MainView
from .core.install_wizard import DuckWizard

logger = logging.getLogger(__name__)


class NQRduck(QApplication):
    """Main application for the NQRduck.

    Args:
        sys_argv (list): The system arguments
    """

    def __init__(self, sys_argv):
        """Initializes the NQRduck application."""
        super().__init__(sys_argv)

        self._main_model = MainModel()
        self._main_controller = MainController(self._main_model)
        self._main_view = MainView(self._main_model, self._main_controller)

        # Wait for the splash screen to close before starting the rest of the application
        self.processEvents()

        # Here the modules are loaded and signals connected
        self._main_controller.load_modules(self._main_view)
        
        # Start the wizard if no modules could be loaded
        if not self._main_model.loaded_modules:
            logger.warning("No modules loaded")
            # Start the install wizard if no modules are loaded
            self._main_view.install_wizard = DuckWizard(
                [], self._main_view
            )
            self._main_view.install_wizard.show()
            self._main_view.install_wizard.exec()

        self._main_view.setWindowTitle("NQRduck")
        self._main_view.showMaximized()

        self._main_view.on_settings_changed()


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
    # Install the exception handler
    sys.excepthook = handle_exception

    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

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

    logger.debug("Starting QApplication ...")

    application = NQRduck(sys.argv)

    exit_code = application.exec()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
