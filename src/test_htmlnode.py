import unittest
from htmlnode import HTMLnode


class TestHTMLnode(unittest.TestCase):
    def test_initialization(self):
        node = HTMLnode(tag="div", value="Hello", children=[],
                        props={"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    def test_props_to_html(self):
        node = HTMLnode(props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

    def test_props_to_html_empty(self):
        node = HTMLnode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLnode(tag="p", value="Text", children=None,
                        props={"style": "color:red;"})
        self.assertEqual(
            repr(node),
            "HTMLnode(tag=p, value=Text, children=None, props={'style': 'color:red;'})"
        )

    def test_to_html_not_implemented(self):
        node = HTMLnode()
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
