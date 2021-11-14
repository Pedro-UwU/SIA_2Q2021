import json

from MultilayerPerceptron import MultilayerPerceptron


class Autoencoder:
    def __init__(self, structure, activation_function, activation_derivative, learning_rate, init_mp=True):
        mirror = list(reversed(structure.copy()))
        mirror.pop(0)
        self.structure = [*structure, *mirror]
        print(self.structure)
        self.latent_index = len(structure) - 1

        if init_mp:
            self.multilayer_perceptron = MultilayerPerceptron(len(self.structure), self.structure, activation_function, activation_derivative, learning_rate=learning_rate)
        else:
            self.multilayer_perceptron = None

    def query(self, input_data):
        result, z = self.multilayer_perceptron.query_with_layer_value(input_data, layer=self.latent_index)
        return result, z

    def train(self, input_data, target_data, last_delta=None, new_delta=None, alpha=None, dynamic_lr=False, a=None, b=None):
        error = self.multilayer_perceptron.train(input_data, target_data, previous_delta_w=last_delta, new_delta_w=new_delta, alpha=alpha, dynamic_lr=dynamic_lr, a=a, b=b)
        return error

    def queryZ(self, input_Z):
        new_structure = self.structure[(len(self.structure)//2):]
        print(new_structure)
        mm = MultilayerPerceptron(len(new_structure), new_structure, self.multilayer_perceptron.activation, self.multilayer_perceptron.derivative, self.multilayer_perceptron.lr ,init_random=False)
        new_weights = self.multilayer_perceptron.weights[(len(self.structure)//2):]
        mm.weights = new_weights
        return mm.query(input_Z)

    @classmethod
    def load_autoencoder(cls, filename, activation, activation_der):
        file = open(filename, 'r')
        data = json.load(file)
        structure = data['nodes_per_layer']
        structure = structure[:(len(structure)//2 + 1)]
        total_nodes = data['total_layers']
        lr = data['learning_rate']
        ae = Autoencoder(structure, activation, activation_der, lr, init_mp=False)
        ae.multilayer_perceptron = MultilayerPerceptron.loadNN(filename, activation, activation_der)
        return ae

if __name__ == '__main__':
    ae = Autoencoder([2,2], MultilayerPerceptron.linear, MultilayerPerceptron.linear_der, 0.1)
    for i in range(100):
        error = ae.train([0.1, 0.2])
        print(error[0])