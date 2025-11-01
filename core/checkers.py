from .player import Player

class Checkers:
    """
    Represents a single checker (or piece) on the board.
    """

    def __init__(self, owner: Player):
        """
        Initializes a Checker object.

        Args:
            owner (Player): The player who owns this checker.
        """
        self.__owner__ = owner

    def get_owner(self):
        """
        Returns the owner of the checker.

        Returns:
            Player: The player who owns this checker.
        """
        return self.__owner__
