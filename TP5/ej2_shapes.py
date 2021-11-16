import csv
import random

import matplotlib.pyplot as plt
import numpy as np

from Autoencoder import Autoencoder
from MultilayerPerceptron import MultilayerPerceptron


def ej2():
    structure = [28*28, 300, 75, 2]
    learning_rate = 0.1
    epochs = 50

    ae = Autoencoder(structure, MultilayerPerceptron.sigmoid, MultilayerPerceptron.sigmoid_der, learning_rate)
    file = open('data/shapes.csv')
    lines = file.readlines()
    errors = []
    for epoch in range(epochs):
        last_delta = {}
        new_delta = {}
        random.shuffle(lines)
        reader = csv.reader(lines)
        line_num = 0
        total_error = 0
        total_count = 0
        for line in reader:
            data = np.array([float(x)/255 for x in line])
            error = ae.train(data, data, last_delta=last_delta, new_delta=new_delta, alpha=0.8)
            total_error += error
            total_count += 1
            print(f'{epoch=}, {line_num=}, {error=}')
        errors.append(total_error/total_count)

    print('Done training')
    test_reader = csv.reader(lines)


    # ae.multilayer_perceptron.save_network(f'mnist_150_30_2_e{epochs}.json')

    x = [i for i in range(epochs)]
    plt.plot(x, errors)
    plt.xlabel('Epochs')
    plt.ylabel('Error')
    plt.title('Average Error while Training')
    plt.show()

    fig, (ax1, ax2) = plt.subplots(1, 2)
    for i, elem in enumerate(test_reader):
        if i % 25 != 0:
            continue

        data = [float(x)/255 for x in elem]
        result, z = ae.query(data)
        ax1.set_title('Original')
        ax2.set_title(f'Result: {i}')
        ax1.imshow(np.array(data).reshape((28, 28)), cmap='gray')
        ax2.imshow(np.array(result).reshape((28, 28)), cmap='gray')
        fig.show()

    # ae = Autoencoder.load_autoencoder('./mnist_350_70_2_e200.json', MultilayerPerceptron.sigmoid, MultilayerPerceptron.sigmoid_der)
    graph_latent_space(ae)

def graph_latent_space(ae):
    n = 15
    figsize = 15
    digit_size = 28
    scale = 1.0
    figure = np.zeros((digit_size * n, digit_size * n))
    # linearly spaced coordinates corresponding to the 2D plot
    # of digit classes in the latent space
    grid_x = np.linspace(-0.5, 1.5, n)
    grid_y = np.linspace(-0.5, 1.5, n)[::-1]
    for i, yi in enumerate(grid_y):
        for j, xi in enumerate(grid_x):
            z_sample = np.array([[xi, yi]])
            z_sample = z_sample.tolist()[0]
            x_decoded = ae.queryZ(z_sample)
            x_decoded = np.array(x_decoded)
            digit = x_decoded.reshape(digit_size, digit_size)
            figure[
            i * digit_size: (i + 1) * digit_size,
            j * digit_size: (j + 1) * digit_size,
            ] = digit

    plt.figure(figsize=(figsize, figsize))
    start_range = digit_size // 2
    end_range = n * digit_size + start_range
    pixel_range = np.arange(start_range, end_range, digit_size)
    sample_range_x = np.round(grid_x, 1)
    sample_range_y = np.round(grid_y, 1)
    plt.xticks(pixel_range, sample_range_x)
    plt.yticks(pixel_range, sample_range_y)
    plt.xlabel("z[0]")
    plt.ylabel("z[1]")
    plt.title('Latent Space')
    plt.imshow(figure, cmap="Greys_r")
    plt.show()


if __name__ == '__main__':
    ej2()