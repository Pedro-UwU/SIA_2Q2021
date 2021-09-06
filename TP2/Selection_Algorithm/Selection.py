import configparser
import math
import os
import random

from dataclasses import dataclass, field
from time import time

from Config import Config
from Genetic_Algorithm.Population import Population
from Selection_Algorithm import Elite, Roulette


@dataclass(frozen=False)
class Selection:
    selection_method_1 = None
    selection_method_2 = None
    selection_method_3 = None
    selection_method_4 = None
    # def fill_all(self, population: Population, kids: Population):
    #     selected_population_method_3 = self.method_3.select_individuals(population, self.constant_B * self.constant_K)
    #     selected_population_method_4 = self.method_4.select_individuals(population,
    #                                                                     (1 - self.constant_B) * self.constant_K)
    #
    #     selected_kids_method_3 = self.method_3.select_individuals(kids, self.constant_B * self.constant_K)
    #     selected_kids_method_4 = self.method_4.select_individuals(kids, (1 - self.constant_B) * self.constant_K)
    #
    #     selected_population = selected_population_method_3 + selected_population_method_4
    #     selected_kids = selected_kids_method_3 + selected_kids_method_4
    #
    #     return selected_population + selected_kids
    #
    # def fill_parent(self, population: Population, kids: Population):
    #     if kids.count() > population.count():
    #         selected_kids_method_3 = self.method_3.select_individuals(kids, self.constant_B * self.constant_K)
    #         selected_kids_method_4 = self.method_4.select_individuals(kids, (1 - self.constant_B) * self.constant_K)
    #         return selected_kids_method_3 + selected_kids_method_4
    #
    #     amount_missing = self.constant_K - kids.count()
    #     selected_population_method_3 = self.method_3.select_individuals(population, amount_missing * self.constant_B)
    #     selected_population_method_4 = self.method_4.select_individuals(population,
    #                                                                     amount_missing * (1 - self.constant_B))
    #     return kids + selected_population_method_3 + selected_population_method_4

    @staticmethod
    def load_selection_methods():
        Selection.selection_method_1 = Selection._methods[Config.config.method1]
        Selection.selection_method_2 = Selection._methods[Config.config.method2]
        Selection.selection_method_3 = Selection._methods[Config.config.method3]
        Selection.selection_method_4 = Selection._methods[Config.config.method4]

    @staticmethod
    def elite(pop: Population, k: int):
        new_pop = Population(k)
        n = pop.size
        for i in range(n):
            total = math.ceil((k - i) / n)
            for j in range(total):
                if len(new_pop.pop) == k:
                    return new_pop
                new_pop.pop.append(pop.pop[i].clone())
        return new_pop

    @staticmethod
    def roulette(pop: Population, k: int):
        total_fitness = pop.total_fitness
        for p in pop.pop:
            p.pseudo_fitness = p.fitness / total_fitness
        acum = 0
        return Selection._aux_roulette(pop, k)

    @staticmethod
    def universal(pop: Population, k: int):
        new_pop = Population(k)
        for i in range(k):
            rnd = random.uniform(0,1)
            r = (rnd + i)/k
            p = Selection._select_from_roullete(pop, r)
            new_pop.pop.append(p)
        return new_pop

    @staticmethod
    def _aux_roulette(pop: Population, k: int):  # Roullete with pseudo-fitness calculed
        new_pop = Population(k)
        for i in range(k):
            rnd = random.uniform(0, 1)
            p = Selection._select_from_roullete(pop, rnd)
            new_pop.pop.append(p)
        return new_pop

    @staticmethod
    def _select_from_roullete(pop: Population, rnd: float):
        orig = rnd
        last_rnd = 0
        while rnd > 0:  # por si tiene que dar mas vueltas
            for p in pop.pop:
                rnd -= p.pseudo_fitness
                if rnd <= 0:
                    return p.clone()
        raise Exception('ERROR in selection')

    @staticmethod
    def ranking(pop: Population, k: int):
        n = len(pop.pop)
        total = 0
        for i in range(len(pop.pop)):
            pop.pop[i].pseudo_fitness = (n - (i + 1))/n
            total += pop.pop[i].pseudo_fitness

        for p in pop.pop:
            p.pseudo_fitness /= total

        return Selection._aux_roulette(pop, k)

    @staticmethod
    def boltzman(pop: Population, k: int):
        T0 = Config.config.boltzmann
        T_c = Config.config.boltzmann_floor
        t = Config.config.boltzmann_t
        _k = Config.config.boltzmann_factor
        T = T_c + (T0 - T_c)*math.exp(-_k*t)
        Config.config.boltzmann_t = t+1
        total = 0
        count = 0
        for p in pop.pop:
            p.pseudo_fitness = math.exp(p.fitness/T)
            total += p.pseudo_fitness
            count += 1

        avg = total/count

        total_f = 0
        for p in pop.pop:
            p.pseudo_fitness /= avg
            total_f += p.pseudo_fitness

        for p in pop.pop:
            p.pseudo_fitness /= total_f

        return Selection._aux_roulette(pop, k)

    @staticmethod
    def tournament_deterministic(pop: Population, k: int):
        M = Config.config.M
        new_pop = Population(k)
        for i in range(k):
            sel = []
            for j in range(M):
                rnd = random.sample(pop.pop, 1)
                sel.append(rnd[0])
            sel.sort(key=lambda x: -x.fitness)
            new_pop.pop.append(sel[0].clone())
        return new_pop

    @staticmethod
    def tournament_probabilistic(pop: Population, k: int):
        thr = Config.config.tournament_threshold
        new_pop = Population(k)
        for i in range(k):
            sample = random.sample(pop.pop, 2)
            sample.sort(key=lambda x: -x.fitness)
            dice = random.uniform(0, 1)
            if dice < thr:
                new_pop.pop.append(sample[0].clone())
            else:
                new_pop.pop.append(sample[1].clone())
        return new_pop
    _methods = {
        'ELITE': elite,
        'ROULETTE': roulette,
        'UNIVERSAL': universal,
        'RANKING': ranking,
        'BOLTZMANN': boltzman,
        'DETERMINISTIC TOURNAMENT': tournament_deterministic,
        'PROBABILISTIC TOURNAMENT': tournament_probabilistic
    }