class Tree2:

    def __init__(self):
        self.root = None

    def set_root(self, value):
        self.root = Node(value)


class Node:
    def __init__(self, value, depth=0, parent=None):
        self.value = value
        self.depth = depth
        self.children = []
        self.parent = parent

    def add_child(self, child_node):
        if child_node not in self.children:
            self.children.append(child_node)
            child_node.depth = self.depth + 1

    def get_path(self, result=None):
        if self.parent is None:
            result.append(self.value)
            return result
        if result is None:
            result = [self.value]
            return self.parent.get_path(result)
        result.append(self.value)
        return self.parent.get_path(result)

    def __hash__(self):
        return self.value.__hash__()