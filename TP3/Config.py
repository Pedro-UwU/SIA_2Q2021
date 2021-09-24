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

    @staticmethod
    def init_config(config_name: str):
        Config.config = Config(config_name)
