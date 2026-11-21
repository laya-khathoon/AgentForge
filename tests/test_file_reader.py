"""Offline tests for the read-only project file tool."""
import unittest

from app.tools.file_reader import FileReadError, read_project_file
from app.tools.registry import run_tool


class FileReaderTests(unittest.TestCase):
    def test_reads_a_project_file(self):
        self.assertIn("AgentForge", read_project_file("README.md"))

    def test_reads_a_nested_file(self):
        self.assertIn("ChatError", read_project_file("app/main.py"))

    def test_refuses_paths_outside_the_project(self):
        for bad in ("../README.md", "..\\outside.txt", "/etc/passwd"):
            with self.subTest(bad=bad):
                with self.assertRaises(FileReadError):
                    read_project_file(bad)

    def test_refuses_hidden_files(self):
        for bad in (".env", ".git/config", ".gitignore"):
            with self.subTest(bad=bad):
                with self.assertRaises(FileReadError):
                    read_project_file(bad)

    def test_refuses_missing_and_non_text_files(self):
        with self.assertRaises(FileReadError):
            read_project_file("does-not-exist.py")
        with self.assertRaises(FileReadError):
            read_project_file("LICENSE")  # no text suffix
        with self.assertRaises(FileReadError):
            read_project_file("")

    def test_refusals_become_text_results_through_the_registry(self):
        result = run_tool("read_project_file", ".env")
        self.assertTrue(result.startswith("File tool:"))


if __name__ == "__main__":
    unittest.main()
