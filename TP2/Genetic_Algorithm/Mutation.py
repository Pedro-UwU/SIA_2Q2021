import random

from Config import Config
from Genetic_Algorithm.Population import Population


class Mutation:
    method = None

    @staticmethod
    def load_mutation_method():
        if Config.config.mutation_method == 'Uniform Multigen':
            Mutation.method = Mutation.uniform_multigen

    @staticmethod
    def uniform_multigen(pop: Population):
        prob = Config.config.mutation_prob
        for p in pop.pop:
            # Height
            dice = random.uniform(0, 1)
            if dice < prob:
                while True:
                    diff = random.uniform(-0.1, 0.1)
                    if 1.3 <= (p.altura + diff) <= 2.0:
                        p.altura += diff
                        break

            # equipment
            totals = {
                0: Config.config.total_weapons,
                1: Config.config.total_boots,
                2: Config.config.total_helmets,
                3: Config.config.total_gloves,
                4: Config.config.total_chestplates
            }
            for i in range(len(p.equipment)):
                dice = random.uniform(0, 1)
                if dice < prob:
                    new_id = random.randint(0, totals[i])
                    p.equipment[i] = new_id
