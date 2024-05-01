"""A wizard to install different NQRduck modules."""

import logging
import urllib.request
import json

from PyQt6.QtWidgets import (
    QWizard,
    QWizardPage,
    QFormLayout,
    QCheckBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)

from PyQt6.QtCore import QThread

from nqrduck.assets.icons import Logos

logger = logging.getLogger(__name__)


class DuckWizard(QWizard):
    """A wizard to install different NQRduck modules."""

    def __init__(self, installed_modules, parent=None):
        """Initializes the DuckWizard."""
        super().__init__(parent=parent)
        self.setParent(parent)

        self.setOption(QWizard.WizardOption.IndependentPages, False)
        self.setOption(QWizard.WizardOption.NoBackButtonOnStartPage, True)
        self.setOption(QWizard.WizardOption.NoBackButtonOnLastPage, True)

        self.addPage(WelcomePage())
        selection_page = SelectionPage(installed_modules)
        self.addPage(selection_page)
        self.addPage(InstallPage(selection_page))
        self.addPage(FinishPage())


class WelcomePage(QWizardPage):
    """The welcome page of the wizard."""

    def __init__(self) -> None:
        """Initializes the WelcomePage."""
        super().__init__()

        self.setTitle("Welcome to NQRduck")
        self.setSubTitle("This wizard will help you install NQRduck modules.")

        label = QLabel("Welcome to the NQRduck installer.")
        label.setWordWrap(True)

        logo_label = QLabel()
        icon = Logos.Logo_full()
        logo_label.setPixmap(icon.pixmap(logo_label.size()))

        # Link to the NQRduck GitHub repository
        link_label = QLabel('<a href="https://github.com/nqrduck">NQRduck</a>')
        link_label.setOpenExternalLinks(True)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(logo_label)
        layout.addWidget(link_label)
        self.setLayout(layout)


class SelectionPage(QWizardPage):
    """The selection page of the wizard.

    It uses the modules.json file to get the modules that can be installed.
    The modules.json file contains the name, description and source of the modules.
    It is hosted on GitHub.

    Args:
        installed_modules (list): The modules that are already installed
    """

    def __init__(self, installed_modules: list):
        """Initializes the SelectionPage."""
        super().__init__()

        self.installed_modules = installed_modules

        self.setTitle("Install NQRduck modules")
        self.setSubTitle(
            "Please specify the modules you want to install. The modules that are already installed are disabled."
        )

        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.modules = self.get_modules()
        self.generate_installation_widgets()

    def generate_installation_widgets(self) -> None:
        """Generate the installation widgets for the modules."""
        # First we get a list of already installed modules

        self.checkboxes = {}

        for num, module in enumerate(self.modules):
            module_widget = QWidget()
            module_widget.setLayout(QHBoxLayout())

            urls = self.get_URLs()
            link_widget = QLabel(f'<a href="{urls[num]}">{module["name"]}</a>')
            link_widget.setOpenExternalLinks(True)

            try:
                dependencies = module["dependencies"]
                dependencies = ", ".join(dependencies)
                tooltip = f"{module['description']} \n Dependencies: {dependencies}"
            except KeyError:
                tooltip = f"{module['description']} \n No dependencies"

            link_widget.setToolTip(tooltip)
            checkbox = QCheckBox()
            checkbox.setProperty("manually_checked", False)
            checkbox.clicked.connect(
                lambda state, module_name=module["name"]: self.on_checkbox_clicked(
                    state, module_name
                )
            )

            checkbox.stateChanged.connect(
                lambda state, module_name=module["name"]: self.on_checkbox_changed(
                    state, module_name
                )
            )

            # If the module is already installed, we disable the checkbox
            if module["name"] in self.installed_modules:
                checkbox.setChecked(True)
                checkbox.setEnabled(False)
                checkbox.setToolTip("Module is already installed")

            module_widget.layout().addWidget(link_widget)
            module_widget.layout().addStretch()
            module_widget.layout().addWidget(checkbox)
            self.layout.addRow(module_widget)
            self.checkboxes[module["name"]] = checkbox

    def get_modules(self) -> dict:
        """Get the modules from the modules json file.

        Returns:
            dict: The module data
        """
        json_url = "https://github.com/nqrduck/nqrduck-modules/raw/main/modules.json"
        file = urllib.request.urlopen(json_url).read()

        data = json.loads(file)
        logger.debug("Modules: %s", data)

        return data

    def get_URLs(self) -> list:
        """Get the URLs of the different modules.

        Returns:
            list: The URLs of the modules
        """
        urls = []
        for module in self.modules:
            source = module["source"]
            if source.startswith("https://"):
                urls.append(source)
            # If the source is just a name we assume its available on PyPI
            else:
                urls.append(f"https://pypi.org/project/{source}/")

        return urls

    def on_checkbox_changed(self, state: int, module_name: str) -> None:
        """Update the different modules when the checkbox is changed with the according dependencies.

        If a module is  manually checked it will stay checked when unselecting a module that depends on it.
        If we select a module with dependencies, the dependencies will be selected as well and the checkboxes will be disabled.

        Args:
            state (int): The state of the checkbox
            module_name (str): The name of the module
        """
        logger.debug(f"Checkbox {module_name} changed to {state}")

        is_checked = state == 2  # True if the checkbox is checked, False if unchecked.
        dependencies = self.get_dependencies(module_name)
        logger.debug(f"Dependencies of {module_name}: {dependencies}")

        def handle_dependency_action(dependency_name, check_state):
            if dependency_name in self.checkboxes:
                logger.debug(f"Setting dependency {dependency_name} to {check_state}")

                required_state = check_state

                if not required_state:
                    module_checkbox = self.checkboxes[dependency_name]
                    if module_checkbox.property("manually_checked") or any(
                        self.checkboxes[other_module["name"]].isChecked()
                        for other_module in self.modules
                        if dependency_name in other_module.get("dependencies", [])
                    ):
                        logger.debug(
                            f"Manually checked: {dependency_name} with state {module_checkbox.property('manually_checked')}"
                        )
                        required_state = True

                self.checkboxes[dependency_name].setChecked(required_state)

                # Determine whether to enable or disable based on the installed modules
                # and other module dependencies.
                can_enable = dependency_name not in self.installed_modules and not any(
                    self.checkboxes[other_module["name"]].isChecked()
                    for other_module in self.modules
                    if dependency_name in other_module.get("dependencies", [])
                )

                self.checkboxes[dependency_name].setEnabled(can_enable)

        # Apply appropriate logic based on the state.
        for dependency in dependencies:
            handle_dependency_action(dependency, is_checked)

    def on_checkbox_clicked(self, state: int, module_name: str) -> None:
        """Save if a checkbox was manually clicked and what state it was set to.

        Args:
            state (int): The state of the checkbox
            module_name (str): The name of the module
        """
        logger.debug(f"Checkbox {module_name} was clicked with state {state}")
        self.checkboxes[module_name].setProperty("manually_checked", state)
        logger.debug(
            f"Checkbox manually enabled: {self.checkboxes[module_name].property('manually_checked')}"
        )

    def get_dependencies(self, module_name: str) -> list:
        """Get the dependencies of a module.

        Args:
            module_name (str): The name of the module

        Returns:
            list: The dependencies of the module
        """
        for module in self.modules:
            try:
                if module["name"] == module_name:
                    return module["dependencies"]
            except KeyError:
                logger.debug("Module has no dependencies")
        return []


