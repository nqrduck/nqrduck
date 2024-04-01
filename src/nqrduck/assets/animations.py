"""Provides methods to load animations."""

import logging
from pathlib import Path
from PyQt6.QtGui import QMovie

logger = logging.getLogger(__name__)


class Animations:
    """This class provides methods to load animations.

    The animations are loaded from the assets/animations folder.
    """

    @staticmethod
    def load_animation(folder, name):
        """Loads an animation and returns it as a QMovie.

        Args:
            folder (str): The folder in which the animation is located.
            name (str): The name of the animation to load.

        Returns:
            QMovie: The loaded animation.
        """
        path = Path(__file__).parent / folder / name
        animation = QMovie(str(path))

        # Print warning if the animation could not be loaded
        if not animation.isValid():
            logger.warning(f"Could not load animation: {path}")

        return animation

    @staticmethod
    def get_animation(name):
        """Returns an animation as a QMovie.

        Args:
            name (str): The name of the animation to load.

        Returns:
            QMovie: The loaded animation.
        """
        return Animations.load_animation("animations", name)


class DuckAnimations(Animations):
    """This class provides duck animations."""

    @staticmethod
    def DuckKick128x128():
        """Returns the DuckKick animation as a QMovie.

        Careful this has been exported at 400% so it might look odd if placed to other assets.

        Returns:
            QMovie: The DuckKick animation.
        """
        return Animations.get_animation("DuckKick_128x128.gif")

    @staticmethod
    def DuckSleep128x128():
        """Returns the DuckSleep animation as a QMovie.

        Careful this has been exported at 400% so it might look odd if placed to other assets.

        Returns:
            QMovie: The DuckSleep animation.
        """
        return Animations.get_animation("DuckSleep_128x128.gif")
