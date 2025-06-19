"""A module that allows for easy creation of form views in the NQRduck framework."""

import logging
import functools
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QPushButton,
    QCheckBox,
    QComboBox,
    QDialogButtonBox,
    QGroupBox,
    QFormLayout,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)
from quackseq.functions import Function
from .duckwidgets import DuckSpinBox, DuckFloatEdit
from ..helpers.signalprocessing import SignalProcessing as sp
from ..contrib.mplwidget import MplWidget

logger = logging.getLogger(__name__)


class DuckFormField(QWidget):
    """The base class for all Form Fields."""

    def __init__(self, text: str, tooltip: str, parent=None, vertical=False) -> None:
        """Initializes a generic form field.

        Args:
            text (str): The text of the form field.
            tooltip (str): The tooltip of the form field.
            parent ([type], optional): The parent widget. Defaults to None.
            vertical (bool, optional): Whether the layout should be vertical. Defaults to False.
        """
        super().__init__(parent=parent)
        self.setParent(parent)
        if vertical:
            self.layout = QVBoxLayout()
        else:
            self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        if text:
            self.label = QLabel(f"{text}:")
            # Make the label bold
            self.label.setStyleSheet("font-weight: bold;")
            if tooltip:
                self.label.setToolTip(tooltip)

            self.layout.addWidget(self.label)


    def return_value(self):
        """This method should return the value of the form field."""
        raise NotImplementedError

class DuckTableField(DuckFormField):
    """A form field for tables.
    
    Every table has different options for columns. The rows are the values of the according columns.
    """
    def __init__(self, text: str, tooltip: str, parent=None, vertical=False) -> None:
        super().__init__(text, tooltip, parent, vertical)
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.fields = {}
    
    def add_column(self, option : "Option", fields: list[DuckFormField]):
        """Adds a column to the table.

        Args:
            column_name (str): The name of the column.
            fields (DuckFormField): The field to add.
        """
        column_name = option.name
        logger.debug("Adding column %s to table", column_name)
        logger.debug("Fields: %s", fields)
        self.table.setColumnCount(self.table.columnCount() + 1)
        self.table.setRowCount(len(fields))
        self.table.setHorizontalHeaderLabels([field.label.text() for field in fields])
        self.fields[option] = fields

        for i, field in enumerate(fields):
            logger.debug("Adding field %s to column %s", field, column_name)
            self.table.setCellWidget(i, self.table.columnCount() - 1, field.widget)

        # Resize everything
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def return_value(self):
        """Returns the values of the table."""
        values = []
        for key, value in self.fields.items():
            values.append([field.return_value() for field in value])

        logger.debug("Returning values: %s", values)

        return values

class DuckFormFloatField(DuckFormField):
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
        self.widget = DuckSpinBox(
            min_value=min_value, max_value=max_value, slider=slider, double_box=True
        )
        self.widget.set_value(default)
        # The layout is already set in the parent class
        self.layout.addWidget(self.widget)
        self.layout.addStretch(1)

    def return_value(self):
        """Returns the value of the float field.

        Returns:
            float: The value of the float field.
        """
        return self.widget.value()


class DuckFormIntField(DuckFormField):
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
        self.widget = DuckSpinBox(
            min_value=min_value, max_value=max_value, slider=slider, double_box=False
        )
        # The layout is already set in the parent class
        self.layout.addWidget(self.widget)
        self.layout.addStretch(1)

    def return_value(self):
        """Returns the value of the integer field.

        Returns:
            int: The value of the integer field.
        """
        return self.widget.value()


