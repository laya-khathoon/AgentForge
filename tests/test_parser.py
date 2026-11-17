"""Offline tests for the tool request parser."""
import unittest

from app.agent.parser import parse_tool_request


class ParserTests(unittest.TestCase):
    def test_valid_request(self):
        self.assertEqual(parse_tool_request("TOOL: get_current_time"), "get_current_time")
        self.assertEqual(parse_tool_request("  TOOL:get_current_time \n"), "get_current_time")

    def test_normal_text_is_not_a_request(self):
        for reply in ("Hello!", "", None, "Sure. TOOL: get_current_time",
                      "TOOL: get_current_time please", "TOOL:"):
            with self.subTest(reply=reply):
                self.assertIsNone(parse_tool_request(reply))


if __name__ == "__main__":
    unittest.main()
