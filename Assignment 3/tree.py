# -*- coding: utf-8 -*-
"""
Created on Fri May 19 19:55:46 2023

@author: Hugo Burton
"""

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def print_tree(node, level=0):
    if node is None:
        return

    print_tree(node.right, level + 1)
    print("    " * level + "|--", node.value)
    print_tree(node.left, level + 1)

# Example usage
# Create the tree
root = Node("A")
root.left = Node("B")
root.right = Node("C")
root.left.left = Node("D")
root.left.right = Node("E")
root.right.left = Node("F")
root.right.right = Node("G")

# Print the tree
print_tree(root)
