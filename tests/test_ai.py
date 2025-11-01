import unittest
from core.player import Player
from core.ai import AIPlayer
from core.board import Board
from core.checkers import Checkers

class TestAIPlayer(unittest.TestCase):
    def setUp(self):
        self.p1 = Player("Human", "white")
        self.ai = AIPlayer("Computer", "black")
        self.board = Board(self.p1, self.ai, random_positions=False)

    def test_ai_chooses_valid_move(self):
        # AI is black, moves from 0 up to 23.
        # Standard setup has AI checkers at 0, 11, 16, 18.
        dice = [3, 4]
        moves = self.ai.choose_moves(self.board, dice)
        
        self.assertGreater(len(moves), 0)
        
        # Validate the chosen moves
        from_point, to_point = moves[0]
        
        # The AI should return a (from, to) tuple
        self.assertIsInstance(from_point, int)
        self.assertIsInstance(to_point, int)
        
        # Check if the move is valid for one of the dice
        die_used = abs(to_point - from_point)
        self.assertIn(die_used, dice)
        self.assertTrue(self.board.is_valid_move(from_point, die_used, self.ai))

    def test_ai_moves_from_bar(self):
        # Put an AI checker on the bar
        self.board.get_bar()[self.ai] = [Checkers(self.ai)]
        # Clear points for entry with dice 3 or 5
        self.board.get_points()[2] = [] # Entry for die 3
        self.board.get_points()[4] = [] # Entry for die 5

        dice = [3, 5]
        moves = self.ai.choose_moves(self.board, dice)
        
        # The AI must make a move from the bar.
        self.assertGreater(len(moves), 0)
        from_point, to_point = moves[0]
        self.assertEqual(from_point, 'bar')
        
        # Check that the move corresponds to a valid die.
        die_used = to_point + 1
        self.assertIn(die_used, dice)

    def test_ai_chooses_bear_off_move(self):
        # Setup for bear-off
        for i in range(24): self.board.get_points()[i] = []
        self.board._set_off_board_count(self.ai, 14)
        self.board.get_points()[18] = [Checkers(self.ai)] # AI checker on its 6-point

        dice = [6, 2]
        moves = self.ai.choose_moves(self.board, dice)
        
        self.assertIn((18, 'off'), moves)

if __name__ == "__main__":
    unittest.main()
