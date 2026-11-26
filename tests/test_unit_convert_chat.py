"""Offline test: the chat loop can use unit_convert and feed the result back."""
import unittest
from unittest.mock import Mock

from app.agent.tool_chat import TOOL_PROMPT, answer_with_tools


class UnitConvertChatTests(unittest.TestCase):
    def test_prompt_mentions_the_tool(self):
        self.assertIn("unit_convert", TOOL_PROMPT)

    def test_chat_runs_the_tool_and_returns_the_final_reply(self):
        chat_fn = Mock(side_effect=["TOOL: unit_convert 2 kg to g", "That is 2000 grams."])
        reply = answer_with_tools(chat_fn, [{"role": "user", "content": "2 kg in g?"}], "m")
        self.assertEqual(reply, "That is 2000 grams.")
        second_call_messages = chat_fn.call_args_list[1][0][0]
        self.assertIn("2 kg = 2000 g", second_call_messages[-1]["content"])


if __name__ == "__main__":
    unittest.main()
