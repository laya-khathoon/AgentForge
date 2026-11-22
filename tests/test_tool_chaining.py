"""Offline tests for chained tool calls in one answer, using a fake model."""
import unittest
from unittest.mock import Mock

from app.agent.tool_chat import MAX_TOOL_CALLS, answer_with_tools


class ToolChainingTests(unittest.TestCase):
    def test_two_tools_chain_in_one_answer(self):
        fake = Mock(side_effect=[
            "TOOL: calculate 2 + 3",
            "TOOL: calculate 5 * 4",
            "2 + 3 is 5 and 5 * 4 is 20.",
        ])
        answer = answer_with_tools(fake, [{"role": "user", "content": "Both?"}], "m")
        self.assertEqual(answer, "2 + 3 is 5 and 5 * 4 is 20.")
        self.assertEqual(fake.call_count, 3)
        # Each later call sees every earlier tool result.
        third = fake.call_args_list[2].args[0]
        results = [m["content"] for m in third if "Tool result:" in m["content"]]
        self.assertEqual(len(results), 2)

    def test_tool_cap_stops_endless_requests(self):
        fake = Mock(side_effect=["TOOL: get_current_time"] * 10)
        answer = answer_with_tools(fake, [{"role": "user", "content": "Time?"}], "m")
        self.assertIn("tool limit", answer)
        # MAX_TOOL_CALLS tool rounds plus one forced final answer.
        self.assertEqual(fake.call_count, MAX_TOOL_CALLS + 1)
        last = fake.call_args_list[-1].args[0]
        self.assertIn("tool limit", last[-1]["content"])

    def test_tool_result_earlier_then_plain_answer(self):
        fake = Mock(side_effect=["TOOL: calculate 7 * 6", "The answer is 42."])
        answer = answer_with_tools(fake, [{"role": "user", "content": "7*6?"}], "m")
        self.assertEqual(answer, "The answer is 42.")
        self.assertEqual(fake.call_count, 2)


if __name__ == "__main__":
    unittest.main()