class DuckFormFunctionSelectionField(DuckFormField):
    """A form field for selecting functions."""

    def __init__(
        self,
        text: str,
        tooltip: str,
        functions,
        duration: float,
        default_function: int = 0,
        view_mode: str = "both",
        mode_selection: int = 0,
        parent=None,
    ) -> None:
        """Initializes a function selection field.

        Args:
            text (str): The text of the field.
            tooltip (str): The tooltip of the field.
            functions (list): The list of functions that can be selected.
            duration (float): The duration of the function.
            default_function (int, optional): The default function. Defaults to 0.
            view_mode (str, optional): The view mode of the function. Defaults to "both". Can be "time", "frequency" or "both".
            mode_selection (int, optional): Whether the mode can be selected. 0 is disabled, 1 is enabled without option for both and 2 is enabled with option for both. Defaults to 0.
            parent ([type], optional): The parent widget. Defaults to None.
        """
        super().__init__(text, tooltip, parent=parent, vertical=True)
        self.parent = parent

        self.functions = functions
        self.selected_function = functions[default_function]

        self.duration = float(duration)

        self.view_mode = view_mode
        self.mode_selection = mode_selection

        self.form_layout = QVBoxLayout()

        if mode_selection:
            # Add mode selection
            mode_layout = QHBoxLayout()
            mode_label = QLabel("View mode:")
            self.widget = QComboBox()
            if mode_selection == 1:
                self.widget.addItems(["Time", "Frequency"])
            else:
                self.widget.addItems(["Time", "Frequency", "Both"])
            self.widget.setCurrentText(self.view_mode.capitalize())
            self.widget.currentTextChanged.connect(self.update_active_function)

            mode_layout.addWidget(mode_label)
            mode_layout.addWidget(self.widget)
            mode_layout.addStretch(1)
            self.form_layout.addLayout(mode_layout)

        inner_layout = QHBoxLayout()
        for function in self.functions:
            logger.debug("Adding button for function %s", function.name)
            button = QPushButton(function.name)
            button.clicked.connect(
                functools.partial(self.on_functionbutton_clicked, function=function)
            )
            inner_layout.addWidget(button)

        self.form_layout.addLayout(inner_layout)

        # The layout is already set in the parent class
        self.layout.addLayout(self.form_layout)

        # Add Advanced settings button
        self.advanced_settings_button = QPushButton("Show Advanced settings")
        self.advanced_settings_button.clicked.connect(
            self.on_advanced_settings_button_clicked
        )
        self.form_layout.addWidget(self.advanced_settings_button)

        # Add advanced settings widget
        self.advanced_settings = QGroupBox("Advanced Settings")
        self.advanced_settings.setHidden(True)
        self.advanced_settings_layout = QFormLayout()
        self.advanced_settings.setLayout(self.advanced_settings_layout)
        self.form_layout.addWidget(self.advanced_settings)

        # Add the advanced settings
        # Advanced settings are  resolution, start_x = -1, end_x and the expr of the function_option.value
        resolution_layout = QHBoxLayout()
        resolution_label = QLabel("Resolution:")
        self.resolution_lineedit = DuckFloatEdit(str(self.selected_function.resolution))
        resolution_layout.addWidget(resolution_label)
        resolution_layout.addWidget(self.resolution_lineedit)
        resolution_layout.addStretch(1)
        self.advanced_settings_layout.addRow(resolution_label, resolution_layout)

        start_x_layout = QHBoxLayout()
        start_x_label = QLabel("Start x:")
        self.start_x_lineedit = DuckFloatEdit(str(self.selected_function.start_x))
        start_x_layout.addWidget(start_x_label)
        start_x_layout.addWidget(self.start_x_lineedit)
        start_x_layout.addStretch(1)
        self.advanced_settings_layout.addRow(start_x_label, start_x_layout)

        end_x_layout = QHBoxLayout()
        end_x_label = QLabel("End x:")
        self.end_x_lineedit = DuckFloatEdit(str(self.selected_function.end_x))
        end_x_layout.addWidget(end_x_label)
        end_x_layout.addWidget(self.end_x_lineedit)
        end_x_layout.addStretch(1)
        self.advanced_settings_layout.addRow(end_x_label, end_x_layout)

        expr_layout = QHBoxLayout()
        expr_label = QLabel("Expression:")
        self.expr_lineedit = DuckFloatEdit(str(self.selected_function.expr))
        expr_layout.addWidget(expr_label)
        expr_layout.addWidget(self.expr_lineedit)
        expr_layout.addStretch(1)
        self.advanced_settings_layout.addRow(expr_label, expr_layout)

        # Add buttton for replotting of the active function with the new parameters
        self.replot_button = QPushButton("Replot")
        self.replot_button.clicked.connect(self.on_replot_button_clicked)
        self.form_layout.addWidget(self.replot_button)

        # Display the active function
        self.load_active_function()

    @pyqtSlot()
    def on_replot_button_clicked(self) -> None:
        """This function is called when the replot button is clicked.

        It will update the parameters of the function and replots the function.
        """
        logger.debug("Replot button clicked")
        # Update the resolution, start_x, end_x and expr lineedits
        self.selected_function.resolution = self.resolution_lineedit.text()
        self.selected_function.start_x = self.start_x_lineedit.text()
        self.selected_function.end_x = self.end_x_lineedit.text()
        try:
            self.selected_function.expr = self.expr_lineedit.text()
        except SyntaxError:
            logger.debug("Invalid expression: %s", self.expr_lineedit.text())
            self.expr_lineedit.setText(str(self.selected_function.expr))
            # Create message box that tells the user that the expression is invalid
            self.create_message_box(
                "Invalid expression",
                "The expression you entered is invalid. Please enter a valid expression.",
            )

        self.update_active_function()

    @pyqtSlot()
    def on_advanced_settings_button_clicked(self) -> None:
        """This function is called when the advanced settings button is clicked.

        It will show or hide the advanced settings.
        """
        if self.advanced_settings.isHidden():
            self.advanced_settings.setHidden(False)
            self.advanced_settings_button.setText("Hide Advanced Settings")
        else:
            self.advanced_settings.setHidden(True)
            self.advanced_settings_button.setText("Show Advanced Settings")

    @pyqtSlot()
    def on_functionbutton_clicked(self, function) -> None:
        """This function is called when a function button is clicked.

        It will update the function_option.value to the function that was clicked.
        """
        logger.debug(
            f"Button for function {function.name} clicked, instance id: {id(self)}"
        )
        for f in self.functions:
            if f.name == function.name:
                self.selected_function = f

        self.update_active_function()

    def delete_active_function(self) -> None:
        """This function is called when the active function is deleted.

        It will remove the active function from the layout.
        """
        # Remove the plotter with object name "plotter" from the layout
        for i in reversed(range(self.form_layout.count())):
            item = self.form_layout.itemAt(i)
            if item.widget() and item.widget().objectName() == "active_function":
                item.widget().deleteLater()
                break

    def load_active_function(self) -> None:
        """This function is called when the active function is loaded.

        It will add the active function to the layout.
        """
        # New QWidget for the active function
        active_function_Widget = QWidget()
        active_function_Widget.setObjectName("active_function")

        function_layout = QVBoxLayout()

        plot_layout = QHBoxLayout()

        if self.mode_selection:
            self.view_mode = self.widget.currentText().lower()

        if self.view_mode == "time" or self.view_mode == "both":
            # Add plot for time domain
            time_domain_layout = QVBoxLayout()
            time_domain_label = QLabel("Time domain:")
            time_domain_layout.addWidget(time_domain_label)
            plot = self.time_domain_plot(self.selected_function, self.duration)
            time_domain_layout.addWidget(plot)
            plot_layout.addLayout(time_domain_layout)

        if self.view_mode == "frequency" or self.view_mode == "both":
            # Add plot for frequency domain
            frequency_domain_layout = QVBoxLayout()
            frequency_domain_label = QLabel("Frequency domain:")
            frequency_domain_layout.addWidget(frequency_domain_label)
            plot = self.frequency_domain_plot(self.selected_function, self.duration)
            frequency_domain_layout.addWidget(plot)
            plot_layout.addLayout(frequency_domain_layout)

        function_layout.addLayout(plot_layout)

        parameter_layout = QFormLayout()
        parameter_label = QLabel("Parameters:")
        parameter_layout.addRow(parameter_label)
        for parameter in self.selected_function.parameters:
            parameter_label = QLabel(parameter.name)
            parameter_lineedit = DuckFloatEdit(str(parameter.value))
            # Add the parameter_lineedit editingFinished signal to the parameter.set_value slot
            parameter_lineedit.editingFinished.connect(
                lambda: parameter.set_value(parameter_lineedit.text())
            )

            # Create a QHBoxLayout
            hbox = QHBoxLayout()

            # Add your QLineEdit and a stretch to the QHBoxLayout
            hbox.addWidget(parameter_lineedit)
            hbox.addStretch(1)

            # Use addRow() method to add label and the QHBoxLayout next to each other
            parameter_layout.addRow(parameter_label, hbox)

        function_layout.addLayout(parameter_layout)
        function_layout.addStretch(1)
        active_function_Widget.setLayout(function_layout)
        self.form_layout.addWidget(active_function_Widget)

        # Update the resolution, start_x, end_x and expr lineedits
        self.resolution_lineedit.setText(str(self.selected_function.resolution))
        self.start_x_lineedit.setText(str(self.selected_function.start_x))
        self.end_x_lineedit.setText(str(self.selected_function.end_x))
        self.expr_lineedit.setText(str(self.selected_function.expr))

    def update_active_function(self) -> None:
        """This function is called when the active function is updated.

        It will update the active function with the new parameters.
        """
        self.delete_active_function()
        self.load_active_function()

    def create_message_box(self, message: str, information: str) -> None:
        """Creates a message box with the given message and information and shows it.

        Args:
            message (str): The message to be shown in the message box
            information (str): The information to be shown in the message box
        """
        msg = QMessageBox(parent=self.parent)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setInformativeText(information)
        msg.setWindowTitle("Warning")
        msg.exec()

    def return_value(self):
        """Returns the selected function.

        Returns:
            Function: The selected function.
        """
        logger.debug("Returning selected function: %s", self.selected_function)
        if self.mode_selection:
            return self.selected_function, self.widget.currentText().lower()

        return self.selected_function
    
    def frequency_domain_plot(self, function : Function, pulse_length: float) -> MplWidget:
        """Plots the frequency domain of the function for the given pulse length.

        Args:
            function (Function): The function to plot.
            pulse_length (float): The pulse length in seconds.

        Returns:
            MplWidget: The matplotlib widget containing the plot.
        """
        mpl_widget = MplWidget()
        td = function.get_time_points(pulse_length)
        yd = function.evaluate(pulse_length)
        xdf, ydf = sp.fft(td, yd)
        mpl_widget.canvas.ax.plot(xdf, abs(ydf))
        mpl_widget.canvas.ax.set_xlabel("Frequency in Hz")
        mpl_widget.canvas.ax.set_ylabel("Magnitude")
        mpl_widget.canvas.ax.grid(True)
        return mpl_widget

    def time_domain_plot(self, function : Function, pulse_length: float) -> MplWidget:
        """Plots the time domain of the function for the given pulse length.

        Args:
            function (Function): The function to plot.
            pulse_length (float): The pulse length in seconds.

        Returns:
            MplWidget: The matplotlib widget containing the plot.
        """
        mpl_widget = MplWidget()
        td = function.get_time_points(pulse_length)
        mpl_widget.canvas.ax.plot(td, abs(function.evaluate(pulse_length)))
        mpl_widget.canvas.ax.set_xlabel("Time in s")
        mpl_widget.canvas.ax.set_ylabel("Magnitude")
        mpl_widget.canvas.ax.grid(True)
        return mpl_widget


