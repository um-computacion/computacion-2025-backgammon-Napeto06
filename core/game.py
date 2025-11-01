from .board import Board
from .player import Player
from .dice import Dice


class Game:
    """
    A class used to represent the overall Backgammon game, coordinating board and players.

    Attributes
    ----------
    board : Board
        The game board.
    players : list of Player
        The list of players.
    current_player_index : int
        Index of the current player.
    dice : Dice
        The dice for the game.
    """

    def __init__(self, players: list['Player'], random_positions=False):
        """
        Initializes the Game object.

        Args:
            players (list[Player]): The list of players.
            random_positions (bool, optional): Whether to start with random checker positions. Defaults to False.
        """
        self.__players__ = players
        self.__board__ = Board(players[0], players[1], random_positions=random_positions)
        self.__current_player_index__ = 0
        self.__dice__ = Dice()
        self.__initial_rolls__ = [0, 0]
        self.__initial_roll_winner__ = None

    def get_current_player(self):
        """
        Returns the current player.

        Returns:
            Player: The player whose turn it is.
        """
        return self.__players__[self.__current_player_index__]

    def switch_player(self):
        """Switches the turn to the other player."""
        self.__current_player_index__ = 1 - self.__current_player_index__

    def roll_dice(self):
        """Rolls the dice for the current turn and handles doubles."""
        self.__dice__.roll()
        if self.__dice__.get_values()[0] == self.__dice__.get_values()[1]:
            # Doubles, grant four moves
            self.__dice__.set_values([self.__dice__.get_values()[0]] * 4)

    def determine_first_player(self):
        """Players roll one die each to determine who goes first, handling ties."""
        # Loop until there is a winner
        while self.__initial_roll_winner__ is None:
            p1_roll = self.__dice__.roll_one()
            p2_roll = self.__dice__.roll_one()

            if p1_roll > p2_roll:
                self.__initial_roll_winner__ = self.__players__[0]
                self.__current_player_index__ = 0
                self.__initial_rolls__ = [p1_roll, p2_roll]
            elif p2_roll > p1_roll:
                self.__initial_roll_winner__ = self.__players__[1]
                self.__current_player_index__ = 1
                self.__initial_rolls__ = [p1_roll, p2_roll]
            # If rolls are equal, the loop continues
        
        # The first turn's dice are the initial winning rolls
        self.__dice__.set_values(self.__initial_rolls__)
            
    def _calculate_and_validate_die_for_move(self, from_point: str | int, to_point: str | int, player: 'Player') -> int | None:
        """
        Calculates and validates the die value required for a given move.

        Args:
            from_point (str or int): The starting point.
            to_point (str or int): The ending point.
            player (Player): The player making the move.

        Returns:
            int or None: The die value if the move is valid with the current dice, otherwise None.
        """
        if to_point == 'off':
            return self.__board__.find_die_for_bear_off(from_point, player, self.__dice__.get_values())

        if from_point == 'bar':
            die = (24 - to_point) if player.get_color() == 'white' else (to_point + 1)
        else:
            die = abs(to_point - from_point)

        return die if die in self.__dice__.get_values() else None

    def move(self, from_point: str | int, to_point: str | int):
        """
        Executes a move after validating it.

        Args:
            from_point (str or int): The starting point.
            to_point (str or int): The ending point.
        
        Raises:
            ValueError: If the move is invalid.
        """
        player = self.get_current_player()
        die = self._calculate_and_validate_die_for_move(from_point, to_point, player)

        if die is None:
            raise ValueError("Invalid move or no available die for this move.")

        self.__board__.move_piece(from_point, die, player)
        self.__dice__.remove_value(die)

    def has_possible_moves(self, player: 'Player') -> bool:
        """
        Checks if the current player has any valid moves with the current dice.

        Args:
            player (Player): The player to check.

        Returns:
            bool: True if there are possible moves, False otherwise.
        """
        return self.__board__.has_any_valid_moves(player, self.__dice__.get_values())

    def play_ai_turn(self):
        """
        Executes the AI's turn by choosing and performing its moves.
        Note: This method does NOT roll dice or switch the turn. The UI is responsible
        for managing the turn flow (roll -> play -> switch).
        A local import is used to avoid circular dependencies.
        """
        from core.ai import AIPlayer
        player = self.get_current_player()

        if isinstance(player, AIPlayer):
            # The AI determines all its moves for the turn at once
            moves = player.choose_moves(self.__board__, self.__dice__.get_values())
            
            for from_point, to_point in moves:
                try:
                    # Each move is executed sequentially
                    self.move(from_point, to_point)
                except (ValueError, IndexError) as e:
                    # This may happen if the AI's logic produces a sequence of moves
                    # that becomes invalid after an earlier move is made.
                    print(f"AI tried an invalid move and has forfeited the rest of its turn: {from_point}->{to_point}. Error: {e}")
                    break # Stop processing further moves

    def is_game_over(self):
        """
        Checks if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        for player in self.__players__:
            if self.__board__.get_off_board_count(player) == 15:
                return True
        return False

    def get_winner(self):
        """
        Returns the winner of the game.

        Returns:
            Player or None: The winning player, or None if there is no winner yet.
        """
        return self.__board__.get_winner()

    # --- Properties for backward compatibility ---
    @property
    def board(self):
        return self.__board__

    @property
    def dice(self):
        return self.__dice__
        
    @property
    def initial_roll_winner(self):
        return self.__initial_roll_winner__

    @property
    def initial_rolls(self):
        return self.__initial_rolls__
        
    @property
    def players(self):
        return self.__players__
