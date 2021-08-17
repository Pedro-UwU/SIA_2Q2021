class Tree:
    def __init__(self):
        self.root = None
        self.children = {}
        self.parents = {}
        self.depths = {}

    def set_root(self, root):
        self.root = root
        self.children[root] = []
        self.depths[root] = 1

    def add_child(self, parent, child):
        # if parent not in self.children:
        #     self.children[parent] = []
        # if child not in self.children[parent]:
        #     if len(self.children[parent]) > 4:
        #         raise Exception('ERROR')
        #     self.children[parent].append(child)
        self.parents[child] = parent
        self.depths[child] = self.depths[parent]+1


    def get_path(self, goal):
        path = []
        while goal in self.parents:
            path.append(goal)
            goal = self.parents[goal]
        path.append(goal)
        path.reverse()
        return path

    def get_depth(self, node):
        if node in self.depths:
            return self.depths[node]
        return -1

    def update_depth(self, node, new_depth):
        if node in self.depths:
            self.depths[node] = new_depth
