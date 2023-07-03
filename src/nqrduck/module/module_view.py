from PyQt5.QtWidgets import QWidget, QMenu
from PyQt5.QtCore import pyqtSignal, QObject


class ModuleView(QWidget):
    widget_changed = pyqtSignal(QObject)

    def __init__(self,  module):
        super().__init__()
        self._module = module

    @property
    def widget(self):
        return self._widget

    @widget.setter
    def widget(self, value):
        self._widget = value
        self.widget_changed.emit(value)
