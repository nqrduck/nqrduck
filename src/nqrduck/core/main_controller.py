import os
import sys
import logging
import glob
import importlib
import yaml
import configparser
import subprocess
import importlib
from PyQt5.QtCore import QObject
from ..module.module import Module

logger = logging.getLogger(__name__)


class MainController(QObject):

    def __init__(self, main_model):
        super().__init__()
        self._main_model = main_model

    def load_modules(self, main_view):
        # Get a list of modules specified as active from the main_configuration.ini
        config = configparser.ConfigParser(allow_no_value=True)

        # Make config parser case sensitive
        config.optionxform = str

        config_path = os.path.join(os.getcwd(), self._main_model.DEFAULT_CONFIG)
        logger.debug("Reading config from %s", config_path)
        config.read(config_path)
        config_modules = list(zip(*config.items("MODULES")))[0]
        logger.debug("Modules found: %s", config_modules)

        # Create instances of the modules and set the main_model accordingly
        for module_name in config_modules:
            self._load_module(module_name, main_view)

    def _load_module(self, module_name, main_view):
        # Install the module via subprocess
        logger.debug("Installing module: %s", module_name)
        
        # Uncomment this again to install modules via pip - this is currently disabled for development
        # subprocess.check_call([sys.executable, "-m", "pip", "install", "nqrduck[%s]" % module_name])
        
        # Reset logging level to default
        logger.setLevel(logging.DEBUG)

        # Import the module
        logger.debug("Importing Module: %s", module_name)
        import_module = importlib.import_module(module_name.replace("-", "_"))
        logger.debug("Imported module path: %s", import_module.__path__[0])

        
        
        # Import the module
        module = getattr(import_module, "Module")

        module._model.widget_changed.connect(main_view.on_module_widget_changed)

        # Add the module to the main model object
        self._main_model.add_module(module._model.name, module)

