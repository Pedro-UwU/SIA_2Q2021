import random
from dataclasses import dataclass, field

from DataReader import DataReader
from Genetic_Algorithm.Individual import Individual
from Personaje import Personaje
from clases.Clase import Clase


@dataclass
class Population:
    pop: list[Individual] = field(default_factory=list, init=False)
    size: int = field()

    def calc_fitness(self):
        for p in self.pop:
            p.calc_fitness()

    def sort_by_fitness(self):
        self.pop.sort(key=lambda x: x.fitness)
        return self.pop

    # TODO
    # @classmethod
    # def generate_random(cls, size: int, player_class: Clase, reader: DataReader):
    #     new_pop = Population(size)
    #     for i in range(size):
    #         weapon_id = random.randint(0, 999999)
    #         boot_id = random.randint(0, 999999)
    #         helmet_id = random.randint(0, 999999)
    #         glove_id = random.randint(0, 999999)
    #         chestplate_id = random.randint(0, 999999)
    #
    #         player = Personaje(player_class, random.uniform(1.3, 2.0), reader.get('weapon', weapon_id), )
    #         new_pop.pop.append()