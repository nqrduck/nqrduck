"""Contains the ModuleView class which is the base class for all module views."""

from PyQt6.QtWidgets import QWidget, QFileDialog
from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
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

    @pyqtSlot()
    def on_settings_changed(self):
        """Slot for when the settings have changed.
        
        This is implemented in the derived classes in case they need to update the view when the settings have changed.
        """
        pass

    class FileManager:
        """This class provides methods for opening and saving files.

        Args:
            extension (str): The extension of the files to open or save
            parent (QWidget): The parent widget of the file dialog
            caption (str): The caption of the file dialog
        """

        def __init__(self, extension, parent=None, caption = None):
            """Initializes the QFileManager."""
            self.extension = extension
            self.parent = parent
            self.caption = caption

        def loadFileDialog(self) -> str:
            """Opens a file dialog for the user to select a file to open.

            Returns:
                str: The path of the file selected by the user.
            """
            extension_name = self.extension.upper()
            caption_string = f"{self.caption} - Open .{self.extension} " if self.caption else f"Open .{self.extension} File"
            fileName, _ = QFileDialog.getOpenFileName(
                self.parent,
                caption_string,
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
            caption_string = f"{self.caption} - Save .{self.extension} " if self.caption else f"Save .{self.extension} File"
            fileName, _ = QFileDialog.getSaveFileName(
                self.parent,
                caption_string,
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
