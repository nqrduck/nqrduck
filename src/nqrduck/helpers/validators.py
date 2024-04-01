"""Helper used for validating input."""

from PyQt6.QtCore import QObject
from PyQt6.QtGui import QValidator


class DuckIntValidator(QValidator):
    """A validator for integers. Accepts only integers.

    This is used to validate the input of the QLineEdit widgets.

    Args:
        parent (QObject): The parent object
        min_value (int): The minimum value that is accepted
        max_value (int): The maximum value that is accepted
    """

    def __init__(
        self, parent: QObject, min_value: int = None, max_value: int = None
    ) -> None:
        """Initializes the DuckIntValidator."""
        super().__init__(parent)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value, position):
        """Validates the input value.

        Args:
            value (str): The input value
            position (int): The position of the cursor

        Returns:
            QValidator.State: The state of the input value
        """
        try:
            f_value = float(value)
            assert f_value.is_integer()
            if self.min_value is not None and f_value < self.min_value:
                return QValidator.State.Invalid
            if self.max_value is not None and f_value > self.max_value:
                return QValidator.State.Invalid

            return QValidator.State.Acceptable

        except ValueError:
            if value.endswith("e"):
                return QValidator.State.Intermediate
            return QValidator.State.Invalid


class DuckFloatValidator(QValidator):
    """A validator for floats. Accepts only floats.

    This is used to validate the input of the QLineEdit widgets.
    It also replaces commas with dots.

    Args:
        parent (QObject): The parent object
        min_value (float): The minimum value that is accepted
        max_value (float): The maximum value that is accepted
    """

    def __init__(
        self, parent: QObject, min_value: float = None, max_value: float = None
    ) -> None:
        """Initializes the DuckFloatValidator."""
        super().__init__(parent)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: str, position: int):
        """Validates the input value.

        Args:
            value (str): The input value
            position (int): The position of the cursor
        """
        try:
            f_value = float(value)
            if self.min_value is not None and f_value < self.min_value:
                return QValidator.State.Invalid
            if self.max_value is not None and f_value > self.max_value:
                return QValidator.State.Invalid

            if value.endswith("."):
                return QValidator.State.Intermediate

            return QValidator.State.Acceptable

        except ValueError:
            if value.endswith("e"):
                return QValidator.State.Intermediate

            return QValidator.State.Invalid

    def fixup(self, value: str):
        """Replaces commas with dots.

        Args:
            value (str): The input value

        Returns:
            str: The fixed value
        """
        return value.replace(",", ".")
