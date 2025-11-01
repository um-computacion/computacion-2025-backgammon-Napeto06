import unittest
from core.player import Player
from core.checkers import Checkers


class TestCheckers(unittest.TestCase):
    """
    Tests for the Checkers class.
    """

    def setUp(self):
        self.player = Player("Alice", "white")
        self.checker = Checkers(self.player)

    def test_init(self):
        """Test initialization: Owner set correctly."""
        self.assertEqual(self.checker.owner, self.player)
        self.assertEqual(self.checker.owner.name, "Alice")

    def test_repr(self):
        """Test string representation."""
        self.assertEqual(repr(self.checker), "Checkers(player(Alice))")

    def test_checker_owner(self):
        p = Player("Alice", "white")
        c = Checkers(p)
        self.assertEqual(c.owner, p)

    def test_checker_repr(self):
        p = Player("Bob", "black")
        c = Checkers(p)
        self.assertIn("Bob", repr(c))


if __name__ == "__main__":
    unittest.main()
