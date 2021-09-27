import json
import random

import numpy as np

from Config import Config


class SimpleLinearPerceptron:
    training_values = None
    predicting_values = None
    training_expected_output = None
    predicting_expected_output = None
    weights = None
    steps = None
    learning_rate = None
    error_method = None

    @staticmethod
    def initialize():
        SimpleLinearPerceptron.steps = Config.config.steps_ej1
        SimpleLinearPerceptron.weights = [0, 0, 0, 0]
        SimpleLinearPerceptron.learning_rate = float(Config.config.learning_rate_ej1)
        if Config.config.error_method == "normal":
            SimpleLinearPerceptron.error_method = SimpleLinearPerceptron.calculate_error_normal
        else:
            SimpleLinearPerceptron.error_method = SimpleLinearPerceptron.calculate_error_quadratic

        file = open('ej2/data.json')
        values = json.load(file)
        if Config.config.training_amount == "":
            SimpleLinearPerceptron.training_values = values['values']
            SimpleLinearPerceptron.predicting_values = values['values']
            SimpleLinearPerceptron.training_expected_output = values['expected_output']
            SimpleLinearPerceptron.predicting_expected_output = values['expected_output']
        else:
            SimpleLinearPerceptron.training_values = values['values'][:Config.config.training_amount]
            SimpleLinearPerceptron.training_expected_output = values['expected_output'][:Config.config.training_amount]
            SimpleLinearPerceptron.predicting_values = values['values'][Config.config.training_amount:]
            SimpleLinearPerceptron.predicting_expected_output = values['expected_output'][Config.config.training_amount:]

    @staticmethod
    def run():
        current_steps = 0
        error = 1
        error_min = 2 * len(SimpleLinearPerceptron.training_values)
        while abs(error) > 0 and current_steps < SimpleLinearPerceptron.steps:
            index = random.randrange(0, len(SimpleLinearPerceptron.training_values))
            activation = SimpleLinearPerceptron.calculate_excitement(1, index)
            SimpleLinearPerceptron.update_weights(index, activation)
            new_error = SimpleLinearPerceptron.error_method()
            if new_error < error_min:
                error_min = new_error
            current_steps += 1
            # print(f'Weights: {SimpleLinearPerceptron.weights}')
            print(f'Current step: {current_steps}, with new_error: {new_error}')

        SimpleLinearPerceptron.predict()

    @staticmethod
    def predict():
        result = []
        for index in range(len(SimpleLinearPerceptron.predicting_values)):
            activation = SimpleLinearPerceptron.calculate_excitement(0, index)
            result.append(activation)
            print(f'Expected Value: {SimpleLinearPerceptron.predicting_expected_output[index]}, Obtained Value: {activation}')

    @staticmethod
    def calculate_error_normal():
        total_error = 0
        for index in range(len(SimpleLinearPerceptron.training_values)):
            activation = SimpleLinearPerceptron.calculate_excitement(1, index)
            total_error += abs(SimpleLinearPerceptron.training_expected_output[index] - activation)
        return total_error

    @staticmethod
    def calculate_error_quadratic():
        total_error = 0
        for index in range(len(SimpleLinearPerceptron.training_values)):
            activation = SimpleLinearPerceptron.calculate_excitement(1, index)
            total_error += pow(SimpleLinearPerceptron.training_expected_output[index] - activation, 2) * 0.5
        return total_error

    @staticmethod
    def update_weights(index, activation):
        delta_w = SimpleLinearPerceptron.calculate_delta_weight(index, activation)
        new_weights = []
        for i in range(4):
            new_weights.append(SimpleLinearPerceptron.weights[i] + delta_w[i])

        SimpleLinearPerceptron.weights = new_weights

    @staticmethod
    def calculate_delta_weight(index, activation):
        output_aux = SimpleLinearPerceptron.training_expected_output[index] - activation
        delta_w = []
        for i in range(len(SimpleLinearPerceptron.weights)):
            if i == 0:
                delta_w.append(SimpleLinearPerceptron.learning_rate * output_aux)
            else:
                value = SimpleLinearPerceptron.training_values[index][i - 1]
                delta_w.append(SimpleLinearPerceptron.learning_rate * value * output_aux)

        return delta_w

    @staticmethod
    def calculate_excitement(training, index):
        if training == 1:
            row = SimpleLinearPerceptron.training_values[index]
        else:
            row = SimpleLinearPerceptron.predicting_values[index]
        total = 0
        for i in range(len(SimpleLinearPerceptron.weights)):
            if i == 0:
                total += SimpleLinearPerceptron.weights[i]
            else:
                total += SimpleLinearPerceptron.weights[i] * row[i - 1]

        return total

    # @staticmethod
    # def get_best_w():
    #     values = SimpleLinearPerceptron.predicting_values
    #     column_1 = []
    #     column_2 = []
    #     column_3 = []
    #     column_4 = []
    #     for x1, x2, x3 in values:
    #         column_1.append(x1)
    #         column_2.append(x2)
    #         column_3.append(x3)
    #         column_4.append(1.0)
    #
    #     matrix = [column_1, column_2, column_3, column_4]
    #     transpose = np.transpose(matrix)
    #     # inverse = np.linalg.inv(matrix)
    #     aux = np.dot(np.dot(transpose, matrix), transpose)
    #     print(f'best_w = {np.dot(SimpleLinearPerceptron.predicting_expected_output, aux)}')
