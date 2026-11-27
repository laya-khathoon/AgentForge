"""Offline tests for the date_diff tool."""
import unittest

from app.tools.date_diff import date_diff


class DateDiffTests(unittest.TestCase):
    def test_later_date(self):
        self.assertEqual(
            date_diff("2026-11-27 to 2026-12-25"),
            "2026-12-25 is 28 days (4 weeks) later than 2026-11-27",
        )

    def test_earlier_date(self):
        self.assertEqual(
            date_diff("2026-12-25 to 2026-12-24"),
            "2026-12-24 is 1 day earlier than 2026-12-25",
        )

    def test_weeks_and_days(self):
        self.assertIn("10 days (1 week 3 days)", date_diff("2026-01-01 to 2026-01-11"))

    def test_same_day(self):
        self.assertIn("same day", date_diff("2026-05-05 to 2026-05-05"))

    def test_leap_year(self):
        self.assertIn("366 days", date_diff("2024-01-01 to 2025-01-01"))


if __name__ == "__main__":
    unittest.main()
