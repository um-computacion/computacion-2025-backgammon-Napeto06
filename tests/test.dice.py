import unittest
import random
from core.dice import roll_dice


class TestDice(unittest.TestCase):
    """
    Tests for the roll_dice function.
    """

    def setUp(self):

        random.seed(42)

    def test_normal_roll(self):
        """Test normal roll: Two different values between 1-6."""
        result = roll_dice()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(1 <= d <= 6 for d in result))
        self.assertNotEqual(result[0], result[1])

    def test_doubles_roll(self):
        """Test doubles: Returns [d, d, d, d] if equal."""

        original_randint = random.randint

        def mock_randint(a, b):
            return 3

        random.randint = mock_randint
        result = roll_dice()
        self.assertEqual(result, [3, 3, 3, 3])
        random.randint = original_randint

    def test_dice_range(self):
        """Test all values are 1-6."""
        for _ in range(100):
            result = roll_dice()
            for d in result:
                self.assertIn(d, range(1, 7))

    def test_roll_dice_range(self):
        for _ in range(100):
            result = roll_dice()
            self.assertTrue(all(1 <= d <= 6 for d in result))
            self.assertIn(len(result), [2, 4])

    def test_roll_dice_doubles(self):
        # Si hay 4 valores, todos deben ser iguales
        for _ in range(100):
            result = roll_dice()
            if len(result) == 4:
                self.assertTrue(all(d == result[0] for d in result))


if __name__ == "__main__":
    unittest.main()
