"""Used for plotting matplotlib figures in the nqrduck program."""

import logging
from PyQt6 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib as mpl

logger = logging.getLogger(__name__)

# Code taken from: https://stackoverflow.com/questions/43947318/plotting-matplotlib-figure-inside-qwidget-using-qt-designer-form-and-pyqt5
# Author: launchpadmcquack (cool name)
# License: https://creativecommons.org/licenses/by-sa/3.0/

# Ensure using PyQt5 backend
# matplotlib.use("QT5Agg")


# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
    """This class creates a matplotlib canvas to plot figures."""

    def __init__(self):
        """Initializes the MplCanvas."""
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(
            self,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        Canvas.updateGeometry(self)


# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    """A Matplotlib Widget.

    Args:
        parent (QWidget): The parent widget.
    """

    def __init__(self, parent=None):
        """Initializes the MplWidget."""
        QtWidgets.QWidget.__init__(self, parent)  # Inherit from QWidget
        self.canvas = MplCanvas()  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()  # Set box for plottingg

        # Add navigation bar
        self.toolbar = NavigationToolbar(self.canvas, self)
        # Create a horizontal layout to include the navigation toolbar and spacers
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addStretch(1)
        hlayout.addWidget(self.toolbar)
        hlayout.addStretch(1)

        self.vbl.addLayout(hlayout)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

        self.setStyleSheet("background-color:transparent;")

        # Set custom matplotlib parameters
        mpl.rcParams["figure.subplot.bottom"] = 0.2
        mpl.rcParams["axes.linewidth"] = 1.5
        mpl.rcParams["xtick.major.width"] = 1.5
        mpl.rcParams["ytick.major.width"] = 1.5
        mpl.rcParams["xtick.minor.width"] = 1.5
        mpl.rcParams["ytick.minor.width"] = 1.5
        mpl.rcParams["xtick.major.size"] = 6
        mpl.rcParams["ytick.major.size"] = 6
        mpl.rcParams["xtick.minor.size"] = 4
        mpl.rcParams["ytick.minor.size"] = 4
