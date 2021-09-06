import random
from dataclasses import dataclass, field

from DataReader import DataReader
from Personaje import Personaje
from clases.Arquero import Arquero
from clases.Clase import Clase
from clases.Defensor import Defensor
from clases.Guerrero import Guerrero
from clases.Infiltrado import Infiltrado


@dataclass
class Population:
    pop: list[Personaje] = field(default_factory=list, init=False)
    size: int = field()
    total_fitness = 0

    def calc_fitness(self):
        for p in self.pop:
            f = p.calc_fitness()
            self.total_fitness += f

    def sort_by_fitness(self):
        self.pop.sort(key=lambda x: -x.fitness)
        return self.pop

    def get_first_fitness(self):
        return self.pop[0].fitness

    def get_last_fitness(self):
        return self.pop[-1].fitness

    def get_avg_fitness(self):
        total = 0
        count = 0
        for p in self.pop:
            total += p.fitness
            count += 1
        return total/count

    def calc_total_fitness(self):
        self.total_fitness = 0
        for p in self.pop:
            self.total_fitness += p.fitness

    @classmethod
    def generate_random(cls, player_class, size: int, total_weapons: int, total_boots: int, total_helmet: int, total_gloves: int, total_chestplates: int):
        new_pop = Population(size)
        for i in range(size):
            p = Personaje(player_class(), random.uniform(1.3, 2.0), random.randint(0, total_weapons), random.randint(0, total_boots), random.randint(0, total_helmet), random.randint(0, total_gloves), random.randint(0, total_chestplates))
            new_pop.pop.append(p)
        return new_pop

    @classmethod
    def union(cls, pop1, pop2):
        new_pop = Population(len(pop1.pop) + len(pop2.pop))
        for p in pop1.pop:
            new_pop.pop.append(p)
        for p in pop2.pop:
            new_pop.pop.append(p)
        new_pop.calc_total_fitness()
        return new_pop

    def __str__(self):
        s = ""
        for p in self.pop:
            s += f'{p}\n'
        return s
