import random

class Dice:
    """
    A class used to represent dice in the Backgammon game.

    Attributes
    ----------
    values : list of int
        The current values of the dice.
    """

    def __init__(self):
        """Initializes the Dice object with no values."""
        self.__values__ = []

    def roll(self):
        """
        Rolls two dice and updates their values.

        Returns:
            list[int]: The new values of the dice.
        """
        self.__values__ = [random.randint(1, 6), random.randint(1, 6)]
        return self.__values__

    def roll_one(self):
        """
        Rolls a single die.

        Returns:
            int: The value of the rolled die.
        """
        return random.randint(1, 6)

    def get_values(self):
        """
        Returns the current values of the dice.

        Returns:
            list[int]: The current dice values.
        """
        return self.__values__

    def set_values(self, values):
        """
        Sets the dice to specific values.

        Args:
            values (list[int]): The values to set the dice to.
        """
        self.__values__ = values

    def remove_value(self, value):
        """
        Removes a die value after it has been used for a move.

        Args:
            value (int): The die value to remove.
        
        Raises:
            ValueError: If the value is not available in the current dice.
        """
        if value in self.__values__:
            self.__values__.remove(value)
        else:
            raise ValueError(f"Die value {value} not available in {self.__values__}")
