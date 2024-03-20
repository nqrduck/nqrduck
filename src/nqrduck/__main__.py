import sys
import traceback
import os
import logging
import logging.handlers
import  tempfile
from PyQt6.QtWidgets import QApplication, QMessageBox   
from .core.main_model import MainModel
from .core.main_controller import MainController
from .core.main_view import MainView, SplashScreen

logger = logging.getLogger(__name__)

class NQRduck(QApplication):

    def __init__(self, sys_argv):
        super(NQRduck, self).__init__(sys_argv)

        self._main_model = MainModel()
        self._main_controller = MainController(self._main_model)
        self._main_view = MainView(self._main_model, self._main_controller)

        # Wait for the splash screen to close before starting the rest of the application
        self.processEvents()

        # Here the modules are loaded and signals connected
        self._main_controller.load_modules(self._main_view)
        # Get the first loaded module and set it as active
        self._main_model.active_module = self._main_model.loaded_modules[list(self._main_model.loaded_modules.keys())[0]]

        self._main_view.setWindowTitle("NQRduck")
        self._main_view.showMaximized()

def handle_exception(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions."""
    logger.exception("An unhandled exception occurred: ", exc_info=(exc_type, exc_value, exc_traceback))
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    QMessageBox.critical(None, "Error", "An unhandled exception occurred:\n" + error_msg)
        
    sys.exit(1)

def main():
    # Install the exception handler
    sys.excepthook = handle_exception  

    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    # Stop matplotlib from spamming the DEBUG log level
    logging.getLogger('matplotlib').setLevel(logging.WARNING)

    # Output log to log file to temp folder
    temp_folder = tempfile.gettempdir()
    # Rotate log files
    fh = logging.handlers.RotatingFileHandler(os.path.join(temp_folder, 'nqrduck.log'), maxBytes=1000000, backupCount=5)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    fh.doRollover()
    logger.addHandler(fh)


    logger.debug("Starting QApplication ...")
    
    application = NQRduck(sys.argv)
        
    exit_code = application.exec()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
