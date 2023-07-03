
import glob
import logging
import yaml
import configparser
import inspect
import pathlib

logger = logging.getLogger(__name__)

class Module():
    MODULE_CONFIG_PATH = "resources"

    def __init__(self, model, view, controller):
        self._model = model(self)
        self._controller = controller(self)
        if view:
            self._view = view(self)

        # Read module config file
        config = configparser.ConfigParser(allow_no_value=True)
        # Make config parser case sensitive
        config.optionxform = str
        config_path =pathlib.Path(inspect.stack()[1].filename).parent
        config_path = config_path / self.MODULE_CONFIG_PATH
        logger.debug("Attempting to load module config file: %s", config_path)

        config_file = config_path.glob("**/*.ini")

        if config_file:
            logger.debug("Found config file: %s", config_file)
        else:
            logger.error("No config file found for module: %s", config_path)
            return -1

        config.read(config_file)

        logger.debug(yaml.dump(config._sections))

        # Sets parameters of the model from the config file
        self._model.name = config["META"]["name"]
        self._model.tooltip = config["META"]["tooltip"]
        self._model.toolbar_name = config["META"]["toolbar_name"]

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, value):
        self._controller = value

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, value):
        self._view = value

    
