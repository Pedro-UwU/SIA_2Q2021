import numpy as np
from matplotlib import pyplot as plt

class Hopfield:
    def __init__(self, nodes: int, patterns: list[list[int]]):
        self.nodes = nodes
        self.patterns = []
        for p in patterns:
            new_p = np.array(p)[np.newaxis].T
            self.patterns.append(new_p)
            # plt.imshow(new_p.reshape(5, 5), cmap=plt.cm.plasma)
            # plt.show()
        self.weights = np.zeros((nodes, nodes))
        for i in range(nodes):
            for j in range(nodes):
                if i == j:
                    continue
                total = 0
                for p in patterns:
                    total += p[i] * p[j]
                self.weights[i][j] = (1/nodes) * total

    def query(self, pattern, title=None):
        last_pattern = None
        pattern = np.array(pattern)[np.newaxis].T
        attemps = 0
        while (last_pattern is None or not np.array_equal(last_pattern, pattern)) and attemps < 1000:
            plt.imshow(pattern.reshape(5, 5))
            if title is not None:
                plt.title(title)
            plt.show()
            last_pattern = pattern
            pattern = np.sign(np.dot(self.weights, pattern))
            attemps += 1
        return pattern.T.tolist()

if __name__ == '__main__':
    h = Hopfield(4, [[1, 1, -1, -1], [-1, -1, 1, 1]])
    s = h.query([1, -1, -1, -1])
    print('a')