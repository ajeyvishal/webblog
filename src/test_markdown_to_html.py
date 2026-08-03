import unittest

from block_markdown import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = (
            "```\n"
            "This is text that _should_ remain\n"
            "the **same** even with inline stuff\n"
            "```"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# Heading"

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading</h1></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> on two lines
"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote on two lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item one
- Item two
- Item three
"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First
2. Second
3. Third
"""

        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()