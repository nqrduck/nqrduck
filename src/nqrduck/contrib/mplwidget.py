import logging
from PyQt6 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib as mpl
from matplotlib import font_manager
from pathlib import Path

logger = logging.getLogger(__name__)

# Code taken from: https://stackoverflow.com/questions/43947318/plotting-matplotlib-figure-inside-qwidget-using-qt-designer-form-and-pyqt5
# Author: launchpadmcquack (cool name)
# License: https://creativecommons.org/licenses/by-sa/3.0/

# Ensure using PyQt5 backend
# matplotlib.use("QT5Agg")


# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(
             self, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding
        )
        Canvas.updateGeometry(self)


# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)  # Inherit from QWidget
        self.canvas = MplCanvas()  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()  # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        
        # Set custom font
        path = Path(__file__).parent
        font_path = str(path / '../core/resources/font/AsepriteFont.ttf')  # Your font path goes here
        logger.debug("Adding font: " + font_path)

        font_manager.fontManager.addfont(font_path)
        prop = font_manager.FontProperties(fname=font_path)
        mpl.rcParams['font.family'] = 'sans-serif'
        mpl.rcParams['font.sans-serif'] = prop.get_name()
        mpl.rcParams['font.size'] = 15

        self.setStyleSheet('background-color:transparent;')
        logger.debug("Set stylesheet to %s" % self.styleSheet())

        mpl.rcParams.update({
            "figure.facecolor":  (0.0, 0.0, 0.0, 0.00),  # transparent   
            "axes.facecolor":    (0.0, 1.0, 0.0, 0.03),  # green 
            "savefig.facecolor": (0.0, 0.0, 0.0, 0.0),  # transparent
        })

        # Set custom matplotlib parameters
        mpl.rcParams['figure.subplot.bottom'] = 0.2
        mpl.rcParams['axes.linewidth'] = 1.5
        mpl.rcParams['xtick.major.width'] = 1.5
        mpl.rcParams['ytick.major.width'] = 1.5
        mpl.rcParams['xtick.minor.width'] = 1.5
        mpl.rcParams['ytick.minor.width'] = 1.5
        mpl.rcParams['xtick.major.size'] = 6
        mpl.rcParams['ytick.major.size'] = 6
        mpl.rcParams['xtick.minor.size'] = 4
        mpl.rcParams['ytick.minor.size'] = 4
        

