"""Offline tests for the calculator tool."""
import unittest

from app.tools.calculator import calculate
from app.tools.registry import run_tool


class CalculatorTests(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(calculate("2 + 3 * 4"), "14")
        self.assertEqual(calculate("(2 + 3) * 4"), "20")
        self.assertEqual(calculate("10 / 4"), "2.5")
        self.assertEqual(calculate("7 // 2"), "3")
        self.assertEqual(calculate("7 % 2"), "1")
        self.assertEqual(calculate("2 ** 10"), "1024")
        self.assertEqual(calculate("-5 + 2"), "-3")

    def test_empty_expression_is_explained(self):
        self.assertTrue(calculate("").startswith("Nothing to calculate"))
        self.assertTrue(calculate(None).startswith("Nothing to calculate"))

    def test_unsafe_input_is_refused(self):
        for bad in ("__import__('os')", "open('x')", "x + 1", "1 / 0",
                    "9 ** " + "9" * 30, "[1,2][0]"):
            with self.subTest(bad=bad):
                self.assertIn("Cannot calculate", calculate(bad))

    def test_resource_limits_and_nonfinite_values(self):
        for bad in ("9 ** 999999999", "2 ** 101", "1e309 + 1", "1e309", "True", "(-1) ** 0.5",
                    "9" * 501, "(" * 300 + "1" + ")" * 300, 42):
            with self.subTest(bad=bad):
                self.assertIn("Cannot calculate", calculate(bad))

    def test_registered_as_a_tool(self):
        self.assertEqual(run_tool("calculate", "6 * 7"), "42")


if __name__ == "__main__":
    unittest.main()
