import math
import matplotlib.pyplot as plt
import numpy as np

class Graph:
    @staticmethod
    def graph_ej1(weights, entries, output):
        x = np.linspace(-2, 2, len(weights))
        class_one_x = []
        class_one_y = []
        class_two_x = []
        class_two_y = []
        for i in range(0, len(entries)):
            if output[i] > 0:
                class_one_x.append(entries[i][0])
                class_one_y.append(entries[i][1])
            else:
                class_two_x.append(entries[i][0])
                class_two_y.append(entries[i][1])

        plt.plot(class_one_x, class_one_y, 'ro')
        plt.plot(class_two_x, class_two_y, 'go')
        plt.plot(x, -((weights[2] + weights[0] * x) / weights[1]), '-b', label='Hiperplano')
        plt.show()

        return

    @staticmethod
    def graph_ej2(training_error_data, test_error_data):
        iterations = len(test_error_data)
        plt.xlabel("Epocas")
        plt.ylabel("Error")
        iterations = len(test_error_data)
        first = training_error_data[0]/4
        title = ("Non Linear")
        plt.title(title)
        plt.grid(True)
        plt.plot(range(0, len(training_error_data)), training_error_data, 'g-', label="Training Error")
        plt.plot(range(0, len(test_error_data)), test_error_data, 'r-', label="Test Error")
        plt.legend()
        plt.show()
