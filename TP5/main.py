from Autoencoder import Autoencoder
from MultilayerPerceptron import MultilayerPerceptron


def main():
    ae = Autoencoder([5, 3, 2], MultilayerPerceptron.tanh, MultilayerPerceptron.tanh_der, 0.1)
    for i in range(100):
        ae.train([-0.3, -0.2, 0.1, 0.2, 0.5])

if __name__ == '__main__':
    main()