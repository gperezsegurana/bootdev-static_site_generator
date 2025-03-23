from enum import Enum


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
# if __name__ == "__main__":
#     def main():
#         text = (
#             "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and _italic_words inside of it.\n\n- This is the first list item in a list blockn\n- This is a list item\n- This is another list item"
#         )
#         blocks = markdown_to_blocks(text)
#         print("Markdown:")
#         print("--------")
#         print(text)
#         print("\nBlocks:")
#         print("------")
#         print(blocks)

#     main()
