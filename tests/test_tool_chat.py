"""Offline tests for the tool-using answer loop, using a fake model."""
import unittest
from unittest.mock import Mock

from app.agent.tool_chat import answer_with_tools


class ToolChatTests(unittest.TestCase):
    def test_plain_answer_makes_one_call(self):
        fake = Mock(return_value="Hi there")
        self.assertEqual(answer_with_tools(fake, [{"role": "user", "content": "Hi"}], "m"),
                         "Hi there")
        self.assertEqual(fake.call_count, 1)

    def test_tool_request_runs_tool_and_asks_again(self):
        fake = Mock(side_effect=["TOOL: get_current_time", "It is late."])
        answer = answer_with_tools(fake, [{"role": "user", "content": "Time?"}], "m")
        self.assertEqual(answer, "It is late.")
        second = fake.call_args_list[1].args[0]
        self.assertIn("Tool result:", second[-1]["content"])

    def test_unknown_tool_does_not_crash(self):
        fake = Mock(side_effect=["TOOL: nope", "Sorry, cannot."])
        self.assertEqual(answer_with_tools(fake, [], "m"), "Sorry, cannot.")
        self.assertIn("Unknown tool", fake.call_args_list[1].args[0][-1]["content"])


if __name__ == "__main__":
    unittest.main()
