import numpy as np
from matplotlib import pyplot as plt


class Hopfield:
    def __init__(self, nodes: int, patterns: list[list[int]]):
        self.nodes = nodes
        self.patterns = []
        for p in patterns:
            new_p = np.array(p)[np.newaxis].T
            self.patterns.append(new_p)
        self.weights = np.zeros((nodes, nodes))
        for i in range(nodes):
            for j in range(nodes):
                if i == j:
                    continue
                total = 0
                for p in patterns:
                    total += p[i] * p[j]
                self.weights[i][j] = (1/nodes) * total

    def query(self, pattern, title=None, show=True):
        last_pattern = None
        pattern = np.array(pattern)[np.newaxis].T
        attempts = 0
        visited = set()
        while (last_pattern is None or not np.array_equal(last_pattern, pattern)) and attempts < 1000:
            if show:
                Hopfield.show_pattern(pattern, title=title)
            last_pattern = pattern
            pattern = np.sign(np.dot(self.weights, pattern))
            if str(pattern) in visited and not np.array_equal(pattern, last_pattern):
                print(f'Loop Found! {title}')
                return pattern.T.tolist()
            visited.add(str(pattern))
            attempts += 1
        return pattern.T.tolist()

    @staticmethod
    def show_pattern(pattern, title=None):
        pattern = np.array(pattern)[np.newaxis].T
        plt.imshow(pattern.reshape(5, 5))
        if title is not None:
            plt.title(title)
        plt.show()


if __name__ == '__main__':
    h = Hopfield(4, [[1, 1, -1, -1], [-1, -1, 1, 1]])
    s = h.query([1, -1, -1, -1])
    print('a')