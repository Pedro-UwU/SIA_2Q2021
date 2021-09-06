import random

from Config import Config
from Genetic_Algorithm.Population import Population


class Mutation:
    method = None

    @staticmethod
    def load_mutation_method():
        if Config.config.mutation_method == 'Uniform Multigen':
            Mutation.method = Mutation.uniform_multigen
        if Config.config.mutation_method == 'Limited Multigen':
            Mutation.method = Mutation.limited_multigen
        if Config.config.mutation_method == 'Single Gen Mutation':
            Mutation.method = Mutation.single_gen_mutation
        if Config.config.mutation_method == 'Complete Mutation':
            Mutation.method = Mutation.complete_mutation

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

    @staticmethod
    def limited_multigen(pop: Population):
        prob = Config.config.mutation_prob
        for p in pop.pop:
            dice = random.uniform(0, 1)
            if dice < prob:
                m = random.randint(1, 5)
                genes = random.sample(range(1, 6), m)
                totals = {
                    0: Config.config.total_weapons,
                    1: Config.config.total_boots,
                    2: Config.config.total_helmets,
                    3: Config.config.total_gloves,
                    4: Config.config.total_chestplates
                }

                for gen in genes:
                    # Height
                    if gen == 5:
                        while True:
                            diff = random.uniform(-0.1, 0.1)
                            if 1.3 <= (p.altura + diff) <= 2.0:
                                p.altura += diff
                                break
                    # Equipment
                    else:
                        new_id = random.randint(0, totals[gen])
                        p.equipment[gen] = new_id

    @staticmethod
    def single_gen_mutation(pop: Population):
        prob = Config.config.mutation_prob
        for p in pop.pop:
            dice = random.uniform(0, 1)
            if dice < prob:
                totals = {
                    0: Config.config.total_weapons,
                    1: Config.config.total_boots,
                    2: Config.config.total_helmets,
                    3: Config.config.total_gloves,
                    4: Config.config.total_chestplates
                }
                gen = random.randint(0, 5)

                # Height
                if gen == 5:
                    while True:
                        diff = random.uniform(-0.1, 0.1)
                        if 1.3 <= (p.altura + diff) <= 2.0:
                            p.altura += diff
                            break
                # Equipment
                else:
                    new_id = random.randint(0, totals[gen])
                    p.equipment[gen] = new_id


    @staticmethod
    def complete_mutation(pop: Population):
        prob = Config.config.mutation_prob
        for p in pop.pop:
            dice = random.uniform(0, 1)
            if dice < prob:
                # Height
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
                    new_id = random.randint(0, totals[i])
                    p.equipment[i] = new_id