import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(
            node.to_html(),
            "<p>Hello, world!</p>"
        )

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "My Blog")
        self.assertEqual(
            node.to_html(),
            "<h1>My Blog</h1>"
        )

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(
            node.to_html(),
            "Just text"
        )

    def test_leaf_to_html_link(self):
        node = LeafNode(
            "a",
            "OpenAI",
            {
                "href": "https://openai.com"
            }
        )

        self.assertEqual(
            node.to_html(),
            '<a href="https://openai.com">OpenAI</a>'
        )

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode(
            "a",
            "Google",
            {
                "href": "https://google.com",
                "target": "_blank"
            }
        )

        self.assertEqual(
            node.to_html(),
            '<a href="https://google.com" target="_blank">Google</a>'
        )

    def test_leaf_no_value(self):
        node = LeafNode("p", None)

        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()