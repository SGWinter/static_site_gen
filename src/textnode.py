from htmlnode import LeafNode
from htmlnode import ParentNode
from htmlnode import HTMLNode
import re


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delimiters = ["**", "*", "`",]
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
        if delimiter not in delimiters:
            raise Exception(f"Invalid delimiter: {delimiter}")
        text_split = node.text.split(delimiter, 2)
        if len(text_split) == 1:
            new_nodes.extend([TextNode(f"{text_split[0]}", node.text_type)])
        else:
            new_nodes.extend([TextNode(f"{text_split[0]}", text_type_text)])
            new_nodes.extend([TextNode(f"{text_split[1]}", text_type)])
            if len(text_split) > 2:
                if delimiter in text_split[2]:
                    new_nodes.extend(split_nodes_delimiter([TextNode(text_split[2],text_type_text)], delimiter, text_type))
                elif len(text_split[2]) > 0:
                    new_nodes.extend([TextNode(f"{text_split[2]}", text_type_text)])
    return new_nodes


def extract_markdown_images(text):
    match = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return match

def extract_markdown_links(text):
    match = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return match

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracts = extract_markdown_images(node.text)
        if not extracts:
            new_nodes.extend([node])
        else:
            new_text = node.text.split(f"![{extracts[0][0]}]({extracts[0][1]})", 1)
            new_nodes.extend(
                    [
                    TextNode(new_text[0], text_type_text),
                    TextNode(extracts[0][0], text_type_image, extracts[0][1]),
                    ]
            )
            if new_text[1]:
                new_nodes.extend(split_nodes_image([TextNode(new_text[1], text_type_text)]))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extracts = extract_markdown_links(node.text)
        if not extracts:
            new_nodes.extend([node])
        else:
            new_text = node.text.split(f"[{extracts[0][0]}]({extracts[0][1]})", 1)
            new_nodes.extend(
                    [
                    TextNode(new_text[0], text_type_text),
                    TextNode(extracts[0][0], text_type_link, extracts[0][1]),
                    ]
            )
            if new_text[1]:
                new_nodes.extend(split_nodes_link([TextNode(new_text[1], text_type_text)]))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = []
    delimiters = ["**", "*", "`"]
    new_nodes.extend(split_nodes_delimiter([TextNode(text, text_type_text)], delimiters[0], text_type_bold))
    new_nodes = split_nodes_delimiter(new_nodes, delimiters[1], text_type_italic)
    new_nodes = split_nodes_delimiter(new_nodes, delimiters[2], text_type_code)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    list_block_strings = []
    lines = markdown.split("\n\n")
    for line in lines:
        if len(line) > 0:
            list_block_strings.append(line.strip())
    return list_block_strings

def block_to_block_type(block):
    block_type = block_type_paragraph
    if "#" in block[:6]:
        block_type = block_type_heading
    elif ">" in block[0]:
        block_lines = block.split("\n")
        quote = True
        for line in block_lines:
            if ">" not in line[0]:
                quote = False
        if quote:
            block_type = block_type_quote
    elif block[0].isnumeric():
        block_lines = block.split("\n")
        i = 1
        for line in block_lines:
            if f"{i}." not in line[:3]:
                return block_type_paragraph
            i += 1
        block_type = block_type_ordered_list
    elif "*" in block[0] or "-" in block[0]:
        block_lines = block.split("\n")
        for line in block_lines:
            if "*" not in line[0] and "-" not in line[0]:
                return block_type_paragraph
        block_type = block_type_unordered_list
    elif "```" in block[:3]:
        if "```" in block[4:]:
            block_type = block_type_code
    return block_type

def block_type_to_html_node_paragraph(block):
    return HTMLNode("p", block + "\n")

def block_type_to_html_node_heading(block):
    i = 0
    new_block = block
    for each in block[:6]:
        if "#" in each:
            i += 1
            new_block = new_block[1:].strip()
        else:
            break
    return HTMLNode(f"h{i}", new_block)

def block_type_to_html_node_quote(block):
    new_block = block.replace(">", "").strip("> ")
    return HTMLNode("blockquote", new_block)

def block_type_to_html_node_code(block):
    new_block = block.strip("` ")
    new_block = f"<code>{new_block.strip()}</code>"
    return HTMLNode("pre", new_block)

def block_type_to_html_node_unordered_list(block):
    split_block = block.split("\n")
    new_block = ""
    for each in split_block:
        new_line = each.lstrip("*- ")
        new_block += f"<li>{new_line}</li>"
    return HTMLNode("ul", new_block)

def block_type_to_html_node_ordered_list(block):
    split_block = block.split("\n")
    new_block = ""
    for each in split_block:
        new_line = each.lstrip("1234567890. ")
        new_block += f"<li>{new_line}</li>"
    return HTMLNode("ol", new_block)

def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    children = []
    for block in block_list:
        block_type = block_to_block_type(block)
        if block_type == block_type_unordered_list:
            children.extend([block_type_to_html_node_unordered_list(block)])
        elif block_type == block_type_ordered_list:
            children.extend([block_type_to_html_node_ordered_list(block)])
        elif block_type == block_type_heading:
            children.extend([block_type_to_html_node_heading(block)])
        elif block_type == block_type_quote:
            children.extend([block_type_to_html_node_quote(block)])
        elif block_type == block_type_code:
            children.extend([block_type_to_html_node_code(block)])
        elif block_type == block_type_paragraph:
            children.extend([block_type_to_html_node_paragraph(block)])
    for child in children:
        child_nodes = text_to_textnodes(child.value)
        child_children = []
        for child_node in child_nodes:
            child_children.extend([text_node_to_html_node(child_node)])
        child.children = child_children
    return ParentNode("div", children)
