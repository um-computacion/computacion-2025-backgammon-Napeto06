from typing import TYPE_CHECKING, List
from .player import Player
import copy

if TYPE_CHECKING:
    from .board import Board

class AIPlayer(Player):
    """
    Represents an AI player that can choose its own moves. Inherits from Player.
    """

    def choose_moves(self, board: 'Board', dice: List[int]) -> List[tuple]:
        """
        Chooses a sequence of moves for the AI based on the current board state and dice.

        This implementation uses a simple greedy algorithm that prioritizes higher dice values
        and bearing off. It simulates moves on a temporary board to find a valid sequence.

        Args:
            board (Board): The current state of the game board.
            dice (List[int]): The dice values available for the turn.

        Returns:
            List[tuple]: A list of move tuples, e.g., [('bar', 22), (5, 3)].
        """
        best_moves = []
        temp_board = copy.deepcopy(board)
        temp_dice = sorted(list(set(dice)), reverse=True)  # Use unique dice, higher first
        
        if len(dice) > len(temp_dice): # Handle doubles
            temp_dice = list(dice)

        direction = 1 if self.get_color() == 'black' else -1

        while temp_dice:
            die_to_use = None
            move_found = None

            # Priority 1: Find a valid move from the bar
            if temp_board.get_bar().get(self):
                for d in temp_dice:
                    # The move logic in board.py handles the conversion from die to point
                    if temp_board.is_valid_move('bar', d, self):
                        to_point = (d - 1) if self.get_color() == 'black' else (24 - d)
                        move_found = ('bar', to_point)
                        die_to_use = d
                        break
            
            # Priority 2: Find a normal or bear-off move
            else:
                # Iterate through dice from largest to smallest to prioritize larger moves
                for d in sorted(temp_dice, reverse=True):
                    # Iterate through points based on player color/direction
                    point_range = range(24) if self.get_color() == 'black' else range(23, -1, -1)
                    for i in point_range:
                        # Check if a checker of the AI's color is on this point
                        if temp_board.get_point(i) and temp_board.get_point(i)[0].get_owner() == self:
                            if temp_board.is_valid_move(i, d, self):
                                # Check for bear-off first if eligible
                                if temp_board.can_player_bear_off(self):
                                    # Exact bear-off
                                    if (self.get_color() == 'white' and (i + 1) == d) or \
                                       (self.get_color() == 'black' and (24 - i) == d):
                                        move_found = (i, 'off')
                                        die_to_use = d
                                        break # Found a bear-off, stop searching points
                                
                                # If no bear-off, consider a normal move
                                if not move_found:
                                    to_point_calc = i + (d * direction)
                                    if 0 <= to_point_calc < 24:
                                         # Check if the destination point is valid
                                        target_point_content = temp_board.get_point(to_point_calc)
                                        if not target_point_content or len(target_point_content) <= 1 or target_point_content[0].get_owner() == self:
                                            move_found = (i, to_point_calc)
                                            die_to_use = d
                                            break # Found a normal move, stop searching points
                    if move_found:
                        break  # Found a move, stop searching dice for this turn

            if move_found and die_to_use is not None:
                best_moves.append(move_found)
                if die_to_use in temp_dice:
                    temp_dice.remove(die_to_use)
                
                # Simulate the move on the temp board for the next iteration
                from_point_sim, _ = move_found
                temp_board.move_piece(from_point_sim, die_to_use, self)

            else:
                # No more moves possible with the remaining dice
                break

        return best_moves
