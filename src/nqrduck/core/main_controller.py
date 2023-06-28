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

    MODULE_CONFIG_PATH = "resources"

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
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nqrduck[%s]" % module_name])
        
        # Reset logging level to default
        logger.setLevel(logging.DEBUG)

        # Import the module
        logger.debug("Importing Module: %s", module_name)
        import_module = importlib.import_module(module_name.replace("-", "_"))
        logger.debug("Imported module path: %s", import_module.__path__[0])

        module = Module()

        # Read module config file
        config = configparser.ConfigParser(allow_no_value=True)
        # Make config parser case sensitive
        config.optionxform = str
        config_path = os.path.join(os.getcwd(), import_module.__path__[0])
        config_path = os.path.join(config_path, self.MODULE_CONFIG_PATH)
        logger.debug("Attempting to load module config file: %s", config_path)

        config_file = glob.glob(config_path + "/**/*.ini", recursive=True)

        if config_file:
            logger.debug("Found config file: %s", config_file)
        else:
            logger.error("No config file found for module: %s", module_name)
            return -1

        config.read(config_file)

        logger.debug(yaml.dump(config._sections))

        # Gets the information about the model class from the config file
        # Imports the according model and instantiates it
        model_class = getattr(import_module, "Model")
        model = model_class()
        module.model = model

        module.model.widget_changed.connect(main_view.on_module_widget_changed)

        # Sets parameters of the model from the config file
        model.name = config["META"]["name"]
        model.tooltip = config["META"]["tooltip"]
        # model.category = config["META"]["category"]

        # Gets the information about the controller class from the config file
        # Imports the according controller and instantiates it
        controller_class = getattr(import_module, "Controller")
        controller = controller_class(model)
        module.controller = controller

        # Gets the information about the view class from the config file
        # Imports the according view and instantiates it
        view_class = getattr(import_module, "View")
        view = view_class(model, controller)
        module.view = view

        # Add the module to the main model object
        self._main_model.add_module(model.name, module)

