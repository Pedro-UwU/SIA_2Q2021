import numpy as np

from MultilayerPerceptron import MultilayerPerceptron


class Autoencoder:
    def __init__(self, structure, activation_function, activation_derivative, learning_rate):
        self.encoder = MultilayerPerceptron(layers=len(structure), nodes_per_layer=structure, activation_function=activation_function, activation_derivative=activation_derivative, learning_rate=learning_rate)
        self.decoder = MultilayerPerceptron(layers=len(structure), nodes_per_layer=list(reversed(structure)), activation_function=activation_function, activation_derivative=activation_derivative, learning_rate=learning_rate)

    def query(self, input_array: list[float]):
        z = self.encoder.query(input_array)
        z = [x[0] for x in z]
        decoder_output = self.decoder.query(z)
        return decoder_output, z

    def train(self, input_array):
        z = self.encoder.query(input_array)
        z = [x[0] for x in z]
        error, d = self.decoder.train(z, input_array)
        new_z = z.copy()
        for i, elem in enumerate(z):
            new_z[i] += d[0][i][0]/self.decoder.derivative(elem)
        error2, d2 = self.encoder.train(input_array, new_z)
        test, z = self.query(input_array)
        print(f'{test=}\n{z=}')

