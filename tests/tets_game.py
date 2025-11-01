import unittest
from unittest.mock import patch, MagicMock
from core.game import Game
from core.player import Player
from core.ai import AIPlayer
from core.checkers import Checkers

class TestGame(unittest.TestCase):

    def setUp(self):
        self.p1 = Player("Human", "white")
        self.p2_ai = AIPlayer("Computer", "black")
        self.game = Game(players=[self.p1, self.p2_ai])

    def test_move_validation(self):
        # White's turn, wants to move from 23 to 21 (die roll 2)
        self.game.dice.set_values([2, 5])
        self.game.current_player_index = 0 # White's turn
        
        # Mock board's move_piece to avoid complex setup
        with patch.object(self.game.board, 'move_piece') as mock_move_piece:
            self.game.move(23, 21)
            mock_move_piece.assert_called_once_with(23, 2, self.p1)
        
        # Check that the die was consumed
        self.assertEqual(self.game.dice.get_values(), [5])

    def test_bear_off_move(self):
        # White's turn, bearing off from point 3 (needs a 4, 5, or 6)
        self.game.current_player_index = 0
        self.game.dice.set_values([4, 1])

        # Setup board for bear-off
        for i in range(24): self.game.board.get_points()[i] = []
        self.game.board._set_off_board_count(self.p1, 14)
        self.game.board.get_points()[3] = [Checkers(self.p1)]
        
        self.game.move(3, 'off')
        
        # Verify checker was borne off and die was consumed
        self.assertEqual(self.game.board.get_off_board_count(self.p1), 15)
        self.assertEqual(self.game.dice.get_values(), [1])
        self.assertTrue(self.game.is_game_over())

    def test_ai_turn_executes_moves(self):
        self.game.current_player_index = 1 # AI's turn
        self.game.dice.set_values([3, 4])

        # Mock AI's move choice
        self.p2_ai.choose_moves = MagicMock(return_value=[(0, 3), (0, 4)])

        with patch.object(self.game, 'move') as mock_game_move:
            self.game.play_ai_turn()
            # Verify that the moves were executed
            self.assertEqual(mock_game_move.call_count, 2)
            # Verify that the player DOES NOT change, as this is now UI responsibility
            self.assertEqual(self.game.get_current_player(), self.p2_ai)

    def test_invalid_move_raises_error(self):
        self.game.dice.set_values([1, 1])
        # White trying to move from 23 to 18 (needs a 5)
        with self.assertRaises(ValueError):
            self.game.move(23, 18)

if __name__ == '__main__':
    unittest.main()
