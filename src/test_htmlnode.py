import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(
            tag="a",
            value="Google",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_with_one_prop(self):
        node = HTMLNode(
            tag="img",
            props={
                "src": "image.png",
            },
        )

        self.assertEqual(
            node.props_to_html(),
            ' src="image.png"',
        )

    def test_props_to_html_with_none(self):
        node = HTMLNode(
            tag="p",
            value="This is a paragraph",
            props=None,
        )

        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_empty_dictionary(self):
        node = HTMLNode(
            tag="p",
            value="This is another paragraph",
            props={},
        )

        self.assertEqual(node.props_to_html(), "")

    def test_to_html_raises_not_implemented_error(self):
        node = HTMLNode(tag="p", value="Hello")

        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_contains_node_information(self):
        child = HTMLNode(tag=None, value="Child text")
        node = HTMLNode(
            tag="p",
            value=None,
            children=[child],
            props={"class": "intro"},
        )

        representation = repr(node)

        self.assertIn("tag='p'", representation)
        self.assertIn("children=", representation)
        self.assertIn("props={'class': 'intro'}", representation)


if __name__ == "__main__":
    unittest.main()