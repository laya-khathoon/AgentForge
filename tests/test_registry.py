"""Offline tests for the tool registry."""
import unittest

from app.tools.registry import TOOLS, ToolError, run_tool


class RegistryTests(unittest.TestCase):
    def test_clock_is_registered_and_runs(self):
        self.assertIn("get_current_time", TOOLS)
        self.assertIsInstance(run_tool("get_current_time"), str)

    def test_word_count_is_registered_and_runs(self):
        self.assertIn("word_count", TOOLS)
        self.assertEqual(run_tool("word_count", "one two"), "2 words, 1 lines, 7 characters")

    def test_unit_convert_is_registered_and_runs(self):
        self.assertIn("unit_convert", TOOLS)
        self.assertEqual(run_tool("unit_convert", "1 km to m"), "1 km = 1000 m")

    def test_unknown_tool_is_refused(self):
        with self.assertRaises(ToolError):
            run_tool("delete_everything")


if __name__ == "__main__":
    unittest.main()
