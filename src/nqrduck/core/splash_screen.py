"""The SplashScreen class provides a splash screen for the application."""

import logging
from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from ..assets.icons import Logos

logger = logging.getLogger(__name__)


class SplashScreen(QSplashScreen):
    """This class provides a simple splash screen for the application.

    It shows the logo of the application for 2 seconds and then closes itself.
    """

    def __init__(self):
        """Initializes the SplashScreen."""
        super().__init__()
        logger.debug("Showing Splash Screen")

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowType.SplashScreen)

        self.logo = Logos.Logo_full()

        pixmap = QPixmap(self.logo.pixmap(self.logo.availableSizes()[0]))

        self.setPixmap(pixmap)

        self.show()
