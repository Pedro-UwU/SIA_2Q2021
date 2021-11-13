import math
import random
import numpy as np
import matplotlib.pyplot as plt

from Config import Config
from ej3 import NumberReader
from ej3.NeuralNetwork import NeuralNetwork


def ej3_2():
    # leer los numeros
    numbers = NumberReader.get_numbers()
    epochs = Config.config.epochs_ej3_2
    total_layers = Config.config.hidden_layers_ej3_2 + 2
    nodes_per_layer = [int(x) for x in Config.config.nodes_per_layer_ej3_2.split(',')]
    nodes_per_layer.insert(0, 5 * 7)  # input
    output_layers = 2
    nodes_per_layer.append(output_layers)  # output
    print(nodes_per_layer)

    testing_division = Config.config.testing_division_ej3_2

    training_values = []
    testing_values = []


   # random.shuffle(training)
    for repetition in range(Config.config.total_nn_ej3_2):
        print(f'Run: {repetition}')
        nn = NeuralNetwork(total_layers, nodes_per_layer, NeuralNetwork.linear, NeuralNetwork.linear_der,
                           Config.config.learning_rate_ej3_2)
        training_results = []
        testing_results = []
        last_delta = {}
        new_delta = {}
        training = numbers.copy()
        testing = []
        if not Config.config.per_epoch_training_ej3_2:
            for i in range(testing_division):
                aux = random.choice(training)
                testing.append(aux)
                training.remove(aux)
        for epoch in range(epochs):
            # # veo que seccion de los numeros es testing:

            if Config.config.per_epoch_training_ej3_2:
                # Elijo 4 numeros como test
                training = numbers.copy()
                testing = []
                for i in range(testing_division):
                    aux = random.choice(training)
                    testing.append(aux)
                    training.remove(aux)

            random.shuffle(training)
            for case in training:
                target = [0, 0]  # primero si es par, segundo si es impar
                target[case[0] % 2] = 1
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

        training_values.append(training_results)
        testing_values.append(testing_results)

    training_values = np.array(training_values)
    testing_values = np.array(testing_values)
    training_avg = [np.mean(training_values[:, x]) for x in range(epochs)]
    testing_avg = [np.mean(testing_values[:, x]) for x in range(epochs)]
    x_axis = [x for x in range(epochs)]

    plt.plot(x_axis, training_avg, label='training')
    plt.plot(x_axis, testing_avg, label='testing')
    plt.xlabel('Epochs')
    plt.ylabel(Config.config.graph_choice_ej3_2.lower().capitalize())
    plt.title('EJ 3.2')
    plt.legend()
    plt.show()

    return nn


def test(nn, output_layers, test_set):
    # creo la matriz de confusion
    confusion = np.array([[0 for _ in range(output_layers)] for _ in range(output_layers)])
    for case in test_set:
        result = np.argmax(nn.query(case[1]))
        target = case[0] % 2
        confusion[target][result] += 1
    tp = confusion[0][0]  # es par
    tn = confusion[1][1]  # es impar
    fp = confusion[1][0]  # es impar pero cree que era par
    fn = confusion[0][1]  # es par pero cree que es impar
    acc = (tp + tn) / (tp + tn + fp + fn)
    if (tp + fp) == 0:
        pres = 0
    else:
        pres = tp / (tp + fp)

    if tp + fn == 0:
        recall = 0
    else:
        recall = tp / (tp + fn)

    if (pres + recall) == 0:
        f1 = 0
    else:
        f1 = 2 * pres * recall / (pres + recall)
    return acc, pres, recall, f1


if __name__ == '__main__':
    Config.init_config('../config.conf')
    nn = ej3_2()
    # number = 0
    # numbers = NumberReader.get_numbers()
    # while 0 <= number < 10:
    #     number = int(input('enter a number\n>>'))
    #     inputs = numbers[number][1]
    #     result = nn.query(inputs)
    #     answer = np.argmax(result)
    #     print(f'Your number is {"odd" if answer == 1 else "even"}')
