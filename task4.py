from uuid import uuid4
import time
import networkx as nx
import matplotlib.pyplot as plt


class Comment:
    def __init__(self, user, text, id=None, timestamp=None):
        self.user = user
        self.text = text
        self.id = id if id is not None else uuid4()
        self.time = timestamp if timestamp is not None else time.time()
        self.color = "RED"
        self.left = None
        self.right = None
        self.parent = None


class Chat:
    def __init__(self):
        self.TNULL = Comment(None, "", id=None, timestamp=None)
        self.TNULL.color = "BLACK"
        self.root = self.TNULL
        self.animation_steps = []

    def _rotate_l(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        self.capture_snapshot("Left ")

    def _rotate_r(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        self.capture_snapshot("Right")

    def fix_colors(self, node):
        while node.parent and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right if node.parent.parent else None
                if uncle and uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._rotate_l(node)
                        self.capture_snapshot(f"Left Rotate {node.user}")
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._rotate_r(node.parent.parent)
            else:
                uncle = node.parent.parent.left if node.parent.parent else None
                if uncle and uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_r(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._rotate_l(node.parent.parent)
        self.root.color = "BLACK"
        self.capture_snapshot("Final Balanced ")

    def add_message(self, user, text):
        node = Comment(user, text)
        node.left = self.TNULL
        node.right = self.TNULL
        parent = None
        current = self.root
        while current != self.TNULL:
            parent = current
            current = current.left if node.time < current.time else current.right
        node.parent = parent
        if parent is None:
            self.root = node
        elif node.time < parent.time:
            parent.left = node
        else:
            parent.right = node
        node.color = "RED"
        self.fix_colors(node)

    def traverse(self, node, comments):
        if node != self.TNULL:
            self.traverse(node.left, comments)
            comments.append((node.id, node.text, node.user))
            self.traverse(node.right, comments)

    def capture_snapshot(self, title=""):
        pic = nx.DiGraph()
        pos = {}
        colors = {}
        labels = {}

        def traverse(node, x=0.0, y=0.0, layer=1.0):
            if node:
                pic.add_node(node.time, label=f"{node.text}")
                pos[node.time] = (x, y)
                colors[node.time] = "red" if node.color == "RED" else "black"
                labels[node.time] = f"{node.user}\n{node.text}"

                if node.left and node.left != self.TNULL:

                    pic.add_edge(node.time, node.left.time)
                    traverse(node.left, x - 1 / layer, y - 1, layer * 3)

                if node.right and node.right != self.TNULL:
                    pic.add_edge(node.time, node.right.time)
                    traverse(node.right, x + 1 / layer, y - 1, layer * 3)

        traverse(self.root)
        self.animation_steps.append((pic, pos, colors, labels, title))

    def animate(self, interval=1):
        plt.ion()
        fig, ax = plt.subplots(figsize=(10, 7))
        for step in self.animation_steps:
            pic, pos, colors, labels, title = step
            ax.clear()
            node_colors = [colors[node] for node in pic.nodes()]
            nx.draw(
                pic,
                pos,
                with_labels=True,
                node_color=node_colors,
                edge_color="gray",
                node_size=3000,
                font_size=6,
            )
            nx.draw_networkx_labels(
                pic,
                pos,
                labels,
                font_size=8,
                font_color="green",
                bbox=dict(
                    facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"
                ),
            )
            ax.set_title(f"Red-Black Tree Balancing: {title}")
            plt.draw()
            plt.pause(interval)
            plt.clf()
        plt.ioff()
        plt.show()


new = Chat()
new.add_message("me", "love red&black")
new.add_message("me2", "love from right side red&black")
new.add_message("me4", "love turn visual side red&black")
new.add_message("me5", "love change visual side red&black")
new.add_message("me6", "love upside-down ")
new.add_message("me7", "love  red&black")
new.add_message("me8", "love side red&black")
new.add_message("me9", "love  red&black")
new.add_message("me10", " red&black")


new.animate(interval=1)
comments = []
new.traverse(new.root, comments)

for comment in comments:
    print(f"User: {comment[2]} | Message: {comment[1]}")
