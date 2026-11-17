"""Offline test for the /tools command."""
import unittest
from unittest.mock import Mock

from app.main import run_chat


class ToolsCommandTests(unittest.TestCase):
    def test_tools_command_lists_tools_without_calling_the_model(self):
        output = []
        responder = Mock()
        run_chat("m", input_fn=Mock(side_effect=["/tools", "/exit"]),
                 output_fn=output.append, chat_fn=responder)
        self.assertIn("Tools: get_current_time", output)
        responder.assert_not_called()


if __name__ == "__main__":
    unittest.main()
