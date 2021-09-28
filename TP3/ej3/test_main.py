from NeuralNetwork import NeuralNetwork
import numpy as np
import matplotlib.pyplot

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_der(x):
    return sigmoid(x) * (1 - sigmoid(x))


def tanh(x):
    return np.tanh(x)


def tanh_der(x):
    return 1 - (np.tanh(x)) ** 2

def testMNIST(n: NeuralNetwork):
    okey = 0
    total = 0
    test = open("./mnist_test.csv")
    test_list = test.readlines()
    test.close()
    for line in test_list:
        all_values = line.split(',')
        inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        target = int(all_values[0])
        result: np.ndarray
        result = np.array(n.query(inputs))
        guess = np.argmax(result)
        if target == guess:
            okey += 1
        total += 1
    print(f'Total Tests: {total}')
    print(f'Asserts: {okey}')
    print(f'RESULT: {okey / total * 100}%')

def trainMNIST(n: NeuralNetwork):
    data = open("./mnist_train.csv", 'r')
    data_list = data.readlines()
    data.close()
    training_rep = 0
    epochs = 4
    for i in range(epochs):
        for line in data_list:
            all_values = line.split(',')
            inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            targets = np.zeros(10)
            targets[int(all_values[0])] = 1
            n.train(inputs, targets)
            training_rep += 1
            if training_rep % (epochs*600) == 0:
                print(f'training: {int(training_rep/(60000*epochs)*100)}%')



def main():
    n = NeuralNetwork(3, [28*28, 125, 10], sigmoid, sigmoid_der, 0.1)
    trainMNIST(n)
    n.save_network('digit_reader.json')
    testMNIST(n)
    n2 = NeuralNetwork.loadNN('digit_reader.json', sigmoid, sigmoid_der)
    testMNIST(n2)



if __name__ == '__main__':
    main()
