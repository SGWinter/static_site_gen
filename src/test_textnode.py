import unittest

from textnode import TextNode
from textnode import split_nodes_delimiter
from textnode import extract_markdown_images
from textnode import extract_markdown_links
from textnode import split_nodes_image
from textnode import split_nodes_link
from textnode import text_to_textnodes
from textnode import block_to_block_type
from textnode import markdown_to_blocks


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_text_type_not(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_eq_text_not(self):
        node = TextNode("This is not a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_eq_url_not(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://www.reddit.com")
        self.assertNotEqual(node, node2)

    def test_split_delimiter_bold(self):
        node = TextNode("Split delimiter **bold** test", "text")
        node_list = [
                TextNode("Split delimiter ", "text"),
                TextNode("bold", "bold"),
                TextNode(" test", "text"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", "bold"), node_list)

    def test_split_delimiter_bold2(self):
        node = TextNode("Split delimiter **bold** test **bold2**", "text")
        node_list = [
                TextNode("Split delimiter ", "text"),
                TextNode("bold", "bold"),
                TextNode(" test ", "text"),
                TextNode("bold2", "bold"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", "bold"), node_list)

    def test_split_delimiter_italic(self):
        node = TextNode("Split delimiter *italic* test", "text")
        node_list = [
                TextNode("Split delimiter ", "text"),
                TextNode("italic", "italic"),
                TextNode(" test", "text"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", "italic"), node_list)

    def test_split_delimiter_code(self):
        node = TextNode("Split delimiter `code` test", "text")
        node_list = [
                TextNode("Split delimiter ", "text"),
                TextNode("code", "code"),
                TextNode(" test", "text"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", "code"), node_list)

    def test_split_delimiter_no_split(self):
        node = TextNode("Split delimiter no split test", "text")
        node_list = [
                TextNode("Split delimiter no split test", "text"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", "code"), node_list)

    def test_split_delimiter_multiple(self):
        node = [
            TextNode("Split delimiter `code` test", "text"),
            TextNode("Split delimiter 2 `code2` test 2", "text"),
        ]
        node_list = [
                TextNode("Split delimiter ", "text"),
                TextNode("code", "code"),
                TextNode(" test", "text"),
                TextNode("Split delimiter 2 ", "text"),
                TextNode("code2", "code"),
                TextNode(" test 2", "text"),
        ]
        self.assertEqual(split_nodes_delimiter(node, "`", "code"), node_list)

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        text_match = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        self.assertEqual(extract_markdown_images(text), text_match)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        text_match = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(extract_markdown_links(text), text_match)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        result_node = [
            TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", "text"),
            TextNode(
                "second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
        ]
        self.assertEqual(split_nodes_image([node]), result_node)

    def test_split_nodes_image2(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            "text",
        )
        result_node = [
            TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ]
        self.assertEqual(split_nodes_image([node]), result_node)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example.com/another)",
            "text",
        )
        result_node = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "https://www.example.com"),
            TextNode(" and another ", "text"),
            TextNode("second link", "link", "https://www.example.com/another"),
        ]
        self.assertEqual(split_nodes_link([node]), result_node)

    def test_split_nodes_link2(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com)",
            "text",
        )
        result_node = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "https://www.example.com"),
        ]
        self.assertEqual(split_nodes_link([node]), result_node)

    def test_text_to_textnodes(self):
        input_text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        result_node = [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(input_text), result_node)

    def test_text_to_textnodes2(self):
        input_text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev) and another **bold** and a `code` also another *italic*"
        result_node = [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://boot.dev"),
                TextNode(" and another ", "text"),
                TextNode("bold", "bold"),
                TextNode(" and a ", "text"),
                TextNode("code", "code"),
                TextNode(" also another ", "text"),
                TextNode("italic", "italic"),
        ]
        self.assertEqual(text_to_textnodes(input_text), result_node)


    def test_split_blocks(self):
        input_text = "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"
        result_text_list = [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
        ]
        self.assertEqual(markdown_to_blocks(input_text), result_text_list)


    def test_split_blocks2(self):
        input_text = " This is **bolded** paragraph\n\n This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line \n\n * This is a list\n * with items"
        result_text_list = [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n * with items",
        ]
        self.assertEqual(markdown_to_blocks(input_text), result_text_list)

    def test_block_to_block_type_heading_1(self):
        input_block = "# Heading one"
        result_block_type = "heading"
        self.assertEqual(block_to_block_type(input_block), result_block_type)

    def test_block_to_block_type_heading_2(self):
        input_block = "## Heading one"
        result_block_type = "heading"
        self.assertEqual(block_to_block_type(input_block), result_block_type)

    def test_block_to_block_type_heading_3(self):
        input_block = "% Heading one"
        result_block_type = "heading"
        self.assertNotEqual(block_to_block_type(input_block), result_block_type)

    def test_block_to_block_type_code_1(self):
        input_block = "``` code block ```"
        result_block_type = "code"
        self.assertEqual(block_to_block_type(input_block), result_block_type)

    def test_block_to_block_type_code_2(self):
        input_block = "`` code block ``"
        result_block_type = "code"
        self.assertNotEqual(block_to_block_type(input_block), result_block_type)

    def test_block_to_block_type_quote_1(self):
        input_block = "> a nice quote"
        result_block_type = "quote"
        self.assertEqual(block_to_block_type(input_block), result_block_type)

    def test_block_to_block_type_quote_2(self):
        input_block = "< a nice quote"
        result_block_type = "quote"
        self.assertNotEqual(block_to_block_type(input_block), result_block_type)

    def test_block_to_block_type_unordered_list_1(self):
        input_block = "* unordered list 1\n* unordered list"
        result_block_type = "unordered_list"
        self.assertEqual(block_to_block_type(input_block), result_block_type)

    def test_block_to_block_type_unordered_list_2(self):
        input_block = "* unordered list 1\n- unordered list"
        result_block_type = "unordered_list"
        self.assertEqual(block_to_block_type(input_block), result_block_type)

    def test_block_to_block_type_unordered_list_3(self):
        input_block = "* unordered list 1\n_ unordered list"
        result_block_type = "unordered_list"
        self.assertNotEqual(block_to_block_type(input_block), result_block_type)

    def test_block_to_block_type_ordered_list_1(self):
        input_block = "1. ordered list\n2. ordered list"
        result_block_type = "ordered_list"
        self.assertEqual(block_to_block_type(input_block), result_block_type)

    def test_block_to_block_type_ordered_list_2(self):
        input_block = "1. ordered list\n3. ordered list"
        result_block_type = "ordered_list"
        self.assertNotEqual(block_to_block_type(input_block), result_block_type)

if __name__ == "__main__":
    unittest.main()
