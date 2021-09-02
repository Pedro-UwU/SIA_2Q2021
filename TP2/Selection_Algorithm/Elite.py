from Genetic_Algorithm.Population import Population
from Personaje import Personaje


class Elite:
    @staticmethod
    def select_individuals(population: Population, amount: int):
        if amount < population.pop.count():
            return population.sort_by_fitness()[amount:]

        selected: list[Personaje]
        missing = amount - selected.count()
        while missing > 0:
            if missing >= population.pop.count():
                selected = selected + population.pop
            else:
                selected = selected + population.sort_by_fitness()[missing:]

        return selected