class InstallPage(QWizardPage):
    """The installation page of the wizard.

    This page is shown while the modules are installed.
    """

    def __init__(self, selection_page):
        """Initializes the InstallPage."""
        super().__init__()

        self.selection_page = selection_page

        self.setTitle("Installing NQRduck modules")
        self.setSubTitle("The following modules will be installed:")


    def initializePage(self) -> None:
        """Generate the installation widgets for the modules."""
        logger.debug("Initializing InstallPage")
        layout = QVBoxLayout()
        self.setLayout(layout)

        install_modules = self.get_install_modules()
        logger.debug(f"Modules to install: {install_modules}")
        for module in install_modules:
            label = QLabel(module)
            layout.addWidget(label)

    def cleanupPage(self) -> None:
        logger.debug("Cleaning up InstallPage")
        for child in self.children():
            child.deleteLater()


    def get_install_modules(self) -> list:
        """Returns the modules that are selected for installation  minus the already installed modules.

        Returns:
            list: The modules that are selected for installation
        """
        install_modules = []
        installed_modules = self.selection_page.installed_modules

        for key, value in self.selection_page.checkboxes.items():
            logger.debug(f"Checking {key} with state {value.isChecked()}")
            if value.isChecked() and key not in installed_modules:
                install_modules.append(key)

        return install_modules

    def install_modules(self):
        """Install the selected modules."""
        pass

    class InstallThread(QThread):
        def __init__(self, install_modules):
            super().__init__()
            self.install_modules = install_modules

        def run(self):
            for module in self.install_modules:
                logger.debug(f"Installing {module}")
                os.system(f"pip install {module}")
                logger.debug(f"Installed {module}")


class FinishPage(QWizardPage):
    def __init__(self):
        super().__init__()

        self.setTitle("Installation complete")
        self.setSubTitle("The installation of NQRduck modules is complete.")

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("The installation of NQRduck modules is complete.")
        layout.addWidget(label)

        self.button = QPushButton("Finish")
        self.button.clicked.connect(self.finish)
        layout.addWidget(self.button)

    def finish(self):
        self.wizard().accept()
