from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .board import Board

class Player:
    """
    A class used to represent a player in the Backgammon game.

    Attributes
    ----------
    __name__ : str
        The name of the player.
    __color__ : str
        The color of the player ('white' or 'black').
    __can_bear_off__ : bool
        Whether the player is in the bear-off phase.
    """

    def __init__(self, name: str, color: str):
        """
        Constructs all the necessary attributes for the player object.

        Parameters
        ----------
        name : str
            The name of the player.
        color : str
            The color of the player's checkers ('white' or 'black').
        """
        self.__name__ = name
        self.__color__ = color
        self.__can_bear_off__ = False

    def __eq__(self, other):
        """
        Checks if two players are equal based on name.
        """
        if not isinstance(other, Player):
            return False
        return self.__name__ == other.__name__

    def __repr__(self):
        """
        Returns a string representation of the player.
        """
        return f"Player(name='{self.__name__}', color='{self.__color__}')"

    def __hash__(self):
        """
        Returns a hash value for the player based on name.
        """
        return hash(self.__name__)

    def get_name(self):
        """Getter for name."""
        return self.__name__

    def get_color(self):
        """Getter for color."""
        return self.__color__

    def set_can_bear_off(self, can_bear_off):
        """Setter for can_bear_off status, primarily for testing."""
        self.__can_bear_off__ = can_bear_off

    def can_bear_off(self):
        """Getter for can_bear_off status."""
        return self.__can_bear_off__
