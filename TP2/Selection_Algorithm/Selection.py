import configparser
import math
import os

from dataclasses import dataclass, field

from Config import Config
from Genetic_Algorithm.Population import Population
from Selection_Algorithm import Elite, Roulette


@dataclass(frozen=False)
class Selection:
    constant_A: float = field()
    constant_B: float = field()
    constant_K: int = field()
    selection_method_1 = None
    selection_method_2 = None
    selection_method_3 = None
    selection_method_4 = None

    def __init__(self):
        dirname = os.path.dirname(__file__)
        configPath = os.path.join(dirname, 'config.conf')
        parser = configparser.ConfigParser()
        parser.read(configPath)

        method_1 = parser.get('config', 'METHOD_1')
        method_2 = parser.get('config', 'METHOD_2')
        method_3 = parser.get('config', 'METHOD_3')
        method_4 = parser.get('config', 'METHOD_4')

        if method_1 == 'Elite':
            self.method_1 = Elite
        else:
            self.method_1 = Roulette

        if method_2 == 'Elite':
            self.method_2 = Elite
        else:
            self.method_2 = Roulette

        if method_3 == 'Elite':
            self.method_3 = Elite
        else:
            self.method_3 = Roulette

        if method_4 == 'Elite':
            self.method_4 = Elite
        else:
            self.method_4 = Roulette

    def fill_all(self, population: Population, kids: Population):
        selected_population_method_3 = self.method_3.select_individuals(population, self.constant_B * self.constant_K)
        selected_population_method_4 = self.method_4.select_individuals(population,
                                                                        (1 - self.constant_B) * self.constant_K)

        selected_kids_method_3 = self.method_3.select_individuals(kids, self.constant_B * self.constant_K)
        selected_kids_method_4 = self.method_4.select_individuals(kids, (1 - self.constant_B) * self.constant_K)

        selected_population = selected_population_method_3 + selected_population_method_4
        selected_kids = selected_kids_method_3 + selected_kids_method_4

        return selected_population + selected_kids

    def fill_parent(self, population: Population, kids: Population):
        if kids.count() > population.count():
            selected_kids_method_3 = self.method_3.select_individuals(kids, self.constant_B * self.constant_K)
            selected_kids_method_4 = self.method_4.select_individuals(kids, (1 - self.constant_B) * self.constant_K)
            return selected_kids_method_3 + selected_kids_method_4

        amount_missing = self.constant_K - kids.count()
        selected_population_method_3 = self.method_3.select_individuals(population, amount_missing * self.constant_B)
        selected_population_method_4 = self.method_4.select_individuals(population,
                                                                        amount_missing * (1 - self.constant_B))
        return kids + selected_population_method_3 + selected_population_method_4

    @staticmethod
    def load_selection_methods():
        #method1
        if Config.config.method1 == 'ELITE':
            Selection.selection_method_1 = Selection.elite

        if Config.config.method2 == 'ELITE':
            Selection.selection_method_2 = Selection.elite

        if Config.config.method3 == 'ELITE':
            Selection.selection_method_3 = Selection.elite

        if Config.config.method3 == 'ELITE':
            Selection.selection_method_4 = Selection.elite

    @staticmethod
    def elite(pop: Population, k: int):
        new_pop = Population(k)
        n = pop.size
        for i in range(n):
            total = math.ceil((k - i) / n)
            for j in range(total):
                if len(new_pop.pop) == k:
                    return new_pop
                new_pop.pop.append(pop.pop[i])
        return new_pop