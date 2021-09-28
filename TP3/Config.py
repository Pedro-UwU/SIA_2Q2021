import configparser
import os


class Config:
    config = None

    def __init__(self, config_name: str):
        parser = configparser.ConfigParser()
        parser.read(config_name)

        self.exercise = parser.getint('config', 'EXERCISE')

        self.operation_ej1 = parser.get('ej1', 'OPERATION')
        self.steps_ej1 = parser.getint('ej1', 'STEPS')

        self.operation_ej2 = parser.get('ej2', 'OPERATION')
        self.steps_ej2 = parser.getint('ej2', 'STEPS')
        self.betha = parser.get('ej2', 'BETHA')
        self.is_linear = parser.get('ej2', 'IS_LINEAR')
        self.function = parser.get('ej2', 'FUNCTION')

        self.hidden_layers_ej3_1 = parser.getint('ej3_1', 'HIDDEN_LAYERS')
        self.nodes_per_layer_ej3_1 = parser.get('ej3_1', 'NODES_PER_LAYER')
        self.learning_rate_ej3_1 = parser.getfloat('ej3_1', 'LEARNING_RATE')
        self.epochs_ej3_1 = parser.getint('ej3_1', 'EPOCHS')

        self.hidden_layers_ej3_2 = parser.getint('ej3_2', 'HIDDEN_LAYERS')
        self.nodes_per_layer_ej3_2 = parser.get('ej3_2', 'NODES_PER_LAYER')
        self.epochs_ej3_2 = parser.getint('ej3_2', 'EPOCHS')
        self.testing_division_ej3_2 = parser.getint('ej3_2', 'TESTING_DIVISION')
        self.learning_rate_ej3_2 = parser.getfloat('ej3_2', 'LEARNING_RATE')
        self.momentum_ej3_2 = parser.getboolean('ej3_2', 'MOMENTUM')
        self.alpha_ej3_2 = parser.getfloat('ej3_2', 'ALPHA_MOMENTUM')
        self.total_nn_ej3_2 = parser.getint('ej3_2', 'TOTAL_NN')
        self.graph_choice_ej3_2 = parser.get('ej3_2', 'GRAPH')
        self.dynamic_lr_ej3_2 = parser.getboolean('ej3_2', 'DYNAMIC_LEARNING_RATE')
        self.a_ej3_2 = parser.getfloat('ej3_2', 'A')
        self.b_ej3_2 = parser.getfloat('ej3_2', 'B')
        self.per_epoch_training_ej3_2 = parser.getboolean('ej3_2', 'PER_EPOCH_TRAINING')

        self.hidden_layers_ej3_3 = parser.getint('ej3_3', 'HIDDEN_LAYERS')
        self.nodes_per_layer_ej3_3 = parser.get('ej3_3', 'NODES_PER_LAYER')
        self.epochs_ej3_3 = parser.getint('ej3_3', 'EPOCHS')
        self.testing_division_ej3_3 = parser.getint('ej3_3', 'TESTING_DIVISION')
        self.learning_rate_ej3_3 = parser.getfloat('ej3_3', 'LEARNING_RATE')
        self.momentum_ej3_3 = parser.getboolean('ej3_3', 'MOMENTUM')
        self.alpha_ej3_3 = parser.getfloat('ej3_3', 'ALPHA_MOMENTUM')
        self.total_nn_ej3_3 = parser.getint('ej3_3', 'TOTAL_NN')
        self.graph_choice_ej3_3 = parser.get('ej3_3', 'GRAPH')
        self.dynamic_lr_ej3_3 = parser.getboolean('ej3_3', 'DYNAMIC_LEARNING_RATE')
        self.a_ej3_3 = parser.getfloat('ej3_3', 'A')
        self.b_ej3_3 = parser.getfloat('ej3_3', 'B')
        self.graph_plot_ej3_3 = parser.get('ej3_3', 'GRAPH_PLOT')
        self.noise_ej3_3 = parser.getboolean('ej3_3', 'TEST_NOISE')
        self.noise_prob_ej3_3 = parser.getfloat('ej3_3', 'NOISE_PROBABILITY')
        self.per_epoch_training_ej3_3 = parser.getboolean('ej3_3', 'PER_EPOCH_TRAINING')

    @staticmethod
    def init_config(config_name: str):
        Config.config = Config(config_name)
