import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_different_content(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_empty_content(self):
        node = TextNode("", TextType.BOLD)
        node2 = TextNode("", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_empty_content_different_type(self):
        node = TextNode("", TextType.BOLD)
        node2 = TextNode("", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_link_null_url(self):
        node = TextNode("This is a link", TextType.LINK, url=None)
        node2 = TextNode("This is a link", TextType.LINK)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
