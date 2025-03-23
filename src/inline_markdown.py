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


def split_nodes_image(old_nodes):
    result = []

    for old_node in old_nodes:
        # Only process text nodes
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        # Find all image matches in this node
        result.extend(extract_images_from_text(old_node.text))

    return result


def extract_images_from_text(text):
    # Base case: no more images to find
    matches = extract_markdown_images(text)
    if not matches:
        # Return the text as a node if it's not empty
        if text:
            return [TextNode(text, TextType.TEXT)]
        return []

    # Get the first match
    alt_text, url = matches[0]
    image_markdown = f"![{alt_text}]({url})"

    # Split text into before, image, and after
    parts = text.split(image_markdown, 1)
    before_text = parts[0]
    after_text = parts[1] if len(parts) > 1 else ""

    result = []
    # Add the text before the image if not empty
    if before_text:
        result.append(TextNode(before_text, TextType.TEXT))

    # Add the image node
    result.append(TextNode(alt_text, TextType.IMAGE, url))

    # Recursively process any text after the image
    result.extend(extract_images_from_text(after_text))

    return result


def split_nodes_link(old_nodes):
    result = []

    for old_node in old_nodes:
        # Only process text nodes
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        # Find all link matches in this node
        result.extend(extract_links_from_text(old_node.text))

    return result


def extract_links_from_text(text):
    # Base case: no more links to find
    matches = extract_markdown_links(text)
    if not matches:
        # Return the text as a node if it's not empty
        if text:
            return [TextNode(text, TextType.TEXT)]
        return []

    # Get the first match
    link_text, url = matches[0]
    link_markdown = f"[{link_text}]({url})"

    # Split text into before, link, and after
    parts = text.split(link_markdown, 1)
    before_text = parts[0]
    after_text = parts[1] if len(parts) > 1 else ""

    result = []
    # Add the text before the link if not empty
    if before_text:
        result.append(TextNode(before_text, TextType.TEXT))

    # Add the link node
    result.append(TextNode(link_text, TextType.LINK, url))

    # Recursively process any text after the link
    result.extend(extract_links_from_text(after_text))

    return result


def text_to_textnodes(text):

    # Handle each of the different type of text nodes
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes
