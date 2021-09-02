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

    def calc_fitness(self):
        for p in self.pop:
            p.calc_fitness()

    def sort_by_fitness(self):
        self.pop.sort(key=lambda x: -x.fitness)
        return self.pop

    # TODO
    @classmethod
    def generate_random(cls, player_class, size: int, total_weapons: int, total_boots: int, total_helmet: int, total_gloves: int, total_chestplates: int):
        new_pop = Population(size)
        for i in range(size):
            p = Personaje(player_class(), random.uniform(1.3, 2.0), random.randint(0, total_weapons), random.randint(0, total_boots), random.randint(0, total_helmet), random.randint(0, total_gloves), random.randint(0, total_chestplates))
            new_pop.pop.append(p)
        return new_pop