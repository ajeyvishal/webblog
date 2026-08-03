import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode(
                "This is text with a ",
                TextType.TEXT,
            ),
            TextNode(
                "code block",
                TextType.CODE,
            ),
            TextNode(
                " word",
                TextType.TEXT,
            ),
        ]

        self.assertEqual(result, expected)

    def test_split_bold(self):
        node = TextNode(
            "This has **bold text** inside it",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" inside it", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_split_italic(self):
        node = TextNode(
            "This has _italic text_ inside it",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "_",
            TextType.ITALIC,
        )

        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" inside it", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_multiple_delimited_sections(self):
        node = TextNode(
            "Use `print()` and `input()` here",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("Use ", TextType.TEXT),
            TextNode("print()", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("input()", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_non_text_node_is_unchanged(self):
        node = TextNode(
            "already bold",
            TextType.BOLD,
        )

        result = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(result, [node])

    def test_mixed_input_nodes(self):
        nodes = [
            TextNode(
                "Normal with `code`",
                TextType.TEXT,
            ),
            TextNode(
                "already bold",
                TextType.BOLD,
            ),
        ]

        result = split_nodes_delimiter(
            nodes,
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("Normal with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("already bold", TextType.BOLD),
        ]

        self.assertEqual(result, expected)

    def test_delimiter_at_start_and_end(self):
        node = TextNode(
            "`all code`",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("all code", TextType.CODE),
        ]

        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode(
            "Plain text only",
            TextType.TEXT,
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        expected = [
            TextNode("Plain text only", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_missing_closing_delimiter(self):
        node = TextNode(
            "This has an `unclosed code section",
            TextType.TEXT,
        )

        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                [node],
                "`",
                TextType.CODE,
            )

class TestExtractMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):

        matches = extract_markdown_images(

            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"

        )

        self.assertListEqual(

            [("image", "https://i.imgur.com/zjjcJKZ.png")],

            matches,

        )

    def test_extract_multiple_images(self):

        matches = extract_markdown_images(

            "This is text with a "

            "![rick roll](https://i.imgur.com/aKaOqIh.gif) "

            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        )

        self.assertListEqual(

            [

                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),

                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),

            ],

            matches,

        )

    def test_extract_markdown_links(self):

        matches = extract_markdown_links(

            "This is text with a link "

            "[to boot dev](https://www.boot.dev)"

        )

        self.assertListEqual(

            [("to boot dev", "https://www.boot.dev")],

            matches,

        )

    def test_extract_multiple_links(self):

        matches = extract_markdown_links(

            "This is text with a link "

            "[to boot dev](https://www.boot.dev) "

            "and [to youtube](https://www.youtube.com/@bootdotdev)"

        )

        self.assertListEqual(

            [

                ("to boot dev", "https://www.boot.dev"),

                (

                    "to youtube",

                    "https://www.youtube.com/@bootdotdev",

                ),

            ],

            matches,

        )

    def test_images_are_not_extracted_as_links(self):

        matches = extract_markdown_links(

            "This has ![an image](https://example.com/image.png) "

            "and [a link](https://example.com)"

        )

        self.assertListEqual(

            [("a link", "https://example.com")],

            matches,

        )

    def test_no_images(self):

        matches = extract_markdown_images(

            "This text contains no images."

        )

        self.assertListEqual([], matches)

    def test_no_links(self):

        matches = extract_markdown_links(

            "This text contains no links."

        )

        self.assertListEqual([], matches)

    def test_empty_alt_text(self):

        matches = extract_markdown_images(

            "![](https://example.com/image.png)"

        )

        self.assertListEqual(

            [("", "https://example.com/image.png")],

            matches,

        )

    def test_empty_anchor_text(self):

        matches = extract_markdown_links(

            "[](https://example.com)"

        )

        self.assertListEqual(

            [("", "https://example.com")],

            matches,

        )
class TestSplitNodesImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an "
            "![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another "
            "![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode(
                    "This is text with an ",
                    TextType.TEXT,
                ),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(
                    " and another ",
                    TextType.TEXT,
                ),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        node = TextNode(
            "Before ![cat](cat.png) after",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode(
                    "cat",
                    TextType.IMAGE,
                    "cat.png",
                ),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_start(self):
        node = TextNode(
            "![cat](cat.png) after",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode(
                    "cat",
                    TextType.IMAGE,
                    "cat.png",
                ),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode(
            "Before ![cat](cat.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode(
                    "cat",
                    TextType.IMAGE,
                    "cat.png",
                ),
            ],
            new_nodes,
        )

    def test_only_image(self):
        node = TextNode(
            "![cat](cat.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode(
                    "cat",
                    TextType.IMAGE,
                    "cat.png",
                ),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode(
            "Plain text without images",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual([node], new_nodes)

    def test_image_does_not_split_non_text_node(self):
        node = TextNode(
            "![cat](cat.png)",
            TextType.BOLD,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual([node], new_nodes)

    def test_multiple_input_nodes_with_images(self):
        nodes = [
            TextNode(
                "First ![one](one.png)",
                TextType.TEXT,
            ),
            TextNode(
                "Second ![two](two.png)",
                TextType.TEXT,
            ),
        ]

        new_nodes = split_nodes_image(nodes)

        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode(
                    "one",
                    TextType.IMAGE,
                    "one.png",
                ),
                TextNode("Second ", TextType.TEXT),
                TextNode(
                    "two",
                    TextType.IMAGE,
                    "two.png",
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link "
            "[to boot dev](https://www.boot.dev) "
            "and "
            "[to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "This is text with a link ",
                    TextType.TEXT,
                ),
                TextNode(
                    "to boot dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube",
                    TextType.LINK,
                    "https://www.youtube.com/@bootdotdev",
                ),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev) today",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" today", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_start(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev) is useful",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
                TextNode(" is useful", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode(
            "Visit [Boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
            ],
            new_nodes,
        )

    def test_only_link(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://www.boot.dev",
                ),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode(
            "Plain text without links",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual([node], new_nodes)

    def test_link_does_not_split_non_text_node(self):
        node = TextNode(
            "[Boot.dev](https://www.boot.dev)",
            TextType.CODE,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual([node], new_nodes)

    def test_images_are_not_split_as_links(self):
        node = TextNode(
            "An ![image](image.png) is here",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual([node], new_nodes)

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word and a "
            "`code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://boot.dev",
                ),
            ],
            nodes,
        )

    def test_plain_text(self):
        nodes = text_to_textnodes("This is plain text")

        self.assertListEqual(
            [
                TextNode(
                    "This is plain text",
                    TextType.TEXT,
                )
            ],
            nodes,
        )

    def test_only_bold(self):
        nodes = text_to_textnodes("**bold**")

        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
            ],
            nodes,
        )

    def test_multiple_format_types(self):
        nodes = text_to_textnodes(
            "**bold** _italic_ `code`"
        )

        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            nodes,
        )

    def test_multiple_links_and_images(self):
        nodes = text_to_textnodes(
            "See [Boot.dev](https://boot.dev), "
            "![cat](cat.png), and "
            "[Python](https://python.org)."
        )

        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://boot.dev",
                ),
                TextNode(", ", TextType.TEXT),
                TextNode(
                    "cat",
                    TextType.IMAGE,
                    "cat.png",
                ),
                TextNode(", and ", TextType.TEXT),
                TextNode(
                    "Python",
                    TextType.LINK,
                    "https://python.org",
                ),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
        )

    def test_invalid_unclosed_bold(self):
        with self.assertRaises(ValueError):
            text_to_textnodes(
                "This has **unclosed bold text"
            )

    def test_invalid_unclosed_italic(self):
        with self.assertRaises(ValueError):
            text_to_textnodes(
                "This has _unclosed italic text"
            )

    def test_invalid_unclosed_code(self):
        with self.assertRaises(ValueError):
            text_to_textnodes(
                "This has `unclosed code"
            )

            
if __name__ == "__main__":
    unittest.main()

