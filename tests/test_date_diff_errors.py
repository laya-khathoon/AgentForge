"""Offline tests for date_diff error messages."""
import unittest

from app.tools.date_diff import date_diff


class DateDiffErrorTests(unittest.TestCase):
    def test_empty_and_none(self):
        self.assertTrue(date_diff("").startswith("Nothing to compare"))
        self.assertTrue(date_diff(None).startswith("Nothing to compare"))

    def test_not_text(self):
        self.assertTrue(date_diff(5).startswith("Cannot compare"))

    def test_missing_to(self):
        self.assertIn("use the form", date_diff("2026-01-01 2026-01-02"))

    def test_not_a_real_date(self):
        self.assertIn("real calendar dates", date_diff("2026-02-30 to 2026-03-01"))
        self.assertIn("real calendar dates", date_diff("tomorrow to today"))

    def test_too_long(self):
        self.assertIn("too long", date_diff("2026-01-01 to 2026-01-02 " + "x" * 200))


if __name__ == "__main__":
    unittest.main()
