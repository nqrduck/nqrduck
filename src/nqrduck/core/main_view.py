import logging
from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import QMainWindow, QToolButton, QMenu, QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from .main_window import Ui_MainWindow

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

        self._main_model.statusbar_message_changed.connect(
            self._ui.statusbar.showMessage
        )

        self._main_controller.create_notification_dialog.connect(self.create_notification_dialog)

        self.setWindowIcon(self._main_model.logo)

        # Set font for the whole application via the stylesheet
        self.setStyleSheet((f"font: 25pt '{self._main_model.font}'"))

        self._layout = self._ui.centralwidget.layout()

    @pyqtSlot(list)
    def create_notification_dialog(self, notification):
        NotificationDialog(notification, self)

    def on_active_module_changed(self, module):
        self._ui.stackedWidget.setCurrentWidget(module.view)

    def on_module_widget_changed(self, widget):
        logger.debug("Adding module widget to stacked widget: %s", widget)
        self._ui.stackedWidget.addWidget(widget)
        self._ui.stackedWidget.setCurrentWidget(widget)

    def on_module_loaded(self, module):
        tool_button = QToolButton()
        tool_button.setText(module.model.toolbar_name)
        tool_button.clicked.connect(
            lambda: self.on_tool_button_clicked(module.model.name)
        )
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

class NotificationDialog(QDialog):
    """This class provides a simple dialog for displaying notifications by the different modules.
    It has a message it displays and a type. The type can be 'Info', 'Warning' or 'Error' and changes the color and symbol of the dialog."""
    def __init__(self, notification, parent=None):
        super().__init__(parent)

        type = notification[0]
        message = notification[1]

        self.setWindowTitle(type)
        self.layout = QVBoxLayout()
            
        if type == 'Info':
            self.color = Qt.GlobalColor.blue
            # self.icon = QIcon('path_to_info_icon')
        elif type == 'Warning':
            self.color = Qt.GlobalColor.yellow
            # self.icon = QIcon('path_to_warning_icon')
        elif type == 'Error':
            self.color = Qt.GlobalColor.red
            # self.icon = QIcon('path_to_error_icon')
                
        self.messageLabel = QLabel(message)
        self.messageLabel.setStyleSheet("QLabel { color : %s }" % self.color.name)
        # self.iconLabel = QLabel()
        # self.iconLabel.setPixmap(self.icon.pixmap(32, 32))
            
        self.layout.addWidget(self.messageLabel)
        # self.layout.addWidget(self.iconLabel)
            
        self.setLayout(self.layout)

        # Add an OK button to the dialog
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.layout.addWidget(self.buttonBox)

        self.exec()
