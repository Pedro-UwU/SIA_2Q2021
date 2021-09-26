import math
import random
import numpy as np
import matplotlib.pyplot as plt

from Config import Config
from ej3.NeuralNetwork import NeuralNetwork


def ej3_2():
    # leer los numeros
    numbers = get_numbers()
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

    for repetition in range(50):
        nn = NeuralNetwork(total_layers, nodes_per_layer, NeuralNetwork.sigmoid, NeuralNetwork.sigmoid_der,
                           Config.config.learning_rate_ej3_2)
        training_acc = []
        testing_acc = []
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
                target = [0, 0]  # primero si es par, segundo si es impar
                target[case[0] % 2] = 1
                inputs = case[1]
                nn.train(inputs, target)

            # testeo con los casos de prueba
            test_acc, test_pres, test_recall, test_f1 = test(nn, output_layers, testing)
            train_acc, train_pres, train_recall, train_f1 = test(nn, output_layers, training)
            training_acc.append(train_acc)
            testing_acc.append(test_acc)
        training_values.append(training_acc)
        testing_values.append(testing_acc)

    training_values = np.array(training_values)
    testing_values = np.array(testing_values)
    training_avg = [np.mean(training_values[:, x]) for x in range(epochs)]
    testing_avg = [np.mean(testing_values[:, x]) for x in range(epochs)]
    x_axis = [x for x in range(epochs)]

    plt.plot(x_axis, training_avg, label='training')
    plt.plot(x_axis, testing_avg, label='testing')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
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
        pres = math.inf
    else:
        pres = tp / (tp + fp)

    if tp + fn == 0:
        recall = math.inf
    else:
        recall = tp / (tp + fn)

    if (pres + recall) == 0:
        f1 = math.inf
    else:
        f1 = 2 * pres * recall / (pres + recall)
    return acc, pres, recall, f1


def get_numbers():
    file = open('./numeros.txt', 'r')
    lines = file.readlines()
    file.close()
    numbers = []
    for i in range(10):
        digits = []
        number = i
        for j in range((i * 7), (i * 7 + 7)):
            for c in lines[j]:
                if c == '0' or c == '1':
                    digits.append(int(c))
        numbers.append((number, digits.copy()))
    return numbers


if __name__ == '__main__':
    Config.init_config('../config.conf')
    nn = ej3_2()
    number = 0
    numbers = get_numbers()
    while 0 <= number < 10:
        number = int(input('enter a number\n>>'))
        inputs = numbers[number][1]
        result = nn.query(inputs)
        answer = np.argmax(result)
        print(f'Your number is {"odd" if answer == 1 else "even"}')
