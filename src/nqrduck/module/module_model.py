"""Base class for module model."""

from PyQt6.QtCore import QObject, pyqtSignal


class ModuleModel(QObject):
    """Base class for module model.

    Args:
        module (Module): The module of the model

    Signals:
        widget_changed : Emitted when a widget has been changed
    """

    widget_changed = pyqtSignal(QObject)

    def __init__(self, module) -> None:
        """Initializes the ModuleModel."""
        super().__init__()
        self.module = module
        self.submodules = []

    @property
    def module(self):
        """The module of the model."""
        return self._module

    @module.setter
    def module(self, value):
        self._module = value

    @property
    def name(self):
        """The name of the module."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def toolbar_name(self):
        """The name of the toolbar.

        This is displayed in the main window.
        """
        return self._toolbox_name

    @toolbar_name.setter
    def toolbar_name(self, value):
        self._toolbox_name = value

    @property
    def category(self):
        """The category of the module."""
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def tooltip(self):
        """The tooltip of the module."""
        return self._tooltip

    @tooltip.setter
    def tooltip(self, value):
        self._tooltip = value

    @property
    def config(self):
        """The configuration of the module."""
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def module_type(self):
        """The type of the module."""
        return self._module_type

    @property
    def submodules(self):
        """The submodules of the module."""
        return self._submodules

    @submodules.setter
    def submodules(self, value):
        self._submodules = value

    def add_submodule(self, submodule):
        """Adds a submodule to the module.

        Args:
            submodule (Module): The submodule to add
        """
        self.submodules.append(submodule)
