from typing import Optional
import networkx as nx
import matplotlib.pyplot as plt
import random


class TreeNode:
    def __init__(self, value: Optional[int] = None):
        self.value = value
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None
        self.height = 1

    def add_child(self, node):
        if node.value > self.value:
            self.left = node
        else:
            self.right = node

    def children(self):
        if self.left and self.right:
            return self.left.value, self.right.value


class Tree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, z):
        y = z.left
        T2 = y.right
        y.right = z
        z.left = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def add_root(self, key):
        self.root = self.insert(self.root, key)

    def insert(self, node, key):
        """node--> its node at the tree key its value to insert on this node"""
        if not node:
            return TreeNode(key)
        if key < node.value:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and key < node.left.value:
            return self.rotate_right(node)
        if balance < -1 and key > node.right.value:
            return self.rotate_left(node)
        if balance > 1 and key > node.left.value:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and key < node.right.value:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def show_tree(self):
        if not self.root:
            print("no tree")
            return
        pic = nx.DiGraph()
        pos = {}
        max_value = self.max_value()
        min_value = self.min_value()
        print(max_value, min_value)

        def traverse(node, x=0.0, y=0.0, layer=1.0):
            if node:
                pic.add_node(node.value)
                pos[node.value] = (x, -y)

                if node.left:
                    pic.add_edge(node.value, node.left.value)
                    traverse(node.left, x - 1 / layer, y + 1, layer * 1.5)

                if node.right:
                    pic.add_edge(node.value, node.right.value)
                    traverse(node.right, x + 1 / layer, y + 1, layer * 1.5)

        traverse(self.root)

        plt.figure(figsize=(8, 5))
        nx.draw(
            pic,
            pos,
            with_labels=True,
            node_color="red",
            edge_color="gray",
            node_size=2000,
            font_size=13,
        )
        plt.title("picture tree")
        plt.text(
            pos[min_value][0],
            pos[min_value][1] - 0.2,
            f"Min: {min_value}",
            color="blue",
            fontsize=12,
            ha="center",
        )
        plt.text(
            pos[max_value][0],
            pos[max_value][1] - 0.2,
            f"Max: {max_value}",
            color="green",
            fontsize=12,
            ha="center",
        )

        plt.show()

    def max_value(self):
        if self.root is None:
            return "no tree"

        def _max_value(node):
            if node is None:
                return float("-inf")
            left_max = _max_value(node.left)
            right_max = _max_value(node.right)
            return max(node.value, left_max, right_max)

        return _max_value(self.root)

    def min_value(self):
        if self.root is None:
            return "no tree"

        def _min_value(node):
            if node is None:
                return float("inf")
            left_min = _min_value(node.left)
            right_min = _min_value(node.right)
            return min(node.value, left_min, right_min)

        return _min_value(self.root)

    def sum_all(self):
        if not self.root:
            print("no tree")
            return
        total_sum = self.root.value

        def _sum_all(node):
            if node is None:
                return 0
            left_sum = _sum_all(node.left)
            right_sum = _sum_all(node.right)
            return node.value + left_sum + right_sum

        return _sum_all(self.root)


# tree = Tree()
# values = [10, 20, 30, 40, 50, 25, 100]


# print(tree.max_value())
# print(tree.min_value())
# print(tree.sum_all())


if __name__ == "__main__":
    print("захопили мене дерева, якось сталось що всі три таски в одну поєднались")
    tree = Tree()
    leaves = [
        random.randint(1, 1000) for _ in range(int(input("Enter number of leaves: ")))
    ]
    for v in leaves:
        tree.add_root(v)

    tree.show_tree()
