import logging
import importlib
import importlib.metadata

import importlib
from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal

logger = logging.getLogger(__name__)


class MainController(QObject):
    create_notification_dialog = pyqtSignal(list)

    def __init__(self, main_model):
        super().__init__()
        self.main_model = main_model

    def load_modules(self, main_view) -> None:
        """Loads all modules with entry points in the nqrduck group
        Also connects the nqrduck_signal to the dispatch_signals slot and creates the menu bar entries.

        Arguments:
            main_view (MainView) -- The main view of the application"""
        # Get the modules with entry points in the nqrduck group
        modules = self._get_modules()
        logger.debug("Found modules: %s", modules)

        for module_name, module in modules.items():
            # Connect the nqrduck_signal to the dispatch_signals slot
            module.nqrduck_signal.connect(self.dispatch_signals)

            if module.view is None:
                logger.debug("Module has no view: %s ... skipping", module_name)
                continue

            logger.debug("View of module: %s", module.view)
            # Import the module
            logger.debug("Loading Module: %s", module_name)
            module.model.widget_changed.connect(main_view.on_module_widget_added)
            logger.debug("Adding module to main model: %s", module_name)
            self.main_model.add_module(module._model.name, module)

            # On loading of the modules the signal for adding a menu entry is connected to the according slot in the main view
            module.view.add_menubar_item.connect(main_view.on_menu_bar_item_added)

            module.controller.on_loading()

    @pyqtSlot(str, object)
    def dispatch_signals(self, key: str, value: object):
        """Dispatches the signals to the according module.
        This method is connected to the nqrduck_signal of the modules.
        It's the main way of communication between the modules.

        Arguments:
            key (str) -- The key of the signal
            value (object) -- The value of the signal"""
        for module in self.main_model.loaded_modules.values():
            # This is a special signal that is used to set the status bar message
            if key == "statusbar_message":
                logger.debug("Setting status bar message: %s", value)
                self.main_model.statusbar_message = value
                break
            # This is a special signal that is used to show a notification dialog
            elif key == "notification":
                logger.debug("Showing notification: %s", value)
                self.create_notification_dialog.emit(value)
                break

            logger.debug("Dispatching signal %s to module: %s", key, module)
            module.controller.process_signals(key, value)

    @staticmethod
    def _get_modules():
        """
        Returns a dictionary of all modules found in the entry points with 'nqrduck'

        Returns: dict -- Dictionary of modules
        """
        modules = {}

        for entry_point in importlib.metadata.entry_points().select(group="nqrduck"):
            modules[entry_point.name] = entry_point.load()

        return modules
