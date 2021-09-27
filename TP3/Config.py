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
        self.learning_rate_ej1 = parser.get('ej1', 'LEARNING_RATE')

        self.steps_ej2 = parser.getint('ej2', 'STEPS')
        self.learning_rate_ej2 = parser.get('ej2', 'LEARNING_RATE')
        self.error_method = parser.get('ej2', 'ERROR_FUNCTION')
        self.training_amount = parser.get('ej2', 'TRAINING_AMOUNT')
        self.betha = parser.getfloat('ej2', 'BETHA')
        self.is_linear = parser.get('ej2', 'IS_LINEAR')
        self.function = parser.get('ej2', 'FUNCTION')

    @staticmethod
    def init_config(config_name: str):
        Config.config = Config(config_name)
