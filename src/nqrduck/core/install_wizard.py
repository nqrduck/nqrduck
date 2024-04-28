"""A wizard to install different NQRduck modules."""

from PyQt6.QtWidgets import (
    QWizard,
    QWizardPage,
    QFormLayout,
    QLineEdit,
    QCheckBox,
    QFileDialog,
    QLabel,
    QPushButton,
)

class DuckWizard(QWizard):
    def __init__(self):
        super().__init__()

        self.addPage(WelcomePage())
        self.addPage(InstallPage())
        self.addPage(FinishPage())


class WelcomePage(QWizardPage):
    def __init__(self):
        super().__init__()

        self.setTitle("Welcome to NQRduck")
        self.setSubTitle("This wizard will help you install NQRduck modules.")
        self.setPixmap(QWizard.WizardPixmap.LogoPixmap, QPixmap("nqrduck.png"))

        label = QLabel("Welcome to the NQRduck installer.")
        label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

class InstallPage(QWizardPage):
    def __init__(self):
        super().__init__()

        self.setTitle("Install NQRduck modules")
        self.setSubTitle("Please specify the modules you want to install.")

        layout = QFormLayout()
        self.setLayout(layout)

        self.module1 = QCheckBox("Module 1")
        layout.addRow(self.module1)

        self.module2 = QCheckBox("Module 2")
        layout.addRow(self.module2)

        self.module3 = QCheckBox("Module 3")
        layout.addRow(self.module3)