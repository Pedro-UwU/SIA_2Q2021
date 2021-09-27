import json
import math
import random

import numpy as np

from Config import Config
from ej2.Graph import Graph


class SimpleNonLinearPerceptron:
    training_values = None
    predicting_values = None
    training_expected_output = None
    predicting_expected_output = None
    weights = None
    steps = None
    learning_rate = None
    g_function = None
    betha = None
    minValue = None
    maxValue = None

    @staticmethod
    def initialize():
        SimpleNonLinearPerceptron.steps = Config.config.steps_ej1
        SimpleNonLinearPerceptron.weights = [0, 0, 0, 0]
        SimpleNonLinearPerceptron.learning_rate = float(Config.config.learning_rate_ej1)
        SimpleNonLinearPerceptron.betha = Config.config.betha
        if Config.config.function == "tanh":
            SimpleNonLinearPerceptron.g_function = SimpleNonLinearPerceptron.tanh
            SimpleNonLinearPerceptron.g_function_derivative = SimpleNonLinearPerceptron.tanh_derivative
        else:
            SimpleNonLinearPerceptron.g_function = SimpleNonLinearPerceptron.exponential
            SimpleNonLinearPerceptron.g_function_derivative = SimpleNonLinearPerceptron.exponential_derivative

        file = open('ej2/data.json')
        values = json.load(file)
        if Config.config.training_amount == "":
            SimpleNonLinearPerceptron.training_values = values['values']
            SimpleNonLinearPerceptron.predicting_values = values['values']
            SimpleNonLinearPerceptron.training_expected_output = values['expected_output']
            SimpleNonLinearPerceptron.predicting_expected_output = values['expected_output']
        else:
            SimpleNonLinearPerceptron.training_values = values['values'][:Config.config.training_amount]
            SimpleNonLinearPerceptron.training_expected_output = values['expected_output'][:Config.config.training_amount]
            SimpleNonLinearPerceptron.predicting_values = values['values'][Config.config.training_amount:]
            SimpleNonLinearPerceptron.predicting_expected_output = values['expected_output'][
                                                                Config.config.training_amount:]

        SimpleNonLinearPerceptron.minValue = min(np.array(values['values']).flatten())
        SimpleNonLinearPerceptron.maxValue = max(np.array(values['values']).flatten())

    @staticmethod
    def run():
        current_steps = 0
        step_error = 1
        error_min = 2 * len(SimpleNonLinearPerceptron.training_values)
        training_errors = []
        test_errors = []
        while abs(step_error) > 0 and current_steps < SimpleNonLinearPerceptron.steps:
            step_error = 0.0
            # index = random.randrange(0, len(SimpleNonLinearPerceptron.training_values))
            for index in range(len(SimpleNonLinearPerceptron.training_values)):
                excitement = SimpleNonLinearPerceptron.calculate_excitement(1, index)
                activation = SimpleNonLinearPerceptron.g_function(excitement)

                diff = SimpleNonLinearPerceptron.training_expected_output[index] - activation
                step_error += SimpleNonLinearPerceptron.calculate_error_quadratic(diff)

                SimpleNonLinearPerceptron.update_weights(index, excitement, diff)

            new_error = (0.5 * step_error) / len(SimpleNonLinearPerceptron.training_values)
            training_errors.append(new_error)
            if new_error < error_min:
                error_min = new_error
            current_steps += 1
            # print(f'Weights: {SimpleNonLinearPerceptron.weights}')
            print(f'Current step: {current_steps}, with new_error: {new_error}')

            [results, error] = SimpleNonLinearPerceptron.predict()
            test_errors.append(error)

        # Graph.graph_ej2(training_errors, test_errors)

    @staticmethod
    def predict():
        result = []
        error = 0.0
        for index in range(len(SimpleNonLinearPerceptron.predicting_values)):
            excitement = SimpleNonLinearPerceptron.calculate_excitement(0, index)
            activation = SimpleNonLinearPerceptron.g_function(excitement)

            normalized_activation = SimpleNonLinearPerceptron.normalize_value(activation)
            diff = SimpleNonLinearPerceptron.training_expected_output[index] - normalized_activation
            error += SimpleNonLinearPerceptron.calculate_error_quadratic(SimpleNonLinearPerceptron.denormalize_value(diff))

            result.append(activation)
            # print(f'Expected Value: {SimpleNonLinearPerceptron.predicting_expected_output[index]}, Obtained Value: {activation}')

        return [result, error]

    @staticmethod
    def calculate_error_quadratic(error):
        return 0.5 * pow(error, 2)

    # @staticmethod
    # def calculate_error_quadratic():
    #     total_error = 0
    #     for index in range(len(SimpleNonLinearPerceptron.training_values)):
    #         excitement = SimpleNonLinearPerceptron.calculate_excitement(1, index)
    #         activation = SimpleNonLinearPerceptron.g_function(excitement)
    #         total_error += pow(SimpleNonLinearPerceptron.training_expected_output[index] - activation, 2) * 0.5
    #     return total_error

    @staticmethod
    def update_weights(index, excitement, diff_error):
        values = SimpleNonLinearPerceptron.training_values[index]
        delta_w = SimpleNonLinearPerceptron.calculate_delta_weight(values, excitement, diff_error)

        SimpleNonLinearPerceptron.weights = np.add(SimpleNonLinearPerceptron.weights, delta_w)

    @staticmethod
    def calculate_delta_weight(values, excitement, diff_error):
        derivative = SimpleNonLinearPerceptron.g_function_derivative(excitement)
        delta_w = []
        for i in range(len(SimpleNonLinearPerceptron.weights)):
            if i == 0:
                delta_w.append(SimpleNonLinearPerceptron.learning_rate * diff_error * derivative)
            else:
                delta_w.append(SimpleNonLinearPerceptron.learning_rate * values[i - 1] * diff_error * derivative)

        return delta_w

    @staticmethod
    def calculate_excitement(training, index):
        if training == 1:
            row = SimpleNonLinearPerceptron.training_values[index]
        else:
            row = SimpleNonLinearPerceptron.predicting_values[index]
        total = 0
        for i in range(len(SimpleNonLinearPerceptron.weights)):
            if i == 0:
                total += SimpleNonLinearPerceptron.weights[i]
            else:
                total += SimpleNonLinearPerceptron.weights[i] * row[i - 1]

        return total

    @staticmethod
    def exponential(value):
        return 1 / (1 + math.exp(-2 * SimpleNonLinearPerceptron.betha * value))

    @staticmethod
    def exponential_derivative(value):
        original = SimpleNonLinearPerceptron.exponential(value)
        return 2 * SimpleNonLinearPerceptron.betha * original * (1 - original)

    @staticmethod
    def tanh(value):
        return math.tanh(SimpleNonLinearPerceptron.betha * value)

    @staticmethod
    def tanh_derivative(value):
        original = SimpleNonLinearPerceptron.tanh(value)
        return SimpleNonLinearPerceptron.betha * (1 - pow(original, 2))

    @staticmethod
    def denormalize_value(value):
        return value * (SimpleNonLinearPerceptron.maxValue - SimpleNonLinearPerceptron.minValue) + SimpleNonLinearPerceptron.minValue

    @staticmethod
    def normalize_value(value):
        return (value - SimpleNonLinearPerceptron.minValue) / (SimpleNonLinearPerceptron.maxValue - SimpleNonLinearPerceptron.minValue)
