import random
import numpy as np
import matplotlib.pyplot as plt
import os

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
    noise_values = []

    for repetition in range(Config.config.total_nn_ej3_3):
        nn = NeuralNetwork(total_layers, nodes_per_layer, NeuralNetwork.sigmoid, NeuralNetwork.sigmoid_der,
                           Config.config.learning_rate_ej3_3)
        training_results = []
        testing_results = []
        noise_results = []
        last_delta = {}
        new_delta = {}
        training = numbers.copy()
        testing = []
        if not Config.config.per_epoch_training_ej3_3:
            for i in range(testing_division):
                aux = random.choice(training)
                testing.append(aux)
                training.remove(aux)
        for epoch in range(epochs):
            # veo que seccion de los numeros es testing:
            # Elijo 4 numeros como test
            if Config.config.per_epoch_training_ej3_3:
                training = numbers.copy()
                testing = []
                for i in range(testing_division):
                    aux = random.choice(training)
                    testing.append(aux)
                    training.remove(aux)

            # entreno la red con esos numeros
            random.shuffle(training)
            for case in training:
                target = [0 for _ in range(10)]  # primero si es par, segundo si es impar
                target[case[0]] = 1
                inputs = case[1]
                if Config.config.momentum_ej3_3:
                    nn.train(inputs, target, previous_delta_w=last_delta, new_delta_w=new_delta, alpha=0.9,
                             dynamic_lr=Config.config.dynamic_lr_ej3_3, a=Config.config.a_ej3_3,
                             b=Config.config.b_ej3_3)
                else:
                    nn.train(inputs, target, dynamic_lr=Config.config.dynamic_lr_ej3_3, a=Config.config.a_ej3_3,
                             b=Config.config.b_ej3_3)

                    # testeo con los casos de prueba
            testing_data = test(nn, output_layers, testing)
            training_data = test(nn, output_layers, training)
            training_results.append(training_data)
            testing_results.append(testing_data)

            if Config.config.noise_ej3_3:
                inputs = generate_noise(numbers, Config.config.noise_prob_ej3_3)
                noise_data = test(nn, output_layers, inputs)
                noise_results.append(noise_data)

        if Config.config.noise_ej3_3:
            noise_values.append(noise_results)
        training_values.append(training_results)
        testing_values.append(testing_results)

        # testing_values -> lista de los resultados de cada repeticion
        # testing_result -> lista de los testing data de cada epoch
        # testing_data -> lista de los datos de cada training case
        # si quiero el avg_acc del primer epoch de la primera repeticion -> testing_values[0][0][0]

    # test con ruido


    graph_plotting = Config.config.graph_plot_ej3_3
    index = 0
    plotting_options = {
        0: 'Average',
        1: 'Max',
        2: 'Min'

    }
    if not Config.config.noise_ej3_3:
        if Config.config.graph_choice_ej3_3 == 'ACCURACY':
            calculate_avgs(training_values, epochs, 0, f'Average Accuracy Training', plt)
            calculate_avgs(testing_values, epochs, 0, f'Average Accuracy Testing', plt)
            plt.ylabel('Accuracy')

        elif Config.config.graph_choice_ej3_3 == 'PRECISION':
            calculate_avgs(training_values, epochs, 3, f'Average Precision Training', plt)
            calculate_avgs(testing_values, epochs, 3, f'Average Precision Testing', plt)
            plt.ylabel('Precision')
        plt.xlabel('Epochs')
    else:
        distribution = np.zeros((Config.config.total_nn_ej3_3, 1))
        for i in range(Config.config.total_nn_ej3_3):
            value = noise_values[i][epochs-1][3]
            distribution[i][0] = value
        print(distribution)
        plt.hist(distribution, histtype='bar')
        plt.xlabel('Precision')
        plt.ylabel('Number of Neural Networks')

    plt.title('EJ 3-3')
    plt.legend()
    plt.show()






def calculate_avgs(initial_values, total_epochs, index, title: str, plot):
    values = []
    for v in initial_values:
        aux_value = []
        for x in v:
            aux_value.append(x[index])
        values.append(aux_value)
    values = np.array(values)
    avg_value = [np.mean(values[:, i]) for i in range(total_epochs)]
    x_axis = [x for x in range(total_epochs)]
    plot.plot(x_axis, avg_value, label=title.lower().capitalize())


def test(nn, output_layers, test_set):
    if len(test_set) == 0:
        return [0, 0, 0, 0, 0, 0]
    confusion = np.array([[0 for _ in range(output_layers)] for _ in range(output_layers)])
    for case in test_set:
        result = np.argmax(nn.query(case[1]))
        target = case[0]
        confusion[target][result] += 1

    # una vez creada la matriz de confusion, calculo los stats de cada clase:
    total_acc = 0
    total_prec = 0
    max_acc = 0
    max_prec = 0
    min_acc = 0
    min_prec = 0
    for i in range(len(test_set)):
        tp, tn, fp, fn = get_stats(confusion, test_set[i][0], output_layers)
        try:
            acc = (tp + tn) / (tp + tn + fn + fp)
        except:
            acc = 0
        prec = 0
        if tp + fp > 0:
            prec = tp / (tp + fp)
        total_acc += acc
        total_prec += prec

        if acc > max_acc:
            max_acc = acc
        if acc < min_acc:
            min_acc = acc

        if prec > max_prec:
            max_prec = prec
        if prec < min_prec:
            min_prec = prec
    avg_acc = total_acc / len(test_set)
    avg_prec = total_prec / len(test_set)

    return [avg_acc, max_acc, min_acc, avg_prec, max_prec, min_prec]

def generate_noise(inputs, noise_prob):
    outputs = []
    for i in inputs:
        value = i[0]
        digits = i[1].copy()
        for d in range(len(digits)):
            dice = random.uniform(0, 1)
            if dice < noise_prob:
                if digits[d] == 0:
                    digits[d] = 1
                elif digits[d] == 1:
                    digits[d] = 0
        outputs.append((value, digits))
    return outputs


def get_stats(confusion, class_number, matrix_size):
    tp = 0
    fn = 0
    fp = 0
    tn = 0
    for i in range(matrix_size):
        for j in range(matrix_size):
            if i == j and i == class_number:
                tp += confusion[i][j]
                continue
            elif i == class_number:
                fn += confusion[i][j]
            elif j == class_number:
                fp += confusion[i][j]
            else:
                tn += confusion[i][j]
    # for i in range(matrix_size):
    #     if i != class_number:
    #         fn += confusion[class_number][i]
    #
    # fp = 0
    # for i in range(matrix_size):
    #     if i != class_number:
    #         fp += confusion[i][class_number]
    # tn = 0
    # for i in range(matrix_size):
    #     if i == class_number:
    #         continue
    #     for j in range(matrix_size):
    #         if j == class_number:
    #             continue
    #         tn += confusion[i][j]
    return tp, tn, fp, fn


if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    configPath = os.path.join(dirname, '../config.conf')
    Config.init_config(configPath)
    ej3_3()
