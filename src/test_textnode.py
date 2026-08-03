import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)

    def test_not_equal_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Different text", TextType.BOLD)

        self.assertNotEqual(node, node2)

    def test_not_equal_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)

        self.assertNotEqual(node, node2)

    def test_not_equal_url(self):
        node = TextNode(
            "Boot.dev",
            TextType.LINK,
            "https://www.boot.dev",
        )
        node2 = TextNode(
            "Boot.dev",
            TextType.LINK,
            "https://example.com",
        )

        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(
            html_node.to_html(),
            "<code>print('hello')</code>",
        )

    def test_link(self):
        node = TextNode(
            "Boot.dev",
            TextType.LINK,
            "https://www.boot.dev",
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(
            html_node.props,
            {"href": "https://www.boot.dev"},
        )
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://www.boot.dev">Boot.dev</a>',
        )

    def test_image(self):
        node = TextNode(
            "A picture of a cat",
            TextType.IMAGE,
            "https://example.com/cat.png",
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://example.com/cat.png",
                "alt": "A picture of a cat",
            },
        )

    def test_invalid_text_type(self):
        node = TextNode("Invalid", "unknown")

        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()