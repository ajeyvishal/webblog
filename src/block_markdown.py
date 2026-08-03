from enum import Enum
from inline_markdown import text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")
    blocks = []

    for block in raw_blocks:
        stripped_block = block.strip()

        if stripped_block != "":
            blocks.append(stripped_block)

    return blocks


def block_to_block_type(block: str) -> BlockType:
    # Heading: 1–6 # characters, followed by a space
    if block.startswith("#"):
        heading_parts = block.split(" ", 1)
        heading_marker = heading_parts[0]

        if (
            len(heading_parts) == 2
            and 1 <= len(heading_marker) <= 6
            and heading_marker == "#" * len(heading_marker)
        ):
            return BlockType.HEADING

    # Multiline code block
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    # Quote: every line starts with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: lines must start with 1., 2., 3., ...
    is_ordered_list = True

    for index, line in enumerate(lines, start=1):
        expected_prefix = f"{index}. "

        if not line.startswith(expected_prefix):
            is_ordered_list = False
            break

    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text: str) -> list:
    text_nodes = text_to_textnodes(text)
    html_nodes = []

    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes


def heading_to_html_node(block: str) -> ParentNode:
    heading_level = 0

    for character in block:
        if character == "#":
            heading_level += 1
        else:
            break

    heading_text = block[heading_level + 1 :]

    return ParentNode(
        f"h{heading_level}",
        text_to_children(heading_text),
    )


def paragraph_to_html_node(block: str) -> ParentNode:
    paragraph_text = block.replace("\n", " ")

    return ParentNode(
        "p",
        text_to_children(paragraph_text),
    )


def code_to_html_node(block: str) -> ParentNode:
    code_text = block[4:-3]

    code_text_node = TextNode(
        code_text,
        TextType.TEXT,
    )
    code_html_node = text_node_to_html_node(code_text_node)

    return ParentNode(
        "pre",
        [
            LeafNode(
                "code",
                code_html_node.value,
            )
        ],
    )


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    quote_lines = []

    for line in lines:
        quote_lines.append(line[1:].strip())

    quote_text = " ".join(quote_lines)

    return ParentNode(
        "blockquote",
        text_to_children(quote_text),
    )


def unordered_list_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    list_items = []

    for line in lines:
        item_text = line[2:]

        list_items.append(
            ParentNode(
                "li",
                text_to_children(item_text),
            )
        )

    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    list_items = []

    for line in lines:
        item_text = line.split(". ", 1)[1]

        list_items.append(
            ParentNode(
                "li",
                text_to_children(item_text),
            )
        )

    return ParentNode("ol", list_items)


def block_to_html_node(block: str):
    block_type = block_to_block_type(block)

    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)

    if block_type == BlockType.CODE:
        return code_to_html_node(block)

    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)

    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)

    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)

    raise ValueError(f"Unsupported block type: {block_type}")


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_nodes.append(block_to_html_node(block))

    return ParentNode("div", block_nodes)