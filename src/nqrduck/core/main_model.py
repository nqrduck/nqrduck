import logging
from pathlib import Path
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon
from ..module.module import Module

logger = logging.getLogger(__name__)


class MainModel(QObject):
    DEFAULT_CONFIG = "configuration.ini"

    module_added = pyqtSignal(Module)
    active_module_changed = pyqtSignal(Module)

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
        self._loaded_modules[name] = module
        logger.debug("Added module: %s", name)
        self.module_added.emit(module)
