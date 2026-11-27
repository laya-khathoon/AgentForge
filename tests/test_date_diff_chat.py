"""Offline test: the chat loop can use date_diff and feed the result back."""
import unittest
from unittest.mock import Mock

from app.agent.tool_chat import TOOL_PROMPT, answer_with_tools


class DateDiffChatTests(unittest.TestCase):
    def test_prompt_mentions_the_tool(self):
        self.assertIn("date_diff", TOOL_PROMPT)
        self.assertIn("six tools", TOOL_PROMPT)

    def test_chat_runs_the_tool_and_returns_the_final_reply(self):
        chat_fn = Mock(side_effect=["TOOL: date_diff 2026-01-01 to 2026-01-08", "One week later."])
        reply = answer_with_tools(chat_fn, [{"role": "user", "content": "gap?"}], "m")
        self.assertEqual(reply, "One week later.")
        second_call_messages = chat_fn.call_args_list[1][0][0]
        self.assertIn("7 days (1 week)", second_call_messages[-1]["content"])


if __name__ == "__main__":
    unittest.main()
