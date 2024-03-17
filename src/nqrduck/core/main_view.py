import logging
from PyQt6.QtCore import pyqtSlot, Qt, QTimer
from PyQt6.QtWidgets import QMainWindow, QToolButton, QMenu, QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QHBoxLayout, QWidget, QApplication, QPushButton, QTextEdit
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

        self.connect_signals()

        self.setWindowIcon(self._main_model.logo)

        # Set font for the whole application via the stylesheet
        default_font = QApplication.font()
        default_font_size = int(default_font.pointSize() * 2.5)

        logger.debug("Setting font to size: %s", default_font_size)

        self.setStyleSheet(f"""
            * {{
                font-family: '{self._main_model.font}';
                font-size: {default_font_size}pt;
            }}
        """)

        self._layout = self._ui.centralwidget.layout()

    def connect_signals(self) -> None:
        """ Connects various signals to the according slots in the main view."""
        self._main_model.module_added.connect(self.on_module_loaded)
        self._main_model.active_module_changed.connect(self.on_active_module_changed)

        # Statusbar Message
        self._main_model.statusbar_message_changed.connect(
            self._ui.statusbar.showMessage
        )

        # Notification Dialog
        self._main_controller.create_notification_dialog.connect(self.create_notification_dialog)

        # About Modules
        self._ui.actionAbout_Modules.triggered.connect(self.on_about_modules)

        # About NQRduck
        self._ui.actionAbout_NQRduck.triggered.connect(self.on_about_nqrduck)

        # Logger
        self._ui.actionLogger.triggered.connect(self.on_logger)


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

        # Indicate which module is active by making the text bold for this we iterate over the  buttons inside the toolbox
        for button in  self._toolbox.findChildren(QToolButton):
            if button.text() == module.model.toolbar_name:
                button.setStyleSheet("font-weight: bold")
            else:
                button.setStyleSheet("font-weight: normal")

    def on_module_widget_added(self, widget: "QWidget") -> None:
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

        self.on_module_widget_added(module.view)

    def on_tool_button_clicked(self, module_name):
        logger.debug("Active module changed to: %s", module_name)
        self._main_model.active_module = self._main_model.loaded_modules[module_name]

    @pyqtSlot(str, list)
    def on_menu_bar_item_added(self, menu_name : str, actions : list) -> None:
        """Adds a menu bar item to the main view.

        Args:
            menu_name (str) -- The name of the menu bar item
            actions (list) -- A list of actions to add to the menu bar item
        """
        logger.debug("Adding menu bar item to main view: %s", menu_name)
        qmenu = QMenu(menu_name, self)
        for action in actions:
            logger.debug("Adding action to menu bar: %s", action.text())
            action.setParent(self)
            qmenu.addAction(action)

        # Get the action before which you want to insert your menu
        before_action = self.menuBar().actions()[0]

        self.menuBar().insertMenu(before_action, qmenu)

    @pyqtSlot()
    def on_about_modules(self) -> None:
        """Opens a dialog with information about the loaded modules."""
        about_modules = AboutModules(self)
        about_modules.exec()

    @pyqtSlot()
    def on_about_nqrduck(self) -> None:
        """Opens a dialog with information about the application."""
        about_nqrduck = AboutNQRduck(self)
        about_nqrduck.exec()

    @pyqtSlot()
    def on_logger(self) -> None:
        """Opens a dialog with the log messages of the application."""
        logger_window = LoggerWindow(self)
        logger_window.exec()
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
    """This class provides a simple splash screen for the application.
    It shows the logo of the application for 2 seconds and then closes itself.
    """
    def __init__(self):
        super().__init__()
        logger.debug("Showing Splash Screen")

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.logo = Logos.Logo_full()
        self.logo_label = QLabel()
        self.logo_label.setPixmap(self.logo.pixmap(self.logo.availableSizes()[0]))
        self.logo_label.setStyleSheet("border: 0px solid green")


        self.main_layout.addWidget(self.logo_label)
        self.setLayout(self.main_layout)

        self.timer = QTimer()
        self.timer.singleShot(2000, self.close)
        
        # Set window properties
        self.setWindowFlags(Qt.WindowType.SplashScreen)

