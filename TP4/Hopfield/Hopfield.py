import numpy as np

class Hopfield:
    def __init__(self, nodes: int, patterns: list[list[int]]):
        self.nodes = nodes
        self.patterns = []
        for p in patterns:
            self.patterns.append(np.array(p)[np.newaxis].T)

        self.weights = np.zeros((nodes, nodes))
        for i in range(nodes):
            for j in range(i+1, nodes):
                total = 0
                for p in patterns:
                    total += p[i] * p[j]
                self.weights[i][j] = self.weights[j][i] = (1/nodes) * total

    def query(self, pattern):
        last_pattern = None
        pattern = np.array(pattern)[np.newaxis].T
        while last_pattern is None or not np.array_equal(last_pattern, pattern):
            last_pattern = pattern
            pattern = np.sign(np.dot(self.weights, pattern))
        return pattern.T.tolist()

if __name__ == '__main__':
    h = Hopfield(4, [[1, 1, -1, -1], [-1, -1, 1, 1]])
    s = h.query([1, -1, -1, -1])
    print('a')