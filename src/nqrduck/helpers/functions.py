"""A module that contains functions that can be used in various modules. This used to be part of the nqrduck-spectrometer module."""

from __future__ import annotations
import logging
import numpy as np
import sympy
from nqrduck.contrib.mplwidget import MplWidget
from nqrduck.helpers.signalprocessing import SignalProcessing as sp


logger = logging.getLogger(__name__)


class Function:
    """A function that can be used as a pulse parameter.

    This class is the base class for all functions that can be used as pulse parameters. Functions can be used for pulse shapes, for example.

    Args:
        expr (str | sympy.Expr): The expression of the function.

    Attributes:
        name (str): The name of the function.
        parameters (list): The parameters of the function.
        expr (sympy.Expr): The sympy expression of the function.
        resolution (float): The resolution of the function in seconds.
        start_x (float): The x value where the evalution of the function starts.
        end_x (float): The x value where the evalution of the function ends.
    """

    name: str
    parameters: list
    expression: str | sympy.Expr
    resolution: float
    start_x: float
    end_x: float

    subclasses = []

    def __init_subclass__(cls, **kwargs):
        """Registers the subclass."""
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def __init__(self, expr) -> None:
        """Initializes the function."""
        self.parameters = []
        self.expr = expr
        self.resolution = 1 / 30.72e6
        self.start_x = -1
        self.end_x = 1

    def get_time_points(self, pulse_length: float) -> np.ndarray:
        """Returns the time domain points for the function with the given pulse length.

        Args:
            pulse_length (float): The pulse length in seconds.

        Returns:
            np.ndarray: The time domain points.
        """
        # Get the time domain points
        n = int(pulse_length / self.resolution)
        t = np.linspace(0, float(pulse_length), n)
        return t

    def evaluate(self, pulse_length: float, resolution: float = None) -> np.ndarray:
        """Evaluates the function for the given pulse length.

        Args:
            pulse_length (float): The pulse length in seconds.
            resolution (float, optional): The resolution of the function in seconds. Defaults to None.

        Returns:
            np.ndarray: The evaluated function.
        """
        if resolution is None:
            resolution = self.resolution
        n = int(pulse_length / resolution)
        t = np.linspace(self.start_x, self.end_x, n)
        x = sympy.symbols("x")

        found_variables = dict()
        # Create a dictionary of the parameters and their values
        for parameter in self.parameters:
            found_variables[parameter.symbol] = parameter.value

        final_expr = self.expr.subs(found_variables)
        # If the expression is a number (does not depend on x), return an array of that number
        if final_expr.is_number:
            return np.full(t.shape, float(final_expr))

        f = sympy.lambdify([x], final_expr, "numpy")

        return f(t)

    def get_tdx(self, pulse_length: float) -> np.ndarray:
        """Returns the time domain points and the evaluated function for the given pulse length.

        Args:
            pulse_length (float): The pulse length in seconds.

        Returns:
            np.ndarray: The time domain points.
        """
        n = int(pulse_length / self.resolution)
        t = np.linspace(self.start_x, self.end_x, n)
        return t

    def frequency_domain_plot(self, pulse_length: float) -> MplWidget:
        """Plots the frequency domain of the function for the given pulse length.

        Args:
            pulse_length (float): The pulse length in seconds.

        Returns:
            MplWidget: The matplotlib widget containing the plot.
        """
        mpl_widget = MplWidget()
        td = self.get_time_points(pulse_length)
        yd = self.evaluate(pulse_length)
        xdf, ydf = sp.fft(td, yd)
        mpl_widget.canvas.ax.plot(xdf, abs(ydf))
        mpl_widget.canvas.ax.set_xlabel("Frequency in Hz")
        mpl_widget.canvas.ax.set_ylabel("Magnitude")
        mpl_widget.canvas.ax.grid(True)
        return mpl_widget

    def time_domain_plot(self, pulse_length: float) -> MplWidget:
        """Plots the time domain of the function for the given pulse length.

        Args:
            pulse_length (float): The pulse length in seconds.

        Returns:
            MplWidget: The matplotlib widget containing the plot.
        """
        mpl_widget = MplWidget()
        td = self.get_time_points(pulse_length)
        mpl_widget.canvas.ax.plot(td, abs(self.evaluate(pulse_length)))
        mpl_widget.canvas.ax.set_xlabel("Time in s")
        mpl_widget.canvas.ax.set_ylabel("Magnitude")
        mpl_widget.canvas.ax.grid(True)
        return mpl_widget

    def get_pulse_amplitude(
        self, pulse_length: float, resolution: float = None
    ) -> np.array:
        """Returns the pulse amplitude in the time domain.

        Args:
            pulse_length (Float): The pulse length in seconds.
            resolution (float, optional): The resolution of the function in seconds. Defaults to None.

        Returns:
            np.array: The pulse amplitude.
        """
        return self.evaluate(pulse_length, resolution=resolution)

    def add_parameter(self, parameter: Function.Parameter) -> None:
        """Adds a parameter to the function.

        Args:
        parameter (Function.Parameter): The parameter to add.
        """
        self.parameters.append(parameter)

    def to_json(self) -> dict:
        """Returns a json representation of the function.

        Returns:
            dict: The json representation of the function.
        """
        return {
            "name": self.name,
            "class" : self.__class__.__name__,
            "parameters": [parameter.to_json() for parameter in self.parameters],
            "expression": str(self.expr),
            "resolution": self.resolution,
            "start_x": self.start_x,
            "end_x": self.end_x,
        }

    @classmethod
    def from_json(cls, data: dict) -> Function:
        """Creates a function from a json representation.

        Args:
            data (dict): The json representation of the function.

        Returns:
            Function: The function.
        """
        logger.debug(f"Data: {data}")
        for subclass in cls.subclasses:
            logger.debug("Checking subclass %s", subclass)
            logger.debug("Subclass name %s", subclass.__name__)
            if subclass.__name__ == data["class"]:
                cls = subclass
                logger.debug("Found subclass %s", cls)
                break

        obj = cls()
        obj.expr = data["expression"]
        obj.name = data["name"]
        obj.resolution = data["resolution"]
        obj.start_x = data["start_x"]
        obj.end_x = data["end_x"]

        obj.parameters = []
        for parameter in data["parameters"]:
            obj.add_parameter(Function.Parameter.from_json(parameter))

        return obj

    @property
    def expr(self):
        """The sympy expression of the function."""
        return self._expr

    @expr.setter
    def expr(self, expr):
        if isinstance(expr, str):
            try:
                self._expr = sympy.sympify(expr)
            except ValueError:
                logger.error(f"Could not convert {expr} to a sympy expression")
                raise SyntaxError(f"Could not convert {expr} to a sympy expression")
        elif isinstance(expr, sympy.Expr):
            self._expr = expr

    @property
    def resolution(self):
        """The resolution of the function in seconds."""
        return self._resolution

    @resolution.setter
    def resolution(self, resolution):
        try:
            self._resolution = float(resolution)
        except ValueError:
            logger.error("Could not convert %s to a float", resolution)
            raise SyntaxError(f"Could not convert {resolution} to a float")

    @property
    def start_x(self):
        """The x value where the evalution of the function starts."""
        return self._start_x

    @start_x.setter
    def start_x(self, start_x):
        try:
            self._start_x = float(start_x)
        except ValueError:
            logger.error("Could not convert %s to a float", start_x)
            raise SyntaxError(f"Could not convert {start_x} to a float")

    @property
    def end_x(self):
        """The x value where the evalution of the function ends."""
        return self._end_x

    @end_x.setter
    def end_x(self, end_x):
        try:
            self._end_x = float(end_x)
        except ValueError:
            logger.error("Could not convert %s to a float", end_x)
            raise SyntaxError(f"Could not convert {end_x} to a float")

    class Parameter:
        """A parameter of a function.

        This can be for example the standard deviation of a Gaussian function.

        Args:
            name (str): The name of the parameter.
            symbol (str): The symbol of the parameter.
            value (float): The value of the parameter.

        Attributes:
            name (str): The name of the parameter.
            symbol (str): The symbol of the parameter.
            value (float): The value of the parameter.
            default (float): The default value of the parameter.
        """

        def __init__(self, name: str, symbol: str, value: float) -> None:
            """Initializes the parameter."""
            self.name = name
            self.symbol = symbol
            self.value = value
            self.default = value

        def set_value(self, value: float) -> None:
            """Sets the value of the parameter.

            Args:
                value (float): The new value of the parameter.
            """
            self.value = value
            logger.debug("Parameter %s set to %s", self.name, self.value)

        def to_json(self) -> dict:
            """Returns a json representation of the parameter.

            Returns:
                dict: The json representation of the parameter.
            """
            return {
                "name": self.name,
                "symbol": self.symbol,
                "value": self.value,
                "default": self.default,
            }

        @classmethod
        def from_json(cls, data):
            """Creates a parameter from a json representation.

            Args:
                data (dict): The json representation of the parameter.

            Returns:
                Function.Parameter: The parameter.
            """
            obj = cls(data["name"], data["symbol"], data["value"])
            obj.default = data["default"]
            return obj


