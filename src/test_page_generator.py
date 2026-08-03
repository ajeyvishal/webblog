import unittest

from page_generator import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"

        self.assertEqual(
            extract_title(markdown),
            "Hello",
        )

    def test_extract_title_strips_whitespace(self):
        markdown = "#    My Page Title   "

        self.assertEqual(
            extract_title(markdown),
            "My Page Title",
        )

    def test_extract_title_from_full_document(self):
        markdown = """
This is a paragraph.

# Tolkien Fan Club

More text here.
"""

        self.assertEqual(
            extract_title(markdown),
            "Tolkien Fan Club",
        )

    def test_ignores_h2(self):
        markdown = """
## This is an H2

# This is the H1
"""

        self.assertEqual(
            extract_title(markdown),
            "This is the H1",
        )

    def test_missing_h1_raises_error(self):
        markdown = """
## Only an H2

This is a paragraph.
"""

        with self.assertRaises(ValueError):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()