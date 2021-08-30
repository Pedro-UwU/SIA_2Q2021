from dataclasses import dataclass, field

from Genetic_Algorithm.Individual import Individual


@dataclass
class Population:
    pop: list[Individual] = field(default_factory=list, init=False)
    size: int = field()

    def calc_fitness(self):
        for p in self.pop:
            p.calc_fitness()

    def sort_by_fitness(self):
        self.pop.sort(key=lambda x: x.fitness)