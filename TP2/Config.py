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
        self.boltzmann = parser.getfloat('selection', 'BOLTZMANN_TEMPERATURE')
        self.boltzmann_floor = parser.getfloat('selection', 'BOLTZMANN_MIN_TEMPERATURE')
        self.boltzmann_factor = parser.getfloat('selection', 'BOLTZMANN_DECREASE_FACTOR')
        self.boltzmann_t = 0
        self.M = parser.getint('selection', 'TOURNAMENT_M')
        self.tournament_threshold = parser.getfloat('selection', 'TOURNAMENT_THRESHOLD')

        self.mutation_method = parser.get('mutation', 'METHOD')
        self.mutation_prob = parser.getfloat('mutation', 'MUTATION_PROB')

        self.stop_decision = parser.get('stop', 'STOP_DECISION')
        self.stop_generations = parser.getint('stop', 'GENERATIONS')
        self.stop_time = parser.getint('stop', 'TIME')
        self.min_fitness = parser.getfloat('stop', 'MIN_FITNESS')
        self.population_portion = parser.getfloat('stop', 'POPULATION_PORTION')
        self.generations_without_change = parser.getint('stop', 'GENERATIONS_WITHOUT_CHANGE')
        self.fitness_percentage_without_change = parser.getfloat('stop', 'FITNESS_PERCENTAGE_WITHOUT_CHANGE')

        self.real_time_graph = parser.getboolean('visualization', 'REAL_TIME_GRAPH')

        self.crossover = parser.get('crossover', 'CROSSOVER_METHOD')
        self.crossover_prob = parser.getfloat('crossover', 'CROSSOVER_PROBABILITY')

    @staticmethod
    def init_config(config_name: str):
        Config.config = Config(config_name)