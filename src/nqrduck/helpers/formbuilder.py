"""A module that allows for easy creation of form views in the NQRduck framework."""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QPushButton,
)
from .duckwidgets import DuckSpinBox
# Brainstorming:
# - We can specify different types of form fields
#    - Numerical (with min/max values and input validation)
#    - Function Selection (with time and frequency domain options)
#    - Dropdowns
#    - Checkboxes (Boolean)
#    - ...
# So the user specifies what type of form they want - then it can be generated for them.
# When the user  finishes the form one can easily retrieve the values from the different fields.
# Ideally the formbuilder re-uses the duckwidgets to create the form fields.
# Optionally a tooltip can be added to each field to provide additional information.

# The view generation needs to be moved from the pulseprogrammer module to this module.
# The functions should not only be defined inside the spectrometer module.


class DuckFormField(QWidget):
    def __init__(self, text: str, tooltip: str) -> None:
        """Initializes a generic form field.

        Args:
            text (str): The text of the form field.
            tooltip (str): The tooltip of the form field.
        """
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(text)
        layout.addWidget(self.label)


class DuckFloatField(DuckFormField):
    def __init__(
        self,
        text: str,
        tooltip: str,
        default: float,
        min_value: float = None,
        max_value: float = None,
        slider=False,
    ) -> None:
        super().__init__(text, tooltip)
        self.float_edit = DuckSpinBox(
            min_value=min_value, max_value=max_value, slider=slider, double_box=True
        )
        # The layout is already set in the parent class
        self.layout.addWidget(self.float_edit)


class DuckIntField(DuckFormField):
    def __init__(
        self,
        text: str,
        tooltip: str,
        default: int,
        min_value: int = None,
        max_value: int = None,
        slider=False,
    ) -> None:
        super().__init__(text, tooltip)
        self.int_edit = DuckSpinBox(
            min_value=min_value, max_value=max_value, slider=slider, double_box=False
        )
        # The layout is already set in the parent class
        self.layout.addWidget(self.int_edit)


class DuckFormFunctionSelectionField(DuckFormField):
    def __init__(
        self, text: str, tooltip: str, functions, default_function: int = 0
    ) -> None:
        super().__init__(text, tooltip)


class DuckFormDropdownField(DuckFormField):
    def __init__(
        self, text: str, tooltip: str, options: str, default_option: int = 0
    ) -> None:
        super().__init__(text, tooltip)


class DuckFormCheckboxField(DuckFormField):
    def __init__(self, text: str, tooltip: str, default: bool = False) -> None:
        super().__init(text, tooltip)


class DuckFormBuilder(QDialog):
    fields = []

    def __init__(self, title: str, description: str = None, parent=None) -> None:
        """Initializes the form builder.

        Args:
            title (str): The title of the form.
            description (str, optional): A description of the form. Defaults to None.
            parent ([type], optional): The parent widget. Defaults to None.
        """
        super().__init__(parent=parent)
        self.setParent(parent)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.setWindowTitle(title)

        if description:
            self.description_label = QLabel(description)
            self.main_layout.addWidget(self.description_label)

        # Ok and cancel buttons
        self.ok_button = QPushButton("Ok")
        self.cancel_button = QPushButton("Cancel")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def add_field(self, field: DuckFormField):
        self.fields.append(field)
        self.main_layout.addWidget(field)

    def get_values(self):
        pass
