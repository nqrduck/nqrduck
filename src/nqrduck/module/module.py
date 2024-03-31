"""Module class for the different modules of the application."""
import logging
import yaml
import configparser
import inspect
import pathlib
from PyQt6.QtCore import pyqtSignal, QObject

logger = logging.getLogger(__name__)

class Module(QObject):
    """Module class for the different modules of the application.
    
    Args:
        model (ModuleModel): The model of the module
        view (ModuleView): The view of the module
        controller (ModuleController): The controller of the module
    
    Attributes:
        MODULE_CONFIG_PATH (str): The path to the module config file
        nqrduck_signal (pyqtSignal): Signal to send messages to the main controller
    """
    MODULE_CONFIG_PATH = "resources"

    nqrduck_signal = pyqtSignal(str, object)

    def __init__(self, model, view, controller):
        """Initializes the Module."""
        super().__init__()
        self.model = model(self)
        self.controller = controller(self)
        if view is not None:
            self.view = view(self)
        else:
            self.view = None

        # Read module config file
        config = configparser.ConfigParser(allow_no_value=True)
        # Make config parser case sensitive
        config.optionxform = str
        
        # Get path of module config file - we need the first frame in the stack that provides a config file
        
        config_path = pathlib.Path(inspect.getfile(model)).parent
        config_path = config_path / self.MODULE_CONFIG_PATH
        logger.debug("Attempting to load module config file: %s", config_path)

        config_file = list(config_path.glob("*.ini"))

        

        if config_file:
            logger.debug("Found config file: %s", config_file)
        else:
            logger.error("No config file found for module: %s", config_path)
            return -1

        config.read(config_file[0])

        logger.debug(yaml.dump(config._sections))

        # Sets parameters of the model from the config file
        self.model.name = config["META"]["name"]
        self.model.tooltip = config["META"]["tooltip"]
        self.model.toolbar_name = config["META"]["toolbar_name"]

    @property
    def model(self):
        """The model of the module."""
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def controller(self):
        """The controller of the module."""
        return self._controller

    @controller.setter
    def controller(self, value):
        self._controller = value

    @property
    def view(self):
        """The view of the module."""
        return self._view

    @view.setter
    def view(self, value):
        self._view = value

    
