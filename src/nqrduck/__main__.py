import sys
import logging
import logging
from PyQt6.QtWidgets import QApplication
from .core.main_model import MainModel
from .core.main_controller import MainController
from .core.main_view import MainView, SplashScreen

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

        screen = self.primaryScreen()
        size = screen.size()
        self._main_view.setWindowTitle("NQRduck")
        self._main_view.resize(size.width(), size.height())
        self._main_view.show()


def main():
    # create logger
    logger = logging.getLogger('root')
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

    logger.debug("Starting QApplication ...")
    
    application = NQRduck(sys.argv)
    
    sys.exit(application.exec())

if __name__ == '__main__':
    main()
