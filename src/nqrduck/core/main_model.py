import logging
from pathlib import Path
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import QObject, pyqtSignal, QSettings
from PyQt6.QtGui import QPixmap, QIcon
from ..module.module import Module

logger = logging.getLogger(__name__)

class SettingsManager(QObject):
    """Manages the settings for the application.
    This can be the font, the theme, the window size, etc.
    """
    settings_changed = pyqtSignal()

    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)
        self.settings = QSettings("NQRduck", "NQRduck")

    @property
    def font(self) -> QFont:
        font = self.settings.value("font", QFont())
        return font
    
    @font.setter
    def font(self, value: QFont) -> None:
        self.settings.setValue("font", value)
        self.settings_changed.emit()

    @property
    def font_size(self) -> int:
        font_size = self.settings.value("font_size", 12)
        return font_size
    
    @font_size.setter
    def font_size(self, value: int) -> None:
        self.settings.setValue("font_size", value)
        self.settings_changed.emit()

    @property
    def style_factory(self) -> str:
        """ The style factory used for the application."""
        style_factory = self.settings.value("style_factory", "Fusion")
        return style_factory
    
    @style_factory.setter
    def style_factory(self, value: str) -> None:
        self.settings.setValue("style_factory", value)
        self.settings_changed.emit()
    
    @property
    def module_order(self) -> list:
        """ The order in  which the modules are displayed in the main window. """
        module_order = self.settings.value("module_order", [])
        return module_order
    
    @module_order.setter
    def module_order(self, value: list) -> None:
        self.settings.setValue("module_order", value)
        self.settings_changed.emit()

class MainModel(QObject):

    module_added = pyqtSignal(Module)
    active_module_changed = pyqtSignal(Module)
    statusbar_message_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._loaded_modules = dict()

        # Get the setting manager
        self.settings = SettingsManager(parent=self)

        # Set Logo
        self_path = Path(__file__).parent
        logo_path = self_path / "resources/logo.png"
        self.logo = QIcon(QPixmap(str(logo_path)))

        # Set Font
        font_path = self_path / "resources/font/AsepriteFont.ttf"
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        self.font = font_families[0]

        # Set default status bar message
        self.statusbar_message = "Ready"

    @property
    def active_module(self):
        return self._active_module

    @active_module.setter
    def active_module(self, value):
        self._active_module = value
        self.active_module_changed.emit(value)

    @property
    def loaded_modules(self):
        return self._loaded_modules

    def add_module(self, name, module):
        """Adds a module to the loaded modules dictionary
        
        Arguments:
            name (str) -- The name of the module
            module (Module) -- The module to add
        """
        self._loaded_modules[name] = module
        logger.debug("Added module: %s", name)
        self.module_added.emit(module)

    @property
    def statusbar_message(self):
        return self._statusbar_message
    
    @statusbar_message.setter
    def statusbar_message(self, value):
        self._statusbar_message = value
        logger.debug("Status bar message changed to: %s", value)
        self.statusbar_message_changed.emit(value)
