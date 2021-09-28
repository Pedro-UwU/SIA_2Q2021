import os
import random

import numpy as np

from Config import Config as Cf
import matplotlib.pyplot as plt

from ej3.NeuralNetwork import NeuralNetwork


def ej3_1():
    train_set = [[-1, 1], [1, -1], [-1, -1], [1, 1]]
    target_set = [1, 1, -1, -1]
    layers = Cf.config.hidden_layers_ej3_1
    nodes_per_layer = [int(x) for x in Cf.config.nodes_per_layer_ej3_1.split(',')]
    nodes_per_layer.insert(0, 2)
    nodes_per_layer.append(1)
    print(nodes_per_layer)

    nn = NeuralNetwork(layers+2, nodes_per_layer, NeuralNetwork.tanh, NeuralNetwork.tanh_der, Cf.config.learning_rate_ej3_1)
    epochs = Cf.config.epochs_ej3_1
    for i in range(epochs):
        order = [x for x in range(len(train_set))]
        random.shuffle(order)
        for j in range(len(train_set)):
            inputs = train_set[j]
            targets = [target_set[j]]
            error = nn.train(inputs, targets)
        if i % 10 == 0:
            print(f"epoch: {i}")
            x = []
            y = []
            values = []
            for _x in np.arange(-1.5, 1.5, 0.1):
                for _y in np.arange(-1.5, 1.5, 0.1):
                    result = nn.query([_x, _y])[0][0]
                    x.append(_x)
                    y.append(_y)
                    values.append(result)

            plt.scatter(x, y, s=50, c=values, cmap='gray')
            plt.title(f'Epoch: {i}')
            plt.xlabel('x_2')
            plt.ylabel('x_1')
            plt.gray()
            plt.show()


if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    config_path = os.path.join(dirname, '../config.conf')
    Cf.init_config(config_path)
    ej3_1()