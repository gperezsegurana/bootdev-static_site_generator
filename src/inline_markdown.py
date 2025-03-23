from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if node.text.count(delimiter) % 2 != 0:
                raise ValueError(
                    f"Unmatched delimiter '{delimiter}' found in text: {node.text}")
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if part:
                    new_type = text_type if i % 2 == 1 else TextType.TEXT
                    new_nodes.append(TextNode(part, new_type))
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
