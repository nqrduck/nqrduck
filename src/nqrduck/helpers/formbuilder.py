"""A module that allows for easy creation of form views in the NQRduck framework."""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QPushButton,
    QCheckBox,
    QComboBox,
)
from .duckwidgets import DuckSpinBox


class DuckFormField(QWidget):
    """The base class for all Form Fields."""

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

    def return_value(self):
        """This method should return the value of the form field."""
        raise NotImplementedError


class DuckFloatField(DuckFormField):
    """A form field for float values."""

    def __init__(
        self,
        text: str,
        tooltip: str,
        default: float,
        min_value: float = None,
        max_value: float = None,
        slider=False,
    ) -> None:
        """Initializes a float field.

        Args:
            text (str): The text of the field.
            tooltip (str): The tooltip of the field.
            default (float): The default value of the field.
            min_value (float, optional): The minimum value of the field. Defaults to None.
            max_value (float, optional): The maximum value of the field. Defaults to None.
            slider (bool, optional): Whether to use a slider. Defaults to False.
        """
        super().__init__(text, tooltip)
        self.float_edit = DuckSpinBox(
            min_value=min_value, max_value=max_value, slider=slider, double_box=True
        )
        self.float_edit.set_value(default)
        # The layout is already set in the parent class
        self.layout.addWidget(self.float_edit)

    def return_value(self):
        """Returns the value of the float field.

        Returns:
            float: The value of the float field.
        """
        return self.float_edit.value()


class DuckIntField(DuckFormField):
    """A form field for integer values."""

    def __init__(
        self,
        text: str,
        tooltip: str,
        default: int,
        min_value: int = None,
        max_value: int = None,
        slider=False,
    ) -> None:
        """Initializes an integer field.

        Args:
            text (str): The text of the field.
            tooltip (str): The tooltip of the field.
            default (int): The default value of the field.
            min_value (int, optional): The minimum value of the field. Defaults to None.
            max_value (int, optional): The maximum value of the field. Defaults to None.
            slider (bool, optional): Whether to use a slider. Defaults to False.
        """
        super().__init__(text, tooltip)
        self.int_edit = DuckSpinBox(
            min_value=min_value, max_value=max_value, slider=slider, double_box=False
        )
        # The layout is already set in the parent class
        self.layout.addWidget(self.int_edit)

    def return_value(self):
        """Returns the value of the integer field.
        
        Returns:
            int: The value of the integer field.
        """
        return self.int_edit.value()


class DuckFormFunctionSelectionField(DuckFormField):
    """A form field for selecting functions."""

    def __init__(
        self, text: str, tooltip: str, functions, default_function: int = 0
    ) -> None:
        """Initializes a function selection field.

        Args:
            text (str): The text of the field.
            tooltip (str): The tooltip of the field.
            functions (list): The list of functions that can be selected.
            default_function (int, optional): The default function. Defaults to 0.
        """
        super().__init__(text, tooltip)

    def return_value(self):
        """Returns the selected function.

        Returns:
            Function: The selected function.
        """
        pass


class DuckFormDropdownField(DuckFormField):
    """A form field for dropdowns."""
    def __init__(
        self, text: str, tooltip: str, options: str, default_option: int = 0
    ) -> None:
        """Initializes a dropdown field.
        
        Args:
            text (str): The text of the field.
            tooltip (str): The tooltip of the field.
            options (str): The options that can be selected.
            default_option (int, optional): The default option. Defaults to 0.
        """
        super().__init__(text, tooltip)
        self.dropdown = QComboBox()
        self.dropdown.addItems(options)
        self.dropdown.setCurrentIndex(default_option)
        self.layout.addWidget(self.dropdown)

    def return_value(self):
        """Returns the selected option."""
        self.dropdown.currentText()


class DuckFormCheckboxField(DuckFormField):
    """A form field for checkboxes."""
    def __init__(self, text: str, tooltip: str, default: bool = False) -> None:
        """Initializes a checkbox field.
        
        Args:
            text (str): The text of the field.
            tooltip (str): The tooltip of the field.
            default (bool, optional): The default value of the checkbox. Defaults to False.
        """
        super().__init(text, tooltip)
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(default)
        self.layout.addWidget(self.checkbox)

    def return_value(self):
        """Returns the value of the checkbox."""
        return self.checkbox.isChecked()


class DuckFormBuilder(QDialog):
    """A class that allows for easy creation of forms.
    
    This class is used to create forms with different types of fields.
    
    Attributes:
        fields (list): The list of fields in the form.
    """
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
        """Adds a field to the form.
        
        Args:
            field (DuckFormField): The field to add.
        """
        field.on_state_changed.connect(self.on_state_changed)
        self.fields.append(field)
        self.main_layout.addWidget(field)

    def on_state_changed(self, state: bool, text: str):
        """This method is called when the state of a field changes.
        
        Args:
            state (bool): The state of the field.
            text (str): The text of the field.
        """
        # Get the sender of the signal
        pass

    def get_values(self):
        """Returns the values of the form fields."""
        pass
