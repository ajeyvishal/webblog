import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span></div>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode(None, "This is "),
                LeafNode("b", "bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " text."),
            ],
        )

        self.assertEqual(
            parent_node.to_html(),
            "<p>This is <b>bold</b> and <i>italic</i> text.</p>",
        )

    def test_to_html_with_props(self):
        parent_node = ParentNode(
            "div",
            [LeafNode("p", "Hello")],
            {
                "class": "content",
                "id": "main",
            },
        )

        self.assertEqual(
            parent_node.to_html(),
            '<div class="content" id="main"><p>Hello</p></div>',
        )

    def test_to_html_with_nested_parent_nodes(self):
        parent_node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode(None, "Nested "),
                                LeafNode("strong", "content"),
                            ],
                        )
                    ],
                )
            ],
        )

        self.assertEqual(
            parent_node.to_html(),
            "<div><section><p>Nested <strong>content</strong></p></section></div>",
        )

    def test_to_html_with_no_tag(self):
        parent_node = ParentNode(
            None,
            [LeafNode("span", "child")],
        )

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_children_none(self):
        parent_node = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_empty_children_list(self):
        parent_node = ParentNode("div", [])

        self.assertEqual(
            parent_node.to_html(),
            "<div></div>",
        )

    def test_to_html_with_link_child(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode(None, "Visit "),
                LeafNode(
                    "a",
                    "Boot.dev",
                    {"href": "https://www.boot.dev"},
                ),
            ],
        )

        self.assertEqual(
            parent_node.to_html(),
            '<p>Visit <a href="https://www.boot.dev">Boot.dev</a></p>',
        )

    def test_repr_contains_parent_information(self):
        parent_node = ParentNode(
            "div",
            [LeafNode("span", "child")],
            {"class": "wrapper"},
        )

        representation = repr(parent_node)

        self.assertIn("tag='div'", representation)
        self.assertIn("children=", representation)
        self.assertIn("props={'class': 'wrapper'}", representation)


if __name__ == "__main__":
    unittest.main()