"""Offline tests for the clock tool."""
import unittest
from datetime import datetime

from app.tools.clock import get_current_time


class ClockToolTests(unittest.TestCase):
    def test_formats_a_fixed_time(self):
        fixed = datetime(2026, 11, 17, 18, 30)
        self.assertEqual(get_current_time(fixed), "Tuesday, 17 November 2026, 06:30 PM")

    def test_returns_text_for_real_time(self):
        self.assertIsInstance(get_current_time(), str)


if __name__ == "__main__":
    unittest.main()
