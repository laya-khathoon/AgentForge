"""More offline tests for the calculator tool."""
import unittest

from app.tools.calculator import calculate


class CalculatorMoreTests(unittest.TestCase):
    def test_floor_division_and_modulo(self):
        self.assertEqual(calculate("17 // 5"), "3")
        self.assertEqual(calculate("17 % 5"), "2")

    def test_unary_minus_and_brackets(self):
        self.assertEqual(calculate("-(2 + 3) * 4"), "-20")

    def test_decimal_results_stay_decimal(self):
        self.assertEqual(calculate("7 / 2"), "3.5")

    def test_whole_float_is_shown_as_integer(self):
        self.assertEqual(calculate("10 / 2"), "5")

    def test_division_by_zero_is_explained(self):
        self.assertIn("Cannot calculate", calculate("1 / 0"))


if __name__ == "__main__":
    unittest.main()
