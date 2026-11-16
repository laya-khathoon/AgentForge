"""Offline tests for the terminal loop and Ollama HTTP contract."""
import io
import json
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

from app.main import ChatError, MAX_TURNS, chat, main, run_chat


class ChatClientTests(unittest.TestCase):
    @patch("app.main.urlopen")
    def test_sends_local_non_streaming_request_and_reads_reply(self, open_url):
        open_url.return_value.__enter__.return_value = io.BytesIO(
            b'{"message": {"role": "assistant", "content": " Hello "}}')
        messages = [{"role": "user", "content": "Hi"}]
        self.assertEqual(chat(messages, model="test-model"), "Hello")
        request = open_url.call_args.args[0]
        self.assertEqual(request.full_url, "http://127.0.0.1:11434/api/chat")
        self.assertEqual(request.method, "POST")
        self.assertEqual(json.loads(request.data), {
            "model": "test-model", "messages": messages, "stream": False})
        self.assertEqual(open_url.call_args.kwargs["timeout"], 120)

    def test_missing_model_and_server_errors_are_friendly(self):
        for status in (404, 500):
            with self.subTest(status=status):
                error = HTTPError("local", status, "failed", None, None)
                with patch("app.main.urlopen", side_effect=error):
                    with self.assertRaises(ChatError) as caught:
                        chat([], model="test-model")
                expected = "ollama pull test-model" if status == 404 else "HTTP 500"
                self.assertIn(expected, str(caught.exception))

    def test_unavailable_server_and_timeout(self):
        for error in (URLError("offline"), TimeoutError()):
            with self.subTest(error=error):
                with patch("app.main.urlopen", side_effect=error):
                    with self.assertRaisesRegex(ChatError, "Cannot reach Ollama"):
                        chat([])

    def test_invalid_response_and_missing_content(self):
        for body in (b"not json", b"{}", b"[]", b'{"message": null}',
                     b'{"message": {"content": " "}}'):
            with self.subTest(body=body):
                with patch("app.main.urlopen") as open_url:
                    open_url.return_value.__enter__.return_value = io.BytesIO(body)
                    with self.assertRaises(ChatError):
                        chat([])


class TerminalTests(unittest.TestCase):
    def session(self, entries, responder):
        output = []
        run_chat("test-model", input_fn=Mock(side_effect=entries),
                 output_fn=output.append, chat_fn=responder)
        return output

    def test_multiturn_history_and_exit(self):
        responder = Mock(side_effect=["First reply", "Second reply"])
        output = self.session(["Hi", "Follow up", "/exit"], responder)
        self.assertIn("AgentForge: First reply", output)
        messages = responder.call_args_list[1].args[0]
        self.assertEqual([m["role"] for m in messages],
                         ["system", "user", "assistant", "user"])
        self.assertEqual(messages[2]["content"], "First reply")
        self.assertEqual(output[-1], "Goodbye.")

    def test_blank_reset_and_failed_turn_not_retained(self):
        responder = Mock(side_effect=[ChatError("offline"), "OK", "New reply"])
        self.session([" ", "failed", "works", "/reset", "fresh", "/exit"], responder)
        self.assertEqual(len(responder.call_args_list), 3)
        second = responder.call_args_list[1].args[0]
        third = responder.call_args_list[2].args[0]
        self.assertEqual([m["content"] for m in second[1:]], ["works"])
        self.assertEqual([m["content"] for m in third[1:]], ["fresh"])

    def test_history_is_bounded_to_complete_turns(self):
        responder = Mock(return_value="OK")
        self.session([str(i) for i in range(MAX_TURNS + 4)] + ["/exit"], responder)
        last = responder.call_args.args[0]
        self.assertEqual(len(last), 2 * MAX_TURNS + 2)
        self.assertEqual(last[0]["role"], "system")
        self.assertEqual(last[1]["role"], "user")

    def test_eof_and_keyboard_interrupt_exit_cleanly(self):
        for exception in (EOFError(), KeyboardInterrupt()):
            responder = Mock()
            output = self.session([exception], responder)
            responder.assert_not_called()
            self.assertEqual(output[-1], "Goodbye.")

    @patch("app.main.run_chat")
    def test_cli_model_option(self, run):
        with patch("sys.argv", ["agentforge", "--model", "custom-model"]):
            main()
        run.assert_called_once_with("custom-model")


if __name__ == "__main__":
    unittest.main()
