"""Offline tests for the unit_convert tool."""
import unittest

from app.tools.unit_convert import unit_convert


class UnitConvertTests(unittest.TestCase):
    def test_length(self):
        self.assertEqual(unit_convert("1 km to m"), "1 km = 1000 m")
        self.assertEqual(unit_convert("12 inches to ft"), "12 inches = 1 ft")

    def test_weight(self):
        self.assertEqual(unit_convert("2 kg to g"), "2 kg = 2000 g")
        self.assertEqual(unit_convert("1 lb to oz"), "1 lb = 16 oz")

    def test_temperature(self):
        self.assertEqual(unit_convert("100 c to f"), "100 c = 212 f")
        self.assertEqual(unit_convert("32 f to c"), "32 f = 0 c")
        self.assertEqual(unit_convert("0 celsius to k"), "0 celsius = 273.15 k")

    def test_miles_to_km(self):
        self.assertEqual(unit_convert("1 mile to km"), "1 mile = 1.6093 km")


if __name__ == "__main__":
    unittest.main()
