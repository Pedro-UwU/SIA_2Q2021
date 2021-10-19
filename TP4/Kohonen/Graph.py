import matplotlib.pyplot as plt
import math
import numpy as np


class Graph:

    @staticmethod
    def graph_activated_neurons(grouped_result, best_neurons, grid_size):
        all_points = []
        for x in range(grid_size):
            for y in range(grid_size):
                all_points.append((x, y))
        activated_neurons = list(set(best_neurons));
        activated_neurons.sort()

        amounts = []
        for activated_neuron in activated_neurons:
            amounts.append(60 * len(grouped_result[activated_neuron]))

        fig, ax = plt.subplots()
        ax.scatter(*zip(*all_points), label='Neuronas no activadas')
        ax.scatter(*zip(*activated_neurons), s=amounts, label='Neuronas activadas y su cantidad')
        ax.set_title('Activación de neuronas')
        ax.set_xlabel('Coordenada x - Neuronas')
        ax.set_ylabel('Coordenada y - Neuronas')

        plt.xlim(-1, grid_size)
        plt.ylim(-1, grid_size)
        plt.legend(fontsize=8, markerscale=0.5)
        plt.show()

    @staticmethod
    def graph_average_distance(grid_size, grid):
        average_distance_grid = Graph.calculate_average_distance_grid(grid_size, grid)

        arr_for_graph = np.array(Graph.grid_for_graph(average_distance_grid))

        fig, ax = plt.subplots()
        im = ax.imshow(arr_for_graph)

        ax.set_xticks(np.arange(grid_size))
        ax.set_yticks(np.arange(grid_size))
        ax.set_yticklabels(range(grid_size - 1, -1, -1))

        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel('Distancia promedio', rotation=-90, va="bottom")

        for x in range(grid_size):
            for y in range(grid_size):
                text = ax.text(y, x, round(arr_for_graph[x, y], 2), ha="center", va="center", color="w")

        ax.set_title("Distancias promedio entre neuronas vecinas")
        fig.tight_layout()
        plt.show()

    @staticmethod
    def calculate_average_distance_grid(grid_size, output_grid):
        grid = [None] * grid_size
        for x in range(grid_size):
            grid[x] = [None] * grid_size

            for y in range(grid_size):
                current_position = (x, y)
                neighbours = Graph.find_neighbours(current_position, grid_size)
                total_distance = []
                for neighbour in neighbours:
                    if neighbour != current_position:
                        total_distance.append(Graph.calculate_distance(current_position, neighbour, output_grid))

                grid[x][y] = sum(total_distance) / len(total_distance)

        return grid

    @staticmethod
    def find_neighbours(position, grid_size):
        neighbours = []
        for idx in range(grid_size):
            for idy in range(grid_size):
                current_position = (idx, idy)
                if Graph.is_neighbour(current_position, position):
                    neighbours.append(current_position)

        return neighbours

    @staticmethod
    def is_neighbour(a, b):
        accum = 0.0
        for idx in range(len(a)):
            accum += (a[idx] - b[idx]) ** 2

        return math.sqrt(accum) <= 1  # radius

    @staticmethod
    def calculate_distance(current_position, neighbour, grid):
        values = grid[current_position[0]][current_position[1]]
        grid_values = grid[neighbour[0]][neighbour[1]]
        accum = 0.0
        for idx in range(len(values)):
            accum += (values[idx] - grid_values[idx]) ** 2

        return math.sqrt(accum)

    @staticmethod
    def grid_for_graph(original_grid):
        size = len(original_grid)
        grid = [None] * size
        for y in range(size):
            grid[y] = []
            aux = size - y - 1
            for x in range(size):
                grid[y].append(original_grid[x][aux])

        return grid




