import configparser
import os

from DataReader import DataReader


class Config:
    config = None

    def __init__(self, config_name: str):
        parser = configparser.ConfigParser()
        parser.read(config_name)
        self.data_dir = os.path.join(os.path.dirname(__file__), parser.get('config', 'DATA_DIR'))
        self.total_weapons = parser.getint('config', 'TOTAL_WEAPONS')
        self.total_boots = parser.getint('config', 'TOTAL_BOOTS')
        self.total_helmets = parser.getint('config', 'TOTAL_HELMETS')
        self.total_gloves = parser.getint('config', 'TOTAL_GLOVES')
        self.total_chestplates = parser.getint('config', 'TOTAL_CHESTPLATES')

        self.N = parser.getint('genetic_algorithm', 'N')
        self.K = parser.getint('genetic_algorithm', 'K')
        self.genetic_implementation = parser.get('genetic_algorithm', 'IMPLEMENTATION')

        self.A = parser.getfloat('selection', 'A')
        self.B = parser.getfloat('selection', 'B')
        self.method1 = parser.get('selection', 'METHOD_1')
        self.method2 = parser.get('selection', 'METHOD_2')
        self.method3 = parser.get('selection', 'METHOD_3')
        self.method4 = parser.get('selection', 'METHOD_4')

        self.mutation_method = parser.get('mutation', 'METHOD')
        self.mutation_prob = parser.getfloat('mutation', 'MUTATION_PROB')

    @staticmethod
    def init_config(config_name: str):
        Config.config = Config(config_name)