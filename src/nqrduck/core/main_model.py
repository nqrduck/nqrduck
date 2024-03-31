"""The main model for the application."""

import logging
from pathlib import Path
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import QObject, pyqtSignal, QSettings
from PyQt6.QtGui import QPixmap, QIcon
import PyQt6.QtWidgets
from ..module.module import Module

logger = logging.getLogger(__name__)


class SettingsManager(QObject):
    """Manages the settings for the application.

    This can be the font, the theme, the window size, etc.

    Arguments:
        parent (QObject) : The parent object
    """

    settings_changed = pyqtSignal()

    def __init__(self, parent: QObject = None) -> None:
        """Initializes the SettingsManager."""
        super().__init__(parent)
        self.settings = QSettings("NQRduck", "NQRduck")

        # Default Aseprite font
        self_path = Path(__file__).parent
        font_path = self_path / "resources/font/AsepriteFont.ttf"
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        self.default_font = font_families[0]

        # Available Style Factories
        self.style_factories = PyQt6.QtWidgets.QStyleFactory.keys()

        # Set default settings
        if not self.settings.contains("font"):
            self.settings.setValue("font", self.default_font)
        if not self.settings.contains("font_size"):
            self.settings.setValue("font_size", 22)
        if not self.settings.contains("style_factory"):
            self.settings.setValue("style_factory", self.style_factories[-1])
        if not self.settings.contains("module_order"):
            self.settings.setValue(
                "module_order", [key for key in self.parent().loaded_modules.keys()]
            )

    @property
    def font(self) -> QFont:
        """The font used for the application."""
        font = self.settings.value("font", self.default_font)
        return font

    @font.setter
    def font(self, value: QFont) -> None:
        self.settings.setValue("font", value)
        self.settings_changed.emit()

    @property
    def font_size(self) -> int:
        """The font size used for the application."""
        font_size = self.settings.value("font_size", 22)
        return font_size

    @font_size.setter
    def font_size(self, value: int) -> None:
        self.settings.setValue("font_size", value)
        self.settings_changed.emit()

    @property
    def style_factory(self) -> str:
        """The style factory used for the application."""
        style_factory = self.settings.value(
            "style_factory", PyQt6.QtWidgets.QStyleFactory.keys()[-1]
        )
        return style_factory

    @style_factory.setter
    def style_factory(self, value: str) -> None:
        self.settings.setValue("style_factory", value)
        self.settings_changed.emit()

    @property
    def module_order(self) -> list:
        """The order in  which the modules are displayed in the main window."""
        self._module_order = self.settings.value(
            "module_order", [key for key in self.parent().loaded_modules.keys()]
        )
        if (
            self._module_order is None
            or self._module_order == []
            or self._module_order == {}
        ):
            self._module_order = [key for key in self.parent().loaded_modules.keys()]
            self.settings.setValue("module_order", self._module_order)
            logger.debug("Module order set to default")

        # Check if there are new modules that are not in the module order, if so add them to the end
        for key in self.parent().loaded_modules.keys():
            if key not in self._module_order:
                self._module_order.append(key)
                self.settings.setValue("module_order", self._module_order)
                logger.debug("Added new module to module order: %s", key)

        return self._module_order

    @module_order.setter
    def module_order(self, value: list) -> None:
        logger.debug("Setting module order to: %s", value)
        self.settings.setValue("module_order", value)
        self.settings_changed.emit()

    def reset_settings(self) -> None:
        """Resets the settings to default values."""
        self.settings.clear()
        self.settings.setValue("font", self.default_font)
        self.settings.setValue("font_size", 22)
        self.settings.setValue("style_factory", self.style_factories[-1])
        self.settings.setValue(
            "module_order", [key for key in self.parent().loaded_modules.keys()]
        )
        self.settings_changed.emit()


class MainModel(QObject):
    """The main model for the application.

    This class is the main model for the application. It holds the different modules that have been loaded.
    It also holds the active module and the status bar message.

    Signals:
        module_added : Emitted when a module has been added
        active_module_changed : Emitted when the active module has changed
        statusbar_message_changed : Emitted when the status bar message has changed
    """

    module_added = pyqtSignal(Module)
    active_module_changed = pyqtSignal(Module)
    statusbar_message_changed = pyqtSignal(str)

    def __init__(self):
        """Initializes the MainModel."""
        super().__init__()
        self._loaded_modules = dict()

        # Get the setting manager
        self.settings = SettingsManager(parent=self)

        # Set Logo
        self_path = Path(__file__).parent
        logo_path = self_path / "resources/logo.png"
        self.logo = QIcon(QPixmap(str(logo_path)))

        # Set default status bar message
        self.statusbar_message = "Ready"

    @property
    def active_module(self):
        """The active module."""
        return self._active_module

    @active_module.setter
    def active_module(self, value):
        self._active_module = value
        self.active_module_changed.emit(value)

    @property
    def loaded_modules(self) -> dict:
        """Dict with the different modules that have been loaded.

        The key is the name of the module and the value is the module object.
        """
        return self._loaded_modules

    def add_module(self, name: str, module: Module) -> None:
        """Adds a module to the loaded modules dictionary.

        Arguments:
            name (str) : The name of the module
            module (Module) : The module to add
        """
        self._loaded_modules[name] = module
        logger.debug("Added module: %s", name)
        self.module_added.emit(module)

    @property
    def statusbar_message(self):
        """The status bar message displayed in the main window."""
        return self._statusbar_message

    @statusbar_message.setter
    def statusbar_message(self, value):
        self._statusbar_message = value
        logger.debug("Status bar message changed to: %s", value)
        self.statusbar_message_changed.emit(value)
