import random
import json
import statistics
import math

class Kohonen:
    data = [] # [0: todos los valores de una variable, 1: todos los valores de otra variable...]
    normalized_data = [] # [0: todos los valores de una variable, 1: todos los valores de otra variable...]
    learning_rate = 0.5
    radius = 1
    output_grid_size = 5
    output_grid = None
    input_size = None
    keys = [] # Orden de los arrays dentro de data y normalized_data
    country_names = []
    epochs = None

    @staticmethod
    def initialize():
        file = open('files/data.json')
        data = json.load(file)['data']

        Kohonen.input_size = len(data[0].keys()) - 1
        Kohonen.epochs = Kohonen.input_size * 500

        Kohonen.normalized_data = Kohonen.normalize_data(data)
        Kohonen.output_grid = Kohonen.initialize_output_grid()

    @staticmethod
    def train():
        indexes = list(range(len(Kohonen.country_names)))
        print(Kohonen.output_grid)
        for e in range(Kohonen.epochs):
            random.shuffle(indexes)
            for idx in indexes:
                idx_values = []
                for row in Kohonen.normalized_data:
                    idx_values.append(row[idx])
                best_neuron = Kohonen.search_best_neuron(idx_values)
                neighbours = Kohonen.find_neighbours(best_neuron)
                Kohonen.update_weights(neighbours, idx_values)
        print(Kohonen.output_grid)

    @staticmethod
    def test():
        grouped_result = {}
        for idx in range(len(Kohonen.country_names)):
            idx_values = []
            for row in Kohonen.normalized_data:
                idx_values.append(row[idx])
            best_neuron = Kohonen.search_best_neuron(idx_values)
            if best_neuron in grouped_result:
                grouped_result[best_neuron].append(Kohonen.country_names[idx])
            else:
                grouped_result[best_neuron] = [Kohonen.country_names[idx]]

        print('Países agrupados por neurona')
        dict_keys = grouped_result.items()
        sorted_by_keys = dict(sorted(dict_keys))
        print(sorted_by_keys)

    @staticmethod
    def normalize_data(data):
        keys = data[0].keys() - ['Country']
        Kohonen.keys = list(keys)

        Kohonen.data = [None] * len(keys)
        for country in data:
            for idx, val in enumerate(keys):
                if Kohonen.data[idx] is None:
                    Kohonen.data[idx] = []
                Kohonen.data[idx].append(float(country[val]))
            Kohonen.country_names.append(country['Country'])

        normalized_data = []
        for row in Kohonen.data:
            normalized_row = []
            media = sum(row) / len(row)
            std = statistics.stdev(row)
            for value in row:
                normalized_row.append((value - media) / std)

            normalized_data.append(normalized_row)

        return normalized_data

    @staticmethod
    def initialize_output_grid():
        grid = [None] * Kohonen.output_grid_size
        for idx in range(Kohonen.output_grid_size):
            grid[idx] = [None] * Kohonen.output_grid_size
            for idy in range(Kohonen.output_grid_size):
                random_index = random.randrange(0, len(Kohonen.normalized_data[0]))
                grid[idx][idy] = []
                for row in Kohonen.normalized_data:
                    grid[idx][idy].append(row[random_index])

        return grid

    @staticmethod
    def search_best_neuron(idx_values):
        min_distance = 1e10
        neuron_position = (-1, -1)
        for x in range(Kohonen.output_grid_size):
            for y in range(Kohonen.output_grid_size):
                current_distance = Kohonen.calculate_distance(idx_values, Kohonen.output_grid[x][y])
                if current_distance < min_distance:
                    min_distance = current_distance
                    neuron_position = (x, y)
        return neuron_position

    @staticmethod
    def calculate_distance(values, grid_values):
        accum = 0.0
        for idx in range(len(values)):
            accum += (values[idx] - grid_values[idx]) ** 2

        return math.sqrt(accum)

    @staticmethod
    def find_neighbours(position):
        neighbours = []
        for idx in range(Kohonen.output_grid_size):
            for idy in range(Kohonen.output_grid_size):
                current_position = (idx, idy)
                if Kohonen.is_neighbour(current_position, position):
                    neighbours.append(current_position)

        return neighbours

    @staticmethod
    def is_neighbour(a, b):
        accum = 0.0
        for idx in range(len(a)):
            accum += (a[idx] - b[idx]) ** 2

        return math.sqrt(accum) <= Kohonen.radius

    @staticmethod
    def update_weights(neighbours, idx_values):
        for neighbor in neighbours:
            idx = neighbor[0]
            idy = neighbor[1]
            current_value = Kohonen.output_grid[idx][idy]
            new_weight = []
            for index in range(len(idx_values)):
                new_weight.append(current_value[index] + (idx_values[index] - current_value[index]) * Kohonen.learning_rate)
            Kohonen.output_grid[idx][idy] = new_weight
