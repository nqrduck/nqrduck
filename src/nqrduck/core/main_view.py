import logging
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QToolButton, QMenu, QAction
from .main_window import Ui_MainWindow
from ..module.module import Module

logger = logging.getLogger(__name__)


class MainView(QMainWindow):

    def __init__(self, main_model, main_controller):
        super().__init__()

        self._main_controller = main_controller
        self._main_model = main_model

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._toolbox = self._ui.toolBar
        self._toolbox.setFloatable(False)
        self._main_model.module_added.connect(self.on_module_loaded)
        self._main_model.active_module_changed.connect(self.on_active_module_changed)

        self._layout = self._ui.centralwidget.layout()

    def on_active_module_changed(self, module):
        self._ui.stackedWidget.setCurrentWidget(module.view)

    def on_module_widget_changed(self, widget):
        logger.debug("Adding module widget to stacked widget: %s", widget)
        self._ui.stackedWidget.addWidget(widget)
        self._ui.stackedWidget.setCurrentWidget(widget)

    def on_module_loaded(self, module):
        tool_button = QToolButton()
        tool_button.setText(module.model.toolbar_name)
        tool_button.clicked.connect(lambda: self.on_tool_button_clicked(module.model.name))
        self._toolbox.addWidget(tool_button)
        logger.debug("Added module to toolbar:%s", module.model.name)
        
        self.on_module_widget_changed(module.view)

    def on_tool_button_clicked(self, module_name):
        logger.debug("Active module changed to: %s", module_name)
        self._main_model.active_module = self._main_model.loaded_modules[module_name]

    @pyqtSlot(str, list)
    def on_menu_bar_item_added(self, menu_name, actions):
        logger.debug("Adding menu bar item to main view: %s", menu_name)
        qmenu = QMenu(menu_name, self)
        for action in actions:
            logger.debug("Adding action to menu bar: %s", action.text())
            action.setParent(self)
            qmenu.addAction(action)

        self._ui.menubar.addMenu(qmenu)
        