class RectFunction(Function):
    """The rectangular function."""

    name = "Rectangular"

    def __init__(self) -> None:
        """Initializes the RecFunction."""
        expr = sympy.sympify("1")
        super().__init__(expr)


class SincFunction(Function):
    """The sinc function.

    The sinc function is defined as sin(x * l) / (x * l).
    The parameter is the scale factor l.
    """

    name = "Sinc"

    def __init__(self) -> None:
        """Initializes the SincFunction."""
        expr = sympy.sympify("sin(x * l)/ (x * l)")
        super().__init__(expr)
        self.add_parameter(Function.Parameter("Scale Factor", "l", 2))
        self.start_x = -np.pi
        self.end_x = np.pi


class GaussianFunction(Function):
    """The Gaussian function.

    The Gaussian function is defined as exp(-0.5 * ((x - mu) / sigma)**2).
    The parameters are the mean and the standard deviation.
    """

    name = "Gaussian"

    def __init__(self) -> None:
        """Initializes the GaussianFunction."""
        expr = sympy.sympify("exp(-0.5 * ((x - mu) / sigma)**2)")
        super().__init__(expr)
        self.add_parameter(Function.Parameter("Mean", "mu", 0))
        self.add_parameter(Function.Parameter("Standard Deviation", "sigma", 1))
        self.start_x = -np.pi
        self.end_x = np.pi


# class TriangleFunction(Function):
#    def __init__(self) -> None:
#        expr = sympy.sympify("triang(x)")
#        super().__init__(lambda x: triang(x))


class CustomFunction(Function):
    """A custom function."""

    name = "Custom"

    def __init__(self) -> None:
        """Initializes the Custom Function."""
        expr = sympy.sympify(" 2 * x**2 + 3 * x + 1")
        super().__init__(expr)
