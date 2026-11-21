"""Offline tests for passing a tool argument through the answer loop."""
import unittest
from unittest.mock import Mock

from app.agent.tool_chat import answer_with_tools


class ToolArgumentTests(unittest.TestCase):
    def test_calculate_runs_end_to_end(self):
        fake = Mock(side_effect=["TOOL: calculate 6 * 7", "That is 42."])
        answer = answer_with_tools(fake, [{"role": "user", "content": "6*7?"}], "m")
        self.assertEqual(answer, "That is 42.")
        followup = fake.call_args_list[1].args[0]
        self.assertIn("Tool result: 42", followup[-1]["content"])

    def test_tool_without_argument_still_works(self):
        fake = Mock(side_effect=["TOOL: get_current_time", "It is late."])
        answer = answer_with_tools(fake, [{"role": "user", "content": "Time?"}], "m")
        self.assertEqual(answer, "It is late.")


if __name__ == "__main__":
    unittest.main()
