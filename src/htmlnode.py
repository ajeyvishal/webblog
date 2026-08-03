class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("The to_html method must be implemented by a child class")

    def props_to_html(self):
        if not self.props:
            return ""

        attributes = ""
        for key, value in self.props.items():
            attributes += f' {key}="{value}"'

        return attributes

    def __repr__(self):
        return (
            f"HTMLNode("
            f"tag={self.tag!r}, "
            f"value={self.value!r}, "
            f"children={self.children!r}, "
            f"props={self.props!r}"
            f")"
        )