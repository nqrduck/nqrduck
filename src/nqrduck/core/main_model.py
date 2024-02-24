import logging
from pathlib import Path
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon
from ..module.module import Module

logger = logging.getLogger(__name__)


class MainModel(QObject):

    module_added = pyqtSignal(Module)
    active_module_changed = pyqtSignal(Module)
    statusbar_message_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._loaded_modules = dict()

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
