import numpy as np
import json


class NeuralNetwork:
    def __init__(self, layers: int, nodes_per_layer: list[int], activation_function, activation_derivative,
                 learning_rate, init_random=True):
        self.layers = layers
        self.nodes_per_layer = nodes_per_layer.copy()
        self.weights: list[np.ndarray] = []
        self.activation = activation_function
        self.derivative = activation_derivative
        self.lr = learning_rate
        self._last_error = None

        if init_random:
            for i in range(layers - 1):
                w = (np.random.rand(self.nodes_per_layer[i + 1],
                                    self.nodes_per_layer[i] + 1) - 0.5) * 2  # El +1 es para el bias node
                self.weights.append(w)

    def query(self, input_array: list[float]):
        inp = np.array(input_array)[np.newaxis].T
        inp = NeuralNetwork._add_bias(inp)
        h = [inp]
        values = [inp]
        self._compute_query(h, values)
        return values[-1].tolist()

    def train(self, input_array: list[float], target_output: list[float], previous_delta_w=None, new_delta_w=None, alpha=None, dynamic_lr=False, a=0, b=0):
        inp = np.array(input_array)[np.newaxis].T
        inp = NeuralNetwork._add_bias(inp)
        trg = np.array(target_output)[np.newaxis].T
        h = [inp]
        values = [inp]
        delta = {}
        self._compute_query(h, values)
        error = np.subtract(trg, values[-1])
        error_value = 0.5 * np.sum(error, axis=0) ** 2
        d = self.derivative(h[-1]) * error
        delta[self.layers - 1] = d

        for i in range(self.layers - 2, 0, -1):  # desde el ultimo al primero
            d = delta[i + 1]
            h_ = h[i]
            aux_weight = np.delete(self.weights[i].T, self.nodes_per_layer[i],
                                   axis=0)  # Le saco la ultima fila de W para no calcular el delta del bias
            tmp1 = np.dot(aux_weight, d)
            tmp2 = self.derivative(h_)
            delta[i] = tmp1 * tmp2

        delta_w = {}

        if dynamic_lr and self._last_error is not None:
            if self._last_error - error_value >= 0: # Si antes tenia mas error que ahora
                self.lr += a
            else:
                self.lr *= (1-b)

        for i in range(self.layers - 1):
            delta_w[i] = self.lr * np.dot(delta[i + 1], values[i].T)
            if previous_delta_w is not None and i in previous_delta_w:
                delta_w[i] += previous_delta_w[i] * alpha
            self.weights[i] = self.weights[i] + delta_w[i]
            if new_delta_w:
                new_delta_w[i] = delta_w[i]

        self._last_error = error_value
        return error_value

    @staticmethod
    def _add_bias(array):
        return np.vstack([array, np.array([1])])

    def _compute_query(self, h, values):
        for i in range(self.layers - 1):
            x = np.dot(self.weights[i], values[i])
            h.append(np.copy(x))
            x = self.activation(x)
            x = NeuralNetwork._add_bias(x)
            values.append(np.copy(x))

        values[-1] = np.delete(values[-1], self.nodes_per_layer[-1], axis=0)

    def save_network(self, name: str):
        data = {
            'total_layers': self.layers,
            'nodes_per_layer': self.nodes_per_layer,
            'learning_rate': self.lr
        }
        weights = []
        for w in self.weights:
            w_list = w.tolist()
            weights.append(w_list)

        data['weights'] = []
        for w in weights:
            data['weights'].append(w)
        with open(name, 'w') as file:
            json.dump(data, file)

    @classmethod
    def loadNN(cls, file_name, activation_function, derivative_activation):
        with open(file_name, 'r') as file:
            decoded = json.loads(file.read())
            aux = NeuralNetwork(decoded['total_layers'], decoded['nodes_per_layer'], activation_function,
                                derivative_activation, decoded['learning_rate'], init_random=False)
            for i in range(decoded['total_layers'] - 1):
                w = np.array(decoded['weights'][i]).reshape((aux.nodes_per_layer[i + 1], aux.nodes_per_layer[i] + 1))
                aux.weights.append(w)
            return aux

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def sigmoid_der(x):
        return NeuralNetwork.sigmoid(x) * (1 - NeuralNetwork.sigmoid(x))

    @staticmethod
    def tanh(x):
        return np.tanh(x)

    @staticmethod
    def tanh_der(x):
        return 1 - (np.tanh(x)) ** 2

    @staticmethod
    def sign(x):
        return (x > 0) * 1

    @staticmethod
    def sign_der(x):
        return 0