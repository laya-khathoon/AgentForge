"""More offline tests for the clock tool."""
import unittest
from datetime import datetime

from app.tools.clock import get_current_time


class ClockMoreTests(unittest.TestCase):
    def test_midnight_shows_12_am(self):
        self.assertEqual(get_current_time(datetime(2026, 11, 24, 0, 5)), "Tuesday, 24 November 2026, 12:05 AM")

    def test_noon_shows_12_pm(self):
        self.assertEqual(get_current_time(datetime(2026, 11, 24, 12, 0)), "Tuesday, 24 November 2026, 12:00 PM")


if __name__ == "__main__":
    unittest.main()
