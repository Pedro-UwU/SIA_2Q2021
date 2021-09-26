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

        self.hidden_layers_ej3_2 = parser.getint('ej3_2', 'HIDDEN_LAYERS')
        self.nodes_per_layer_ej3_2 = parser.get('ej3_2', 'NODES_PER_LAYER')
        self.epochs_ej3_2 = parser.getint('ej3_2', 'EPOCHS')
        self.testing_division_ej3_2 = parser.getint('ej3_2', 'TESTING_DIVISION')
        self.learning_rate_ej3_2 = parser.getfloat('ej3_2', 'LEARNING_RATE')

    @staticmethod
    def init_config(config_name: str):
        Config.config = Config(config_name)
