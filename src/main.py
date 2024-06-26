from textnode import TextNode
from textnode import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import os
import shutil

def recursive_dir_copy(static_path="./static", public_path="./public"):
    if not os.path.exists(static_path):
        raise Exception(f"Path error: {static_path} path does not exist")
    static_dir_list = os.listdir(static_path)
    shutil.rmtree(public_path)
    os.mkdir(public_path)
    for path in static_dir_list:
        new_path_static = os.path.join(static_path, path)
        new_path_public = os.path.join(public_path, path)
        if os.path.isfile(new_path_static):
            shutil.copy(new_path_static, new_path_public)
        else:
            os.mkdir(new_path_public)
            recursive_dir_copy(new_path_static, new_path_public)

def check_static_public_paths(static_path="./static", public_path="./public"):
    if not os.path.exists(static_path) and not os.path.exists(public_path):
        raise Exception(f"Path error: {static_path} and {public_path} paths do not exist")
    shutil.rmtree("./public")
    os.mkdir("./public")

def extract_title(markdown):
    html_node = markdown_to_html_node(markdown)
    h1_flag = False
    header_text = ""
    for node in html_node.children:
        if node.tag == "h1":
            h1_flag = True
            header_text = ""
            for child in node.children:
                header_text += child.to_html()
    if h1_flag == False:
        raise Exception("Header 1 Error: no h1 contents found")
    return header_text

def recursive_to_html(html_node):
    html = ""
    if isinstance(html_node, LeafNode):
        html += html_node.to_html()
        return(html)
    elif isinstance(html_node, ParentNode) and html_node.children is not None:
        html += f"<{html_node.tag}>\n"
        for child in html_node.children:
            html += recursive_to_html(child)
        html += f"</{html_node.tag}>\n"
    elif isinstance(html_node, HTMLNode) and html_node.children is not None:
        html += f"<{html_node.tag}>\n"
        for child in html_node.children:
            html += recursive_to_html(child)
        html += f"</{html_node.tag}>\n"
    return html

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path)
    template_file = open(template_path)
    dest_file = open(dest_path, "w")
    markdown = from_file.read()
    from_file.close()
    html_nodes = markdown_to_html_node(markdown)
    html = "\n" + recursive_to_html(html_nodes) + "\n"
    title = extract_title(markdown)
    template = template_file.read()
    template_file.close()
    new_file = template.replace("{{ Title }}", title)
    new_file = new_file.replace("{{ Content }}", html)
    dest_file.write(new_file)
    dest_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_list = os.listdir(dir_path_content)
    for dir in dir_list:
        dir_path = os.path.join(dir_path_content, dir)
        if os.path.isfile(dir_path):
            print(f"is file: {dir_path}")
            generate_page(dir_path, template_path, f"{dest_dir_path}/{dir.replace('.md', '.html')}")
        else:
            print(f"is dir: {dir_path}")
            new_dest_dir_path = f"./public{dir_path.replace('./content', '')}"
            print(new_dest_dir_path)
            if not os.path.exists(new_dest_dir_path):
                os.mkdir(new_dest_dir_path)
            generate_pages_recursive(dir_path, template_path, new_dest_dir_path)


def main():
    check_static_public_paths()
    recursive_dir_copy()
    generate_pages_recursive("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()
