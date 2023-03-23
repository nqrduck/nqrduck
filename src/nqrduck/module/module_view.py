from PyQt5.QtWidgets import QWidget


class ModuleView(QWidget):
    def __init__(self, model, controller):
        super().__init__()
        self._model = model
        self._controller = controller
