"""Contains the ModuleView class which is the base class for all module views."""

from PyQt6.QtWidgets import QWidget, QFileDialog
from PyQt6.QtCore import pyqtSignal, QObject
from nqrduck.module.module import Module


class ModuleView(QWidget):
    """Base class for module views.

    Args:
        module (Module): The module of the view

    Signals:
        widget_changed : Emitted when a widget has been changed
        add_menubar_item : Emitted when a menu bar item should be added
    """

    widget_changed = pyqtSignal(QObject)
    add_menubar_item = pyqtSignal(str, list, bool)

    def __init__(self, module):
        """Initializes the ModuleView."""
        super().__init__()
        self.module = module

    @property
    def widget(self):
        """The widget of the view."""
        return self._widget

    @widget.setter
    def widget(self, value):
        self._widget = value
        self.widget_changed.emit(value)

    @property
    def module(self) -> Module:
        """The module of the view."""
        return self._module

    @module.setter
    def module(self, value):
        self._module = value

    class QFileManager:
        """This class provides methods for opening and saving files.

        Args:
            extension (str): The extension of the files to open or save
            parent (QWidget): The parent widget of the file dialog
        """

        def __init__(self, extension, parent=None):
            """Initializes the QFileManager."""
            self.extension = extension
            self.parent = parent

        def loadFileDialog(self) -> str:
            """Opens a file dialog for the user to select a file to open.

            Returns:
                str: The path of the file selected by the user.
            """
            extension_name = self.extension.upper()
            fileName, _ = QFileDialog.getOpenFileName(
                self.parent,
                "QFileManager - Open File",
                "",
                f"{extension_name} Files (*.{self.extension});;All Files (*)",
                options=QFileDialog.Option.DontUseNativeDialog,
            )
            if fileName:
                return fileName
            else:
                return None

        def saveFileDialog(self) -> str:
            """Opens a file dialog for the user to select a file to save.

            Returns:
                str: The path of the file selected by the user.
            """
            extension_name = self.extension.upper()
            fileName, _ = QFileDialog.getSaveFileName(
                self.parent,
                "QFileManager - Save File",
                "",
                f"{extension_name} Files (*.{self.extension});;All Files (*)",
                options=QFileDialog.Option.DontUseNativeDialog,
            )
            if fileName:
                # Append the .quack extension if not present
                if not fileName.endswith(f".{self.extension}"):
                    fileName += f".{self.extension}"
                return fileName
            else:
                return None
