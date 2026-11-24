"""word_count used through the parser and the registry, like the chat does."""
import unittest

from app.agent.parser import parse_tool_request
from app.tools.registry import run_tool


class WordCountChatTests(unittest.TestCase):
    def test_request_is_parsed_and_run(self):
        name, argument = parse_tool_request("TOOL: word_count good morning everyone")
        self.assertEqual(run_tool(name, argument), "3 words, 1 lines, 21 characters")

    def test_request_without_text_is_explained(self):
        name, argument = parse_tool_request("TOOL: word_count")
        self.assertIn("Nothing to count", run_tool(name, argument))


if __name__ == "__main__":
    unittest.main()
