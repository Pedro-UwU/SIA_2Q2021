import time

from Config import Config
from Genetic_Algorithm.Crossover import Crossover
from Genetic_Algorithm.Mutation import Mutation
from Selection_Algorithm.Selection import *
from clases.Arquero import Arquero
from clases.Defensor import Defensor
from clases.Guerrero import Guerrero
from clases.Infiltrado import Infiltrado
import matplotlib.pyplot as plt

GENOTYPE_LENGTH = 6


class Genetic:
    _classNames = {
        'Archer': Arquero,
        'Defender': Defensor,
        'Warrior': Guerrero,
        'Spy': Infiltrado
    }

    @staticmethod
    def genetic_algorithm(player_class):
        pop_size = Config.config.N
        cross_size = Config.config.K
        total_gloves = Config.config.total_gloves
        total_weapons = Config.config.total_weapons
        total_boots = Config.config.total_boots
        total_helmets = Config.config.total_helmets
        total_chestplates = Config.config.total_chestplates
        Selection.load_selection_methods()
        Mutation.load_mutation_method()

        gen_record = []
        max_fitness_record = []
        min_fitness_record = []
        avg_fitness_record = []

        init_pop = Population.generate_random(Genetic._classNames[player_class], pop_size, total_weapons, total_boots,
                                              total_helmets, total_gloves, total_chestplates)
        current_pop = init_pop
        current_pop.calc_fitness()
        current_pop.sort_by_fitness()
        gen = 0
        gen_record.append(gen)
        max_fitness_record.append(current_pop.get_first_fitness())
        min_fitness_record.append(current_pop.get_last_fitness())
        avg_fitness_record.append(current_pop.get_avg_fitness())
        plt.plot(gen_record, max_fitness_record)


        A = int(Config.config.A * cross_size)
        B = int(Config.config.B * pop_size)
        # print(f'Init Gen: \n{init_pop}')
        while gen < 500:
            fathers1 = Selection.selection_method_1(current_pop, A)
            fathers2 = Selection.selection_method_2(current_pop, cross_size - A)
            # print(f'FATHERS 1: \n{fathers1}')
            # print(f'FATHERS 2: \n{fathers2}')

            cross1 = Crossover.pointCross(fathers1)
            cross2 = Crossover.pointCross(fathers2)
            cross1.calc_fitness()
            cross2.calc_fitness()
            cross = Population.union(cross1, cross2)
            # print(f'Cross: \n{cross}')
            if Config.config.genetic_implementation == 'Fill All':
                union = Population.union(cross, current_pop)
                Mutation.method(union)
                union.sort_by_fitness()
                # print(f'Union: \n{union}')

                new_pop1 = Selection.selection_method_3(union, B)
                new_pop2 = Selection.selection_method_4(union, pop_size - B)
                new_pop = Population.union(new_pop1, new_pop2)
                new_pop.sort_by_fitness()
                current_pop = new_pop
                # print(f'New Gen: \n{current_pop}')

            if Config.config.genetic_implementation == 'Fill Parent':
                if len(cross.pop) > len(current_pop.pop):
                    new_pop1 = Selection.selection_method_3(cross, B)
                    new_pop2 = Selection.selection_method_4(cross, pop_size - B)
                    new_pop = Population.union(new_pop1, new_pop2)
                    new_pop.sort_by_fitness()
                    current_pop = new_pop
                else:
                    amount_missing = int(Config.config.K) - len(cross.pop)
                    B = int(Config.config.B * amount_missing)
                    new_pop1 = Selection.selection_method_3(current_pop, B)
                    new_pop2 = Selection.selection_method_4(current_pop, amount_missing - B)
                    new_pop = Population.union(new_pop1, new_pop2)
                    final_new_pop = Population.union(new_pop, cross)
                    final_new_pop.sort_by_fitness()
                    current_pop = final_new_pop

            gen += 1

            gen_record.append(gen)
            max_fitness_record.append(current_pop.get_first_fitness())
            min_fitness_record.append(current_pop.get_last_fitness())
            avg_fitness_record.append(current_pop.get_avg_fitness())
            plt.plot(gen_record, max_fitness_record, 'b', gen_record, min_fitness_record, 'r', gen_record, avg_fitness_record, 'g')
            plt.pause(0.000000001)

            print(f'Generation: {gen}, Max Fitness: {current_pop.get_first_fitness()}')