class DuckFormDropdownField(DuckFormField):
    """A form field for dropdowns."""

    def __init__(
        self, text: str, tooltip: str, options: dict, default_option: int = 0
    ) -> None:
        """Initializes a dropdown field.

        Args:
            text (str): The text of the field.
            tooltip (str): The tooltip of the field.
            options (dict): The options that can be selected.
            default_option (int, optional): The default option. Defaults to 0.
        """
        super().__init__(text, tooltip)
        self.options = options
        self.widget = QComboBox()
        self.widget.addItems(options.keys())
        self.widget.setCurrentIndex(default_option)
        self.layout.addWidget(self.widget)

    def return_value(self):
        """Returns the selected option."""
        return [self.widget.currentText(), self.options[self.widget.currentText()]]


class DuckFormCheckboxField(DuckFormField):
    """A form field for checkboxes."""

    def __init__(self, text: str, tooltip: str, default: bool = False) -> None:
        """Initializes a checkbox field.

        Args:
            text (str): The text of the field.
            tooltip (str): The tooltip of the field.
            default (bool, optional): The default value of the checkbox. Defaults to False.
        """
        super().__init__(text, tooltip)
        self.widget = QCheckBox()
        self.widget.setChecked(default)
        self.layout.addWidget(self.widget)

    def return_value(self):
        """Returns the value of the checkbox."""
        return self.widget.isChecked()


