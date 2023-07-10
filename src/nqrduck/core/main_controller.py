import logging
import importlib
import importlib.metadata

import importlib
from PyQt6.QtCore import QObject, pyqtSlot

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

            # On loading of the modules the signal for adding a menu entry is connected to the according slot in the main view
            module.view.add_menubar_item.connect(main_view.on_menu_bar_item_added)

            module.controller.on_loading()

            # Connect the nqrduck_signal to the dispatch_signals slot
            module.nqrduck_signal.connect(self.dispatch_signals)

    @pyqtSlot(str, str)
    def dispatch_signals(self, key: str, value: str):
        for module in self._main_model.loaded_modules.values():
            module.controller.process_signals(key, value)

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
