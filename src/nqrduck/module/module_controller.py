"""Base class for module controllers."""

from PyQt6.QtCore import QObject


class ModuleController(QObject):
    """Base class for module controllers."""

    def __init__(self, module):
        """Initializes the ModuleController."""
        super().__init__()
        self.module = module

    @property
    def module(self):
        """The module of the controller."""
        return self._module

    @module.setter
    def module(self, value):
        self._module = value

    def on_loading(self):
        """This method is called when the module is loaded.

        Implement this method in the subclass.
        """
        pass

    def process_signals(self, key, value):
        """Processes the signals from the module.

        Implement this method in the subclass.
        """
        pass