class DuckFormBuilder(QDialog):
    """A class that allows for easy creation of forms.

    This class is used to create forms with different types of fields.

    Attributes:
        fields (list): The list of fields in the form.
    """

    def __init__(self, title: str, description: str = None, parent=None) -> None:
        """Initializes the form builder.

        Args:
            title (str): The title of the form.
            description (str, optional): A description of the form. Defaults to None.
            parent ([type], optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.parent = parent

        self.fields = []

        self.setWindowTitle("Options")

        self.layout = QVBoxLayout(self)

        self.form_layout = QVBoxLayout()

        self.numeric_wrap_layout = QHBoxLayout()
        self.numeric_layout = QFormLayout()
        self.numeric_layout.setHorizontalSpacing(30)
        self.numeric_wrap_layout.addLayout(self.numeric_layout)
        self.numeric_wrap_layout.addStretch(1)

        self.label = QLabel(f"Change options for: {title}")
        self.layout.addWidget(self.label)

        self.layout.addLayout(self.numeric_wrap_layout)
        self.layout.addLayout(self.form_layout)

        self.button_layout = QHBoxLayout()

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.button_layout.addWidget(self.buttons)

        self.layout.addLayout(self.button_layout)

    def add_field(self, field: DuckFormField):
        """Adds a field to the form.

        Args:
            field (DuckFormField): The field to add.
        """
        self.fields.append(field)
        if isinstance(field, DuckFormFloatField) or isinstance(field, DuckFormIntField):
            self.numeric_layout.addRow(field.label, field.widget)
        else:
            self.form_layout.addWidget(field)

        # Resize the window to fit the new field
        self.resize(self.sizeHint())

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
        return [field.return_value() for field in self.fields]
