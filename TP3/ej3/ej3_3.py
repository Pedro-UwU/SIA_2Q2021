import random
import numpy as np

from Config import Config
from ej3 import NumberReader
from ej3.NeuralNetwork import NeuralNetwork


def ej3_3():
    # leer los numeros
    numbers = NumberReader.get_numbers()
    epochs = Config.config.epochs_ej3_3
    total_layers = Config.config.hidden_layers_ej3_3 + 2
    nodes_per_layer = [int(x) for x in Config.config.nodes_per_layer_ej3_3.split(',')]
    nodes_per_layer.insert(0, 5 * 7)  # input
    output_layers = 10
    nodes_per_layer.append(output_layers)  # output

    testing_division = Config.config.testing_division_ej3_3

    training_values = []
    testing_values = []

    for repetition in range(Config.config.total_nn_ej3_2):
        nn = NeuralNetwork(total_layers, nodes_per_layer, NeuralNetwork.sigmoid, NeuralNetwork.sigmoid_der,
                           Config.config.learning_rate_ej3_2)
        training_results = []
        testing_results = []
        last_delta = {}
        new_delta = {}
        for epoch in range(epochs):
            # veo que seccion de los numeros es testing:
            # Elijo 4 numeros como test
            training = numbers.copy()
            testing = []
            for i in range(testing_division):
                aux = random.choice(training)
                testing.append(aux)
                training.remove(aux)

            # entreno la red con esos numeros
            random.shuffle(training)
            for case in training:
                target = [0 for _ in range(10)] # primero si es par, segundo si es impar
                target[case[0]] = 1
                inputs = case[1]
                if Config.config.momentum_ej3_2:
                    nn.train(inputs, target, previous_delta_w=last_delta, new_delta_w=new_delta, alpha=0.9, dynamic_lr=Config.config.dynamic_lr_ej3_2, a=Config.config.a_ej3_2, b=Config.config.b_ej3_2)
                else:
                    nn.train(inputs, target, dynamic_lr=Config.config.dynamic_lr_ej3_2, a=Config.config.a_ej3_2, b=Config.config.b_ej3_2)

                    # testeo con los casos de prueba
                    test_acc, test_pres, test_recall, test_f1 = test(nn, output_layers, testing)
                    train_acc, train_pres, train_recall, train_f1 = test(nn, output_layers, training)
                    choice = Config.config.graph_choice_ej3_2
                    if choice == 'ACCURACY':
                        training_results.append(train_acc)
                        testing_results.append(test_acc)
                    elif choice == 'PRECISION':
                        training_results.append(train_pres)
                        testing_results.append(test_pres)
                    elif choice == 'RECALL':
                        training_results.append(train_recall)
                        testing_results.append(test_recall)
                    elif choice == 'F1':
                        training_results.append(train_f1)
                        testing_results.append(test_f1)

def test(nn, output_layers, test_set):
    confusion = np.array([[0 for _ in range(output_layers)] for _ in range(output_layers)])
    for case in test_set:
        result = np.argmax(nn.query(case[1]))
        target = case[0]
        confusion[target][result] += 1

if __name__ == '__main__':
    Config.init_config('../config.conf')
    ej3_3()
