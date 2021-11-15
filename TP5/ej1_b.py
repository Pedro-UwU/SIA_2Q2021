import csv
import random

import matplotlib.pyplot as plt
import numpy as np

from Autoencoder import Autoencoder
from MultilayerPerceptron import MultilayerPerceptron


def ej1_b():
    structure = [35, 20, 5]
    noise_prob = 0.5
    noise_range = 1
    epochs = 10000

    file = open('data/group2_format.csv')
    reader = csv.reader(file)
    ae = Autoencoder(structure, MultilayerPerceptron.sigmoid, MultilayerPerceptron.sigmoid_der, 0.1)
    data = get_data(reader)

    error = train_with_noise(ae, data, epochs, noise_prob, noise_range)
    graph_error(epochs, error)
    print(error[-1])
    test_data = add_noise(data, noise_prob, noise_range)
    graph_digits(ae, data, test_data)


def graph_digits(ae, data, corrupted_data):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    for i in range(len(data)):
        result, z = ae.query(corrupted_data[i])
        ax1.set_title('Original')
        ax2.set_title('With Noise')
        ax3.set_title('AE result')
        ax1.imshow(np.array(data[i]).reshape((7,5)), cmap='gray')
        ax2.imshow(np.array(corrupted_data[i]).reshape((7, 5)), cmap='gray')
        ax3.imshow(np.array(result).reshape((7, 5)), cmap='gray')
        fig.show()


def graph_error(epochs, error):
    y = error
    x = [i for i in range(epochs)]
    plt.plot(x, y)
    plt.title('Error promedio por epoca')
    plt.xlabel('Epochs')
    plt.ylabel('Error promedio')
    plt.show()


def train_with_noise(ae, data, epochs, noise_prob, noise_range):
    error_per_epoch = []
    for i in range(epochs):
        print(f'epoch: {i}')
        corrupted = add_noise(data, noise_prob, noise_range)
        last_delta = {}
        new_delta = {}
        total_error = 0
        total_count = 0
        for i in range(len(data)):
            total_error += ae.train(corrupted[i], data[i], last_delta=last_delta, new_delta=new_delta, alpha=0.8)
            total_count += 1
        error_per_epoch.append(total_error/total_count)
    return error_per_epoch


def add_noise(data, noise_prob, noise_range):
    corrupted = []
    for line in data:
        corrupted_line = line.copy()
        for i, elem in enumerate(corrupted_line):
            if random.uniform(0, 1) < noise_prob:
                elem += random.uniform(-noise_range, noise_range)
                corrupted_line[i] = elem
        corrupted.append(corrupted_line)
    return corrupted


def get_data(reader):
    data = []
    for line in reader:
        values = [float(x) for x in line[:-1]]
        data.append(values)
    return data


if __name__ == '__main__':
    ej1_b()