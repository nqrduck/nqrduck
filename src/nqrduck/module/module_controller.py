from PyQt5.QtCore import QObject

class ModuleController(QObject):
    def __init__(self, module):
        super().__init__()
        self.module = module

    @property
    def module(self):
        return self._module
    
    @module.setter
    def module(self, value):
        self._module = value

    def on_loading(self):
        pass

    def process_signals(self, key, value):
        pass