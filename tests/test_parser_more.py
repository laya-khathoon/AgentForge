"""More offline tests for the tool request parser."""
import unittest

from app.agent.parser import parse_tool_request


class ParserMoreTests(unittest.TestCase):
    def test_argument_keeps_inner_spaces(self):
        self.assertEqual(parse_tool_request("TOOL: calculate 2 + 3 * 4"), ("calculate", "2 + 3 * 4"))

    def test_surrounding_whitespace_is_ignored(self):
        self.assertEqual(parse_tool_request("  TOOL: get_current_time  \n"), ("get_current_time", None))

    def test_none_and_empty_replies_are_not_requests(self):
        self.assertIsNone(parse_tool_request(None))
        self.assertIsNone(parse_tool_request(""))

    def test_tool_text_inside_a_sentence_is_not_a_request(self):
        self.assertIsNone(parse_tool_request("You could write TOOL: calculate 1 + 1 to add."))

    def test_upper_case_tool_name_is_refused(self):
        self.assertIsNone(parse_tool_request("TOOL: Calculate 1 + 1"))


if __name__ == "__main__":
    unittest.main()
