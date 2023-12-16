from PyQt6.QtWidgets import QWidget, QFileDialog
from PyQt6.QtCore import pyqtSignal, QObject
from nqrduck.module.module import Module

class ModuleView(QWidget):
    widget_changed = pyqtSignal(QObject)
    add_menubar_item = pyqtSignal(str, list)

    def __init__(self,  module):
        super().__init__()
        self.module = module

    @property
    def widget(self):
        return self._widget

    @widget.setter
    def widget(self, value):
        self._widget = value
        self.widget_changed.emit(value)

    @property
    def module(self) -> Module:
        return self._module
    
    @module.setter
    def module(self, value):
        self._module = value

    class QFileManager:
        """This class provides methods for opening and saving files."""
        def __init__(self, extenstion, parent=None):
            self.extension = extenstion
            self.parent = parent

        def loadFileDialog(self) -> str:
            """Opens a file dialog for the user to select a file to open.
            
            Returns:
                str: The path of the file selected by the user.
            """
            extension_name = self.extension.upper()
            fileName, _ = QFileDialog.getOpenFileName(self.parent,
                                                    "QFileManager - Open File",
                                                    "",
                                                    "%s Files (*.%s);;All Files (*)" % (extension_name, self.extension),
                                                    options=QFileDialog.Option.DontUseNativeDialog)
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
            fileName, _ = QFileDialog.getSaveFileName(self.parent,
                                                    "QFileManager - Save File",
                                                    "",
                                                    "%s Files (*.%s);;All Files (*)" % (extension_name, self.extension),
                                                    options=QFileDialog.Option.DontUseNativeDialog)
            if fileName:
                # Append the .quack extension if not present
                if not fileName.endswith(". %s" % self.extension):
                    fileName += ".%s" % self.extension
                return fileName
            else:
                return None
