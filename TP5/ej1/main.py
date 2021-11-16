import random

from Autoencoder import Autoencoder
from MultilayerPerceptron import MultilayerPerceptron
import csv
import matplotlib.pyplot as plt
import numpy as np

def main():
    structures = [[35, 20, 2, 20, 35]] # [[35, 18, 2, 18, 35], [35, 15, 2, 15, 35], [35, 20, 2, 20, 35], [35, 10, 2, 10, 35], [35, 12, 2, 12, 35]]
    colors = ['b', 'r', 'g', 'c', 'm']
    # # # for idx, val in enumerate(ints):
    plt.xlabel("Epoch")
    plt.ylabel("Error Promedio")
    for index, structure in enumerate(structures):
        print(f'Structure: {index + 1} / {len(structures)}')
        ab = 0
        ae = Autoencoder(structure[:-2], MultilayerPerceptron.sigmoid, MultilayerPerceptron.sigmoid_der, 0.07)
        # ae.queryZ([])
        cummulative_error = []
        x = []
        epochs_error = []
        for i in range(15000):
            print(f'epoch: {i}')
            with open('../data/group2_format.csv') as file:
                last_delta = {}
                new_delta = {}
                reader = csv.reader(file)
                lines = []
                for l in reader:
                    lines.append(l)
                random.shuffle(lines)
                epoch_error = 0.0
                for line in lines:
                    data = [float(x) for x in line[:-1]]
                    error = ae.train(data, data, a=0.01, b=0.02)
                    epoch_error += error[0]
                    # print(f'{error=}')
                epochs_error.append(epoch_error / len(lines))
                if (i % 50 == 0):
                    average_error = 0.0
                    for e in epochs_error:
                        average_error += e
                    average_error = average_error / len(epochs_error)
                    cummulative_error.append(average_error)
                    x.append(i)
                    epochs_error = []

    #     ae.multilayer_perceptron.save_network('35-20-2.json')
        print(f'X: {x}')
        plt.plot(x, cummulative_error, colors[index], label=f"{structure}", linewidth=0.4)
        # print(f'Error = {cummulative_error}')
    plt.legend(loc='best')
    plt.show()

    # ae = Autoencoder.load_autoencoder('35-20-2.json', MultilayerPerceptron.sigmoid, MultilayerPerceptron.sigmoid_der)
    # xy = [0.25, 0.55]
    # result = ae.queryZ(xy)
    # plt.imshow(np.array(result).reshape((7, 5)), cmap='gray')
    # plt.title(f"{xy}")
    # plt.show()
    # with open('../data/group2_format.csv') as file:
    #     reader = csv.reader(file)
    #     x = []
    #     y = []
    #     labels = []
    #     for line in reader:
    #         data = [float(x) for x in line[:-1]]
    #         result, z = ae.query(data)
    #         # fig, (ax1, ax2) = plt.subplots(1, 2)
    #         # ax1.imshow(np.array(data).reshape((7, 5)), cmap='gray')
    #         # ax2.imshow(np.array(result).reshape((7, 5)), cmap='gray')
    #         # plt.plot(z[0][0], z[1][0], label=f"{line[-1]}")
    #         x.append(z[0][0])
    #         y.append(z[1][0])
    #         labels.append(line[-1])
    #     fig, ax = plt.subplots()
    #     ax.scatter(x, y)
    #
    #     for i, txt in enumerate(labels):
    #         ax.annotate(txt, (x[i], y[i]))
    #     plt.title("Espacio latente")
    #     plt.show()
    # ae.multilayer_perceptron.save_network('test1.json')


if __name__ == '__main__':
    main()