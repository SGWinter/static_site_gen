from htmlnode import *

def main():
    ol_test = "1. testing\n2. testing2\n3. testing3"
    print(block_type_to_html_node_ordered_list(ol_test))


if __name__ == "__main__":
    main()
