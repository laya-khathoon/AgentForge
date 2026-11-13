import io
import unittest
from contextlib import redirect_stdout

from app.main import main


class MainTest(unittest.TestCase):
    def test_main_prints_startup_messages(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            main()
        lines = buffer.getvalue().splitlines()
        self.assertEqual(lines[0], "AgentForge Autonomous AI Agent")
        self.assertEqual(lines[1], "Project environment is working!")
        self.assertEqual(len(lines), 3)


if __name__ == "__main__":
    unittest.main()
