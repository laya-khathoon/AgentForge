"""Offline tests for the tool registry."""
import unittest

from app.tools.registry import TOOLS, ToolError, run_tool


class RegistryTests(unittest.TestCase):
    def test_clock_is_registered_and_runs(self):
        self.assertIn("get_current_time", TOOLS)
        self.assertIsInstance(run_tool("get_current_time"), str)

    def test_unknown_tool_is_refused(self):
        with self.assertRaises(ToolError):
            run_tool("delete_everything")


if __name__ == "__main__":
    unittest.main()
