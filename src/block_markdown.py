from enum import Enum
from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    ULIST = 'unordered_list'
    OLIST = 'ordered_list'


def markdown_to_blocks(markdown):
    # Split the markdown text into blocks based on double newlines
    blocks = markdown.split("\n\n")
    # Remove leading and trailing whitespace from each block
    blocks = [block.lstrip().rstrip() for block in blocks]
    # Remove empty blocks
    blocks = [block for block in blocks if block]

    return blocks


def block_to_block_type(block):
    # Check for heading
    if block.startswith("#"):
        if block.split(" ", 1)[0].count("#") in range(1, 7):
            return BlockType.HEADING

    # Check for code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Check for quote block
    if all(line.startswith(">") for line in block.splitlines()):
        return BlockType.QUOTE

    # Check for unordered list block
    if all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.ULIST

    # Check for ordered list block
    lines = block.splitlines()
    if all(
        line.split(". ", 1)[0].isdigit() and int(
            line.split(". ", 1)[0]) == i + 1
        for i, line in enumerate(lines)
    ):
        return BlockType.OLIST

    # Default to paragraph
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def extract_title(markdown):
    # Pulls the h1 header from the markdown file. if there is no h1 header, it raises and exception.
    markdown_heading = ""
    for line in markdown.splitlines():
        if line.startswith("# "):
            markdown_heading = line[1:].strip()
    if markdown_heading == "":
        raise ValueError("No h1 header found in markdown file.")
    return markdown_heading
