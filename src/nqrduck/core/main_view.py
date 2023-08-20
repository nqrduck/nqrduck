import logging
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import pyqtSlot, Qt, QTimer
from PyQt6.QtWidgets import QMainWindow, QToolButton, QMenu, QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QHBoxLayout, QWidget, QApplication
from .main_window import Ui_MainWindow
from ..module.module import Module
from ..assets.icons import Logos

logger = logging.getLogger(__name__)


class MainView(QMainWindow):
    def __init__(self, main_model, main_controller):
        super().__init__()
        # Use the splash screen
        self.splash = SplashScreen()
        self.splash.setFocus()
        self.splash.show()

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
    def create_notification_dialog(self, notification : list) -> None:
        """Creates a notification dialog with the given message and type.
        The type can be 'Info', 'Warning' or 'Error' and changes the color and symbol of the dialog.
        
        Arguments:
            notification (list) -- The notification to display. It has the form [type, message]
        """
        NotificationDialog(notification, self)

    def on_active_module_changed(self, module : Module) -> None:
        """Changes the current widget in the stacked widget to the view of the active module.
        
        Args:
            module (Module) -- The active module"""
        self._ui.stackedWidget.setCurrentWidget(module.view)

    def on_module_widget_changed(self, widget: "QWidget"):
        """Adds a module widget to the stacked widget and sets it as the current widget.
        
        Args:
            widget (QWidget) -- The widget to add"""
        logger.debug("Adding module widget to stacked widget: %s", widget)
        self._ui.stackedWidget.addWidget(widget)
        self._ui.stackedWidget.setCurrentWidget(widget)

    def on_module_loaded(self, module : Module) -> None:
        """Adds a module to the toolbar and connects the clicked signal to the according slot in the main view.
        Also connects the widget_changed signal of the module to the according slot in the main view.
        
        Arguments:
            module (Module) -- The module to add
        """
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
    def on_menu_bar_item_added(self, menu_name : str, actions : list) -> None:
        logger.debug("Adding menu bar item to main view: %s", menu_name)
        qmenu = QMenu(menu_name, self)
        for action in actions:
            logger.debug("Adding action to menu bar: %s", action.text())
            action.setParent(self)
            qmenu.addAction(action)

        self._ui.menubar.addMenu(qmenu)

class NotificationDialog(QDialog):
    """This class provides a simple dialog for displaying notifications by the different modules.
    It has a message it displays and a type. The type can be 'Info', 'Warning' or 'Error' and changes the color and symbol of the dialog.
    """
    def __init__(self, notification, parent=None):
        super().__init__()
        self.setParent(parent)

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


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        logger.debug("Showing Splash Screen")

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.logo = Logos.Logo_64x32()
        self.logo_label = QLabel()
        self.logo_label.setPixmap(self.logo.pixmap(self.logo.availableSizes()[0]))
        self.logo_label.setStyleSheet("border: 0px solid green")

        self.title_duck_label = QLabel()
        self.title_duck = Logos.LabMallard_32x32()
        self.title_duck_label.setPixmap(self.title_duck.pixmap(self.title_duck.availableSizes()[0]))

        self.main_layout.addWidget(self.logo_label)
        self.main_layout.addWidget(self.title_duck_label)
        self.setLayout(self.main_layout)

        self.timer = QTimer()
        self.timer.singleShot(2000, self.close)
        
        # Set window properties
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.WindowStaysOnTopHint)

        # Set border and background color
        self.setStyleSheet("QWidget { background-color: rgb(134, 234, 154) }")
