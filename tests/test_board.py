from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING
from core.checkers import Checkers
import random

if TYPE_CHECKING:
    from core.player import Player
    from core.ai import AIPlayer


class Board:
    """
    Manages the Backgammon board state and move validation.
    """

    def __init__(self, player1: 'Player', player2: 'Player', random_positions: bool = False):
        """
        Initializes the Board object.

        Args:
            player1 (Player): The first player (white).
            player2 (Player): The second player (black).
            random_positions (bool, optional): Whether to set up the board with random checker positions. Defaults to False.
        """
        self.__player1__ = player1  # White
        self.__player2__ = player2  # Black
        self.__winner__ = None
        self.__points__ = self._create_points(random_positions)
        self.__bar__: Dict['Player', List[Checkers]] = {player1: [], player2: []}
        self.__off_board__: Dict['Player', int] = {player1: 0, player2: 0}

    def _create_points(self, random_positions: bool = False):
        """
        Creates the initial layout of the checkers on the board.

        Args:
            random_positions (bool, optional): If True, places checkers randomly. Defaults to False.

        Returns:
            list: A list of 24 lists, where each inner list represents a point on the board.
        """
        points = [[] for _ in range(24)]
        if not random_positions:
            # Player 1 (White) moves from 23 down to 0
            points[23] = [Checkers(self.__player1__) for _ in range(2)]
            points[12] = [Checkers(self.__player1__) for _ in range(5)]
            points[7] = [Checkers(self.__player1__) for _ in range(3)]
            points[5] = [Checkers(self.__player1__) for _ in range(5)]
            
            # Player 2 (Black) moves from 0 up to 23
            points[0] = [Checkers(self.__player2__) for _ in range(2)]
            points[11] = [Checkers(self.__player2__) for _ in range(5)]
            points[16] = [Checkers(self.__player2__) for _ in range(3)]
            points[18] = [Checkers(self.__player2__) for _ in range(5)]
        else:
            # Random setup
            for player in [self.__player1__, self.__player2__]:
                remaining_checkers = 15
                while remaining_checkers > 0:
                    point_index = random.randrange(24)
                    if not points[point_index] or points[point_index][0].get_owner() == player:
                        num_to_place = random.randint(1, remaining_checkers)
                        for _ in range(num_to_place):
                            points[point_index].append(Checkers(player))
                        remaining_checkers -= num_to_place
        return points

    def get_point(self, index: int):
        """
        Returns the checkers at a specific point on the board.

        Args:
            index (int): The point index (0-23).

        Returns:
            list: A list of Checkers at the specified point.
        
        Raises:
            IndexError: If the index is out of bounds.
        """
        if 0 <= index < 24: return self.__points__[index]
        raise IndexError("Invalid point index")

    def get_points(self):
        """Returns the entire list of points on the board."""
        return self.__points__

    def get_bar(self):
        """Returns the dictionary representing the bar."""
        return self.__bar__

    def get_off_board_count(self, player: 'Player'):
        """Returns the number of checkers a player has borne off."""
        return self.__off_board__.get(player, 0)

    def _set_off_board_count(self, player: 'Player', count: int):
        """Sets the number of checkers a player has borne off (for testing)."""
        self.__off_board__[player] = count

    def get_winner(self):
        """Returns the winner of the game, if any."""
        return self.__winner__


    def is_valid_move(self, from_point, die: int, player: 'Player'):
        """
        Checks if a move is valid according to the rules of Backgammon.

        Args:
            from_point (str or int): The starting point ('bar' or 0-23).
            die (int): The value of the die to use for the move.
            player (Player): The player making the move.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if die <= 0: return False

        direction = -1 if player.get_color() == 'white' else 1
        
        if from_point == 'bar':
            if not self.__bar__.get(player): return False
            to_point = 24 + die * direction if player.get_color() == 'white' else -1 + die * direction
        else:
            if self.__bar__.get(player): return False
            if not self.__points__[from_point] or self.__points__[from_point][0].get_owner() != player:
                return False
            to_point = from_point + (die * direction)
        
        is_bear_off = (direction == 1 and to_point > 23) or (direction == -1 and to_point < 0)
        if is_bear_off:
            return self.is_valid_bear_off_move(from_point, die, player)
        
        if not (0 <= to_point < 24): return False
        
        destination = self.__points__[to_point]
        return not (destination and destination[0].get_owner() != player and len(destination) > 1)

    def move_piece(self, from_point, die: int, player: Player):
        """
        Moves a checker on the board.

        Args:
            from_point (str or int): The starting point ('bar' or 0-23).
            die (int): The die value used for the move.
            player (Player): The player making the move.

        Raises:
            ValueError: If the move is invalid.
        """
        if not self.is_valid_move(from_point, die, player):
            raise ValueError("Invalid move")

        direction = -1 if player.get_color() == 'white' else 1
        
        if from_point == 'bar':
            checker = self.__bar__[player].pop(0)
            to_point = 24 + die * direction if player.get_color() == 'white' else -1 + die * direction
        else:
            checker = self.__points__[from_point].pop()
            to_point = from_point + (die * direction)

        is_bear_off = (direction == -1 and to_point < 0) or (direction == 1 and to_point > 23)
        if is_bear_off:
            self.__off_board__[player] += 1
            if self.__off_board__[player] == 15: self.__winner__ = player
            return
            
        destination = self.__points__[to_point]
        if destination and destination[0].get_owner() != player:
            opponent_checker = destination.pop()
            self.__bar__[opponent_checker.get_owner()].append(opponent_checker)
        
        self.__points__[to_point].append(checker)

    def can_player_bear_off(self, player: Player):
        """
        Checks if a player is in a position to start bearing off checkers.

        Args:
            player (Player): The player to check.

        Returns:
            bool: True if the player can bear off, False otherwise.
        """
        if self.__bar__.get(player):
            return False

        color = player.get_color()
        home_board_indices = range(6) if color == 'white' else range(18, 24)
        
        checkers_in_home = 0
        for i in home_board_indices:
            point = self.__points__[i]
            if point and point[0].get_owner() == player:
                checkers_in_home += len(point)
        
        total_checkers = self.get_off_board_count(player) + checkers_in_home
        
        return total_checkers == 15

    def is_valid_bear_off_move(self, from_point, die, player):
        """
        Checks if a bear-off move is valid.

        Args:
            from_point (int): The point from which to bear off.
            die (int): The value of the die used.
            player (Player): The player making the move.

        Returns:
            bool: True if the bear-off move is valid, False otherwise.
        """
        if not self.can_player_bear_off(player):
            return False

        color = player.get_color()
        if color == 'white':  # Home is 0-5
            if from_point > 5: return False
            # Exact roll only
            return (from_point + 1) == die
        else:  # Black, home is 18-23
            if from_point < 18: return False
            # Exact roll only
            return (24 - from_point) == die

    def get_possible_moves_for_checker(self, from_point, player, dice):
        """
        Gets all possible moves for a single checker.

        Args:
            from_point (str or int): The starting point of the checker.
            player (Player): The player who owns the checker.
            dice (list): A list of available dice values.

        Returns:
            list: A list of possible destination points (int or 'off').
        """
        moves = []
        direction = -1 if player.get_color() == 'white' else 1
        for die in set(dice):
            if self.is_valid_move(from_point, die, player):
                if from_point == 'bar':
                    to_point = 24 + die * direction if player.get_color() == 'white' else -1 + die * direction
                else:
                    to_point = from_point + (die * direction)
                
                is_bear_off = (direction == -1 and to_point < 0) or (direction == 1 and to_point > 23)
                if is_bear_off: 
                    moves.append("off")
                elif 0 <= to_point < 24: 
                    moves.append(to_point)
        return moves
        
    def has_any_valid_moves(self, player, dice):
        """
        Checks if the player has any valid moves with the available dice.

        Args:
            player (Player): The player to check.
            dice (list): A list of available dice values.

        Returns:
            bool: True if there is at least one valid move, False otherwise.
        """
        if self.__bar__.get(player):
            for die in dice:
                if self.is_valid_move('bar', die, player): return True
            return False
        for i in range(24):
            if self.__points__[i] and self.__points__[i][0].get_owner() == player:
                for die in dice:
                    if self.is_valid_move(i, die, player): return True
        return False
        
    def find_die_for_bear_off(self, from_point, player, dice):
        """
        Finds the exact die required for a bear-off move and checks if it's available.
        Returns the die value if valid, otherwise None.
        """
        required_die = (from_point + 1) if player.get_color() == 'white' else (24 - from_point)
        
        if required_die in dice:
            if self.is_valid_bear_off_move(from_point, required_die, player):
                return required_die
        return None
