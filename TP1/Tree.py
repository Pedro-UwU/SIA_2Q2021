class Tree:
    def __init__(self):
        self.root = None
        self.children = {}
        self.parents = {}

    def set_root(self, root):
        self.root = root
        self.children[root] = []

    def add_child(self, parent, child):
        # if parent not in self.children:
        #     self.children[parent] = []
        # if child not in self.children[parent]:
        #     if len(self.children[parent]) > 4:
        #         raise Exception('ERROR')
        #     self.children[parent].append(child)
        if child not in self.parents:
            self.parents[child] = parent

    def get_path(self, goal):
        path = []
        while goal in self.parents:
            path.append(goal)
            goal = self.parents[goal]
        path.append(goal)
        path.reverse()
        return path
