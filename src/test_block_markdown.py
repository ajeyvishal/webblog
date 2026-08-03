import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                (
                    "This is another paragraph with _italic_ text "
                    "and `code` here\n"
                    "This is the same paragraph on a new line"
                ),
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a normal paragraph."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_multiline_paragraph(self):
        block = "This is line one.\nThis is line two."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_heading_one(self):
        block = "# Heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_heading_six(self):
        block = "###### Heading level six"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_heading_too_many_hashes(self):
        block = "####### Not a heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_heading_without_space(self):
        block = "###Not a heading"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_code(self):
        block = "```\nprint('hello')\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_code_without_newline_after_opening(self):
        block = "```print('hello')\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_unclosed_code(self):
        block = "```\nprint('hello')"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_quote(self):
        block = ">This is a quote\n> This is another line"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_invalid_quote(self):
        block = "> This starts as a quote\nThis line does not"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self):
        block = "- First item\n- Second item\n- Third item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_invalid_unordered_list(self):
        block = "- First item\nSecond item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_wrong_start(self):
        block = "2. First item\n3. Second item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_wrong_sequence(self):
        block = "1. First item\n3. Third item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_missing_space(self):
        block = "1.First item\n2.Second item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()