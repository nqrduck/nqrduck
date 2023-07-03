import os
import sys
import logging
import glob
import importlib
import importlib.metadata
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
        # Get the modules with entry points in the nqrduck group
        modules = self._get_modules()
        logger.debug("Found modules: %s", modules)

        for module_name, module in modules.items():
            if module.view is None:
                logger.debug("Module has no view: %s ... skipping", module_name)
                continue

            # Import the module
            logger.debug("Loading Module: %s", module_name)
            module._model.widget_changed.connect(main_view.on_module_widget_changed)
            logger.debug("Adding module to main model: %s", module_name)
            self._main_model.add_module(module._model.name, module)

    @staticmethod
    def _get_modules():
        """
        Returns a dictionary of all modules found in the entry points with 'nqrduck'

        Returns: dict -- Dictionary of modules
        """
        modules = {}

        for entry_point in importlib.metadata.entry_points().get("nqrduck", []):
            modules[entry_point.name] = entry_point.load()

        return modules
