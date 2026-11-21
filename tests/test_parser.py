"""Offline tests for the tool request parser."""
import unittest

from app.agent.parser import parse_tool_request


class ParserTests(unittest.TestCase):
    def test_request_without_argument(self):
        self.assertEqual(parse_tool_request("TOOL: get_current_time"),
                         ("get_current_time", None))
        self.assertEqual(parse_tool_request("  TOOL:get_current_time \n"),
                         ("get_current_time", None))

    def test_request_with_argument(self):
        self.assertEqual(parse_tool_request("TOOL: calculate 2 + 3 * 4"),
                         ("calculate", "2 + 3 * 4"))
        self.assertEqual(parse_tool_request("TOOL: read_project_file README.md"),
                         ("read_project_file", "README.md"))

    def test_normal_text_is_not_a_request(self):
        for reply in ("Hello!", "", None, "Sure. TOOL: get_current_time", "TOOL:"):
            with self.subTest(reply=reply):
                self.assertIsNone(parse_tool_request(reply))


if __name__ == "__main__":
    unittest.main()
