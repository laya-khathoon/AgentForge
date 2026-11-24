"""Offline tests for the word_count tool."""
import unittest

from app.tools.word_count import word_count


class WordCountTests(unittest.TestCase):
    def test_counts_words_lines_and_characters(self):
        self.assertEqual(word_count("hello brave world"), "3 words, 1 lines, 17 characters")

    def test_counts_several_lines(self):
        self.assertIn("2 lines", word_count("one two\nthree"))

    def test_extra_spaces_do_not_add_words(self):
        self.assertIn("2 words", word_count("  a    b  "))

    def test_empty_input_is_explained(self):
        self.assertIn("Nothing to count", word_count(""))
        self.assertIn("Nothing to count", word_count(None))
        self.assertIn("Nothing to count", word_count("   "))

    def test_non_text_is_refused(self):
        self.assertIn("give some text", word_count(42))

    def test_huge_text_is_refused(self):
        self.assertIn("too long", word_count("a " * 20000))


if __name__ == "__main__":
    unittest.main()
