import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        test_prop = {
            "class": "greeting",
            "href": "https://boot.dev",
            "target": "_blank",
        }
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            test_prop
        )
        test_prop_html = ""
        for prop in test_prop:
            test_prop_html += f' {prop}="{test_prop[prop]}"'
        self.assertEqual(
            node.props_to_html(),
            test_prop_html
        )

    def test_leaf_node(self):
        test_prop = {
            "href": "https://www.google.com",
        }
        test_leaf_node = LeafNode(
            "a",
            "Click me!",
            test_prop,
        )
        test_prop_html = ""
        for prop in test_prop:
            test_prop_html += f' {prop}="{test_prop[prop]}"'
        html = f'<{test_leaf_node.tag}{test_prop_html}>{test_leaf_node.value}</{test_leaf_node.tag}>'
        self.assertEqual(
            test_leaf_node.to_html(),
            html
        )

    def test_leaf_node2(self):
        test_prop = {
        }
        test_leaf_node = LeafNode(
            "p",
            "This is a paragraph of text.",
            test_prop,
        )
        test_prop_html = ""
        for prop in test_prop:
            test_prop_html += f' {prop}="{test_prop[prop]}"'
        html = f'<{test_leaf_node.tag}{test_prop_html}>{test_leaf_node.value}</{test_leaf_node.tag}>'
        self.assertEqual(
            test_leaf_node.to_html(),
            html
        )

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_parent(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
    unittest.main()
