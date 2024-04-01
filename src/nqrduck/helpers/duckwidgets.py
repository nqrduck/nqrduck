"""Provides a variety of different widgets for the  NQRduck GUI."""
import logging

from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import pyqtSlot, pyqtSignal

from .validators import DuckFloatValidator, DuckIntValidator

logger = logging.getLogger(__name__)

class DuckEdit(QLineEdit):
    """A QLineEdit widget for floats and integers.

    By setting the validator attribute, the widget can be used for integers or floats.

    Args:
        parent (QWidget): The parent widget.

    Attributes:
        validator (DuckFloatValidator or DuckIntValidator): The validator for the input.

    Signals:
        state_updated: Signal emitted when the state of the widget changes. It emits a bool and a str the bool indicates if the input is valid and the str is the input.
    """

    state_updated = pyqtSignal(bool, str)
    validator = None

    def __init__(self, parent=None):
        """Initializes the DuckEdit."""
        super().__init__(parent)
        self.textChanged.connect(self.on_text_changed)

    @pyqtSlot(str)
    def on_text_changed(self, text):
        """Slot that is called when the text of the QLineEdit changes.

        Args:
            text (str): The text of the QLineEdit.
        """
        if self.validator is None:
            logger.info("No validator set for DuckEdit")
            return

        state, _, _ = self.validator.validate(text, 0)
        if state == self.validator.State.Acceptable:
            self.setStyleSheet("")
            self.state_updated.emit(True, text)
        elif state == self.validator.State.Intermediate:
            self.setStyleSheet("background-color: #FFD700")
            self.state_updated.emit(False, text)
        else:
            self.setStyleSheet("background-color: #FFB6C1")
            self.state_updated.emit(False, text)


class DuckIntEdit(DuckEdit):
    """A QLineEdit widget for integers.

    This widget only accepts integers as input.
    Additionally, it changes its appearance when the input is invalid.

    Args:
        parent (QWidget): The parent widget.
        min_value (int): The minimum value that is accepted.
        max_value (int): The maximum value that is accepted.

    Attributes:
        validator (DuckIntValidator): The validator for the input.
    """

    def __init__(self, parent=None, min_value=None, max_value=None):
        """Initializes the DuckIntEdit."""
        super().__init__(parent)
        self.validator = DuckIntValidator(self, min_value, max_value)

    def set_min_value(self, min_value):
        """Sets the minimum value that is accepted.

        Args:
            min_value (int): The minimum value.
        """
        self.validator.min_value = min_value

    def set_max_value(self, max_value):
        """Sets the maximum value that is accepted.

        Args:
            max_value (int): The maximum value.
        """
        self.validator.max_value = max_value

class DuckFloatEdit(DuckEdit):
    """A QLineEdit widget for floats.

    This widget only accepts floats as input.
    Additionally, it changes its appearance when the input is invalid.

    Args:
        parent (QWidget): The parent widget.
        min_value (float): The minimum value that is accepted.
        max_value (float): The maximum value that is accepted.

    Attributes:
        validator (DuckFloatValidator): The validator for the input.
    """

    def __init__(self, parent=None, min_value=None, max_value=None):
        """Initializes the DuckFloatEdit."""
        super().__init__(parent)
        self.validator = DuckFloatValidator(self, min_value, max_value)

    def set_min_value(self, min_value):
        """Sets the minimum value that is accepted.

        Use this when creating the DuckFloatWidgets with the Qtdesigner.

        Args:
            min_value (float): The minimum value.
        """
        self.validator.min_value = min_value

    def set_max_value(self, max_value):
        """Sets the maximum value that is accepted.

        Use this when creating the DuckFloatWidgets with the Qtdesigner.

        Args:
            max_value (float): The maximum value.
        """
        self.validator.max_value = max_value
        