class AboutModules(QDialog):
    """This class provides a simple dialog for displaying information about the different modules.
    It shows the module name and the version of the module.
    """

    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)

        self.setWindowTitle("About Modules")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # Add black border and  fill background
        self.setStyleSheet("QDialog { border: 2px solid black; background-color: white }")
        
        self.module_info = QLabel("Installed Modules:")
        # Make text bold
        self.module_info.setStyleSheet("font-weight: bold")
        self.layout.addWidget(self.module_info)

        # Create module Label
        self.modules  = QLabel()

        modules =  parent._main_model.loaded_modules
        for module in modules:
            self.modules.setText("\t" + self.modules.text() + f"\n{module}")
            # Add the  submodules
            submodules = modules[module].model.submodules
            for submodule in submodules:
                self.modules.setText("\t \t" + self.modules.text() + f"\n\t{submodule}")

        self.layout.addWidget(self.modules)
        self.layout.addStretch()

        # Add an OK button to close the dialog
        ok_button = QPushButton('OK', self)
        ok_button.clicked.connect(self.accept)
        self.layout.addWidget(ok_button)

class AboutNQRduck(QDialog):
    """This class provides a simple dialog for displaying information about the application.
    It shows the name of the application and the version of the application.
    """

    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)

        self.setWindowTitle("About NQRduck")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # Add black border and  fill background
        self.setStyleSheet("QDialog { border: 2px solid black; background-color: white }")
        
        self.app_info = QLabel("NQRduck")
        # Make text bold
        self.app_info.setStyleSheet("font-weight: bold")
        self.layout.addWidget(self.app_info)

        #NQRduck logo
        self.logo = Logos.Logo_full()
        self.logo_label = QLabel()
        self.logo_label.setPixmap(self.logo.pixmap(self.logo.availableSizes()[0]))
        self.layout.addWidget(self.logo_label)

        # Link to the repository -  hardcoded link: evil
        self.repository_link = QLabel("<a href='https://github.com/nqrduck/'>GitHub Project</a>")
        self.repository_link.setOpenExternalLinks(True)
        self.layout.addWidget(self.repository_link)

        self.layout.addStretch()

        # Add an OK button to close the dialog
        ok_button = QPushButton('OK', self)
        ok_button.clicked.connect(self.accept)
        self.layout.addWidget(ok_button)

class LoggerWindow(QDialog):
    """This class provides a simple dialog for displaying the log messages of the application.
    It shows the log messages and the log level of the log message.
    """

    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)

        self.setWindowTitle("Logger")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Make log window half the screen width
        self.setFixedWidth(int(QApplication.primaryScreen().size().width() / 2))

        # Add black border and  fill background
        self.setStyleSheet("QDialog { border: 2px solid black; background-color: white }")

        # Height is also half the screen height
        self.setFixedHeight(int(QApplication.primaryScreen().size().height() / 2))

        log_level = logging.getLevelName(logger.parent.level)

        self.log_level = QLabel(f"Log Level: {log_level}")
        self.layout.addWidget(self.log_level)
        
        self.log_info = QLabel("Log Messages:")
        # Make text bold
        self.log_info.setStyleSheet("font-weight: bold")
        self.layout.addWidget(self.log_info)

        # Create scrollable text area for the logs
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        # Leave some space for the other widgets
        self.logs.setFixedHeight(int(QApplication.primaryScreen().size().height() * 0.4))

        logs =  logger.parent.handlers[1].baseFilename
        
        with open(logs, 'r') as file:
            log = file.read().strip()

            # Go through lines
            for line in log.split("\n"):
                try:
                    line = line.split(" - ")
                    timestampe = line[0]
                    name = line[1]
                    level = line[2]
                    message = " - ".join(line[3:])
                    # Create html message: timestamp is blue, name is green, level is red message black
                    html_message = f"<font color='blue'>{timestampe}</font> - <font color='green'>{name}</font> - <font color='red'>{level}</font> - {message}"
                # If this fails the line is part of a multiline log message and therefor the text is simply black
                except IndexError:
                    html_message = f"<font color='black'>{line}</font>" 
                
                self.logs.append(html_message)


        self.layout.addWidget(self.logs)
        # Scroll to bottom
        self.logs.verticalScrollBar().setValue(
            self.logs.verticalScrollBar().maximum()
         )
        
        self.layout.addStretch()

        # Add an OK button to close the dialog
        ok_button = QPushButton('OK', self)
        ok_button.clicked.connect(self.accept)
        self.layout.addWidget(ok_button)
