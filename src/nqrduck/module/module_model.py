from PyQt6.QtCore import QObject, pyqtSignal


class ModuleModel(QObject):
    
    widget_changed = pyqtSignal(QObject)

    def __init__(self, module) -> None:
        super().__init__()
        self.module = module

    @property
    def module(self):
        return self._module
    
    @module.setter
    def module(self, value):
        self._module = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def toolbar_name(self):
        return self._toolbox_name
    
    @toolbar_name.setter
    def toolbar_name(self, value):
        self._toolbox_name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property 
    def tooltip(self):
        return self._tooltip

    @tooltip.setter
    def tooltip(self, value):
        self._tooltip = value

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def module_type(self):
        return self._module_type
    