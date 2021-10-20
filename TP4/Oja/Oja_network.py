import csv

import numpy as np
from sklearn.preprocessing import StandardScaler


class Oja_network:
    def __init__(self, input_size: int, learning_rate):
        self.learning_rate = learning_rate
        self.input_size = input_size
        self.W = np.random.rand(input_size)

    def train(self, data, iterations):
        #standarize data
        std_data = np.zeros((len(data), len(data[0])))
        for i in range(0, len(data[0])):
            new_data = StandardScaler().fit_transform(data[:, i].reshape(-1, 1))
            std_data[:, i] = new_data[:, 0]
        data = std_data

        for iteration in range(iterations):
            for j in data:
                x = j
                y = self.W.dot(x)
                self.W += (self.learning_rate/(iteration+1)) * (y*x - y*y*self.W)
        return self.W


def main():
    file = open('../Kohonen/files/europe.csv')
    reader = csv.reader(file)
    names = []
    data = []
    next(reader)
    for line in reader:
        names.append(line[0])
        data.append([float(x) for x in line[1:8]])
    data = np.array(data)
    oja = Oja_network(7, 0.1)
    W = oja.train(data, 1000)
    pass


if __name__ == '__main__':
    main()