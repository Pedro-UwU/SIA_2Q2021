import math
from sklearn.preprocessing import StandardScaler
import numpy as np
import random
import csv

class newKohonen:

    def __init__(self, learning_rate=0.5, radius=1, grid_size=20, input_size=None, data=None, data_headers=None, decreasing_factor=1):
        self.decreasing_factor = decreasing_factor
        self.initial_lr = learning_rate
        self.learning_rate = learning_rate
        self.initial_radius = radius
        self.radius = radius
        self.grid_size = grid_size
        self.input_size = input_size
        self.data_headers = data_headers

        #standarize data
        std_data = np.zeros((len(data), len(data[0])))
        for i in range(0, len(data[0])):
            new_data = StandardScaler().fit_transform(data[:, i].reshape(-1, 1))
            std_data[:, i] = new_data[:, 0]
        self.data = std_data

        self.W = np.zeros((grid_size, grid_size), dtype=np.ndarray) #weight matrix
        for i in range(grid_size):
            for j in range(grid_size):
                self.W[i, j] = random.choice(self.data).copy()

    def train(self):
        repetitions = 500 * len(self.data[0])
        for rep in range(repetitions):
            all_data = self.data.copy()
            for selected_data in all_data:
                winner_i, winner_j = self._search_winner(selected_data)
                neighbors = self._get_neighbors(self.radius, winner_i, winner_j)
                # Update W
                for n_i, n_j in neighbors:
                    self.W[n_i, n_j] += self.learning_rate * (selected_data - self.W[n_i, n_j])
            # Update Learing_rate
            self.learning_rate = 1/(rep + 2)
            self.radius = 1 + math.exp(-self.decreasing_factor * rep / 1000) * (self.initial_radius - 1)

    def test(self):
        count = np.empty((self.grid_size, self.grid_size), dtype=list)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                count[i, j] = []
        for i, d in enumerate(self.data):
            winner_i, winner_j = self._search_winner(d)
            count[winner_i, winner_j].append(self.data_headers[i] if self.data_headers is not None else 1)

        return count


    def _search_winner(self, selected):
        min_i = 0
        min_j = 0
        min_dist = math.inf
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                new_dist = np.linalg.norm(self.W[i, j] - selected)
                if new_dist < min_dist:
                    min_dist = new_dist
                    min_i = i
                    min_j = j
        return min_i, min_j

    def _get_neighbors(self, radius, i, j):
        result = []
        for new_i in range(int(max(i-radius, 0)), int(min(i+radius+1, self.grid_size))):
            for new_j in range(int(max(j-radius, 0)), int(min(j+radius+1, self.grid_size))):
                if new_i == i and new_j == j:
                    continue
                dist = math.sqrt((i - new_i) ** 2 + (j - new_j) ** 2)
                if dist <= radius:
                    result.append((new_i, new_j))
       # print(f'Original {(i,j)}, neighbors: {result}')
        return result
