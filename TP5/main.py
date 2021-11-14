import random

from Autoencoder import Autoencoder
from MultilayerPerceptron import MultilayerPerceptron
import csv
import matplotlib.pyplot as plt
import numpy as np

def main():
    # ae = Autoencoder([35, 18, 2], MultilayerPerceptron.sigmoid, MultilayerPerceptron.sigmoid_der, 0.07)
    # ae.queryZ([])
    # for i in range(15000):
    #     print(f'epoch: {i}')
    #     with open('data/group1_format.csv') as file:
    #         last_delta = {}
    #         new_delta = {}
    #         reader = csv.reader(file)
    #         lines = []
    #         for l in reader:
    #             lines.append(l)
    #         random.shuffle(lines)
    #         for line in lines:
    #             data = [float(x) for x in line[:-1]]
    #             error = ae.train(data, data, last_delta=last_delta, new_delta=new_delta, alpha=0.8)
    #             # print(f'{error=}')
    ae = Autoencoder.load_autoencoder('test5.json', MultilayerPerceptron.sigmoid, MultilayerPerceptron.sigmoid_der)
    result = ae.queryZ([0.9111892496842396, 0.5221588378941739])
    plt.imshow(np.array(result).reshape((7, 5)), cmap='gray')
    plt.show()
    # with open('data/group1_format.csv') as file:
    #     reader = csv.reader(file)
    #     for line in reader:
    #         data = [float(x) for x in line[:-1]]
    #         result, z = ae.query(data)
    #         fig, (ax1, ax2) = plt.subplots(1, 2)
    #         ax1.imshow(np.array(data).reshape((7, 5)), cmap='gray')
    #         ax2.imshow(np.array(result).reshape((7, 5)), cmap='gray')
    #         print(z)
    #         plt.show()
    # ae.multilayer_perceptron.save_network('test6.json')


if __name__ == '__main__':
    main()