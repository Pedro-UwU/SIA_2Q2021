import random

from Config import Config

class SimplePerceptron:
    values = [[-1, 1], [1, -1], [-1, -1], [1, 1]]
    weights = None
    size = None
    expected_output = None
    steps = None

    @staticmethod
    def initialize():
        SimplePerceptron.steps = Config.config.steps_ej1
        SimplePerceptron.size = len(SimplePerceptron.values)
        SimplePerceptron.weights = [0, 0, 0]
        if Config.config.operation_ej1 == "XOR":
            SimplePerceptron.expected_output = [-1, -1, -1, 1]
        elif Config.config.operation_ej1 == "AND":
            SimplePerceptron.expected_output = [1, 1, -1, -1]
        else:
            # Should raise error
            pass

    @staticmethod
    def run():
        current_steps = 0
        error = 1
        error_min = 2 * SimplePerceptron.size
        while abs(error) > 0 and current_steps < SimplePerceptron.steps:
            index = random.randrange(0, SimplePerceptron.size)
            excitement = SimplePerceptron.calculate_excitement(index)
            activation = SimplePerceptron.calculate_activation(excitement)
            SimplePerceptron.update_weights(index, activation)
            new_error = SimplePerceptron.calculate_error()
            if new_error < error_min:
                error_min = new_error
            current_steps += 1
            print(f'Current step: {current_steps}, with new_error: {new_error}')

        SimplePerceptron.predict()

    @staticmethod
    def predict():
        result = []
        for index in range(len(SimplePerceptron.values)):
            excitement = SimplePerceptron.calculate_excitement(index)
            activation = SimplePerceptron.calculate_activation(excitement)
            result.append(activation)

            print(f'Expected Value: {SimplePerceptron.expected_output[index]}, Obtained Value: {activation}')

    @staticmethod
    def calculate_error():
        total_error = 0
        for index in range(len(SimplePerceptron.values)):
            excitement = SimplePerceptron.calculate_excitement(index)
            activation = SimplePerceptron.calculate_activation(excitement)
            total_error += abs(SimplePerceptron.expected_output[index] - activation)
        return total_error


    @staticmethod
    def update_weights(index, activation):
        delta_w = SimplePerceptron.calculate_delta_weight(index, activation)
        new_weights = []
        for i in range(2):
            new_weights.append(SimplePerceptron.weights[i] + delta_w[i])

        SimplePerceptron.weights = new_weights

    @staticmethod
    def calculate_delta_weight(index, activation):
        output_aux = SimplePerceptron.expected_output[index] - activation
        delta_w = []
        for i in SimplePerceptron.values[index]:
            delta_w.append(0.01 * i * output_aux)

        return delta_w


    @staticmethod
    def calculate_excitement(index):
        row = SimplePerceptron.values[index]
        total = 0
        for i in range(len(SimplePerceptron.weights)):
            if i == 2:
                total += SimplePerceptron.weights[i]
            else:
                total += SimplePerceptron.weights[i] * row[i]

        return total

    @staticmethod
    def calculate_activation(excitement):
        return -1.0 if excitement < 0.0 else 1.0
