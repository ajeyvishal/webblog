from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")

        children_html = ""

        for child in self.children:
            children_html += child.to_html()

        return (
            f"<{self.tag}{self.props_to_html()}>"
            f"{children_html}"
            f"</{self.tag}>"
        )

    def __repr__(self):
        return (
            f"ParentNode("
            f"tag={self.tag!r}, "
            f"children={self.children!r}, "
            f"props={self.props!r}"
            f")"
        )