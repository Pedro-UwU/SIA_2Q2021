from Genetic_Algorithm.Population import Population


class Genetic:
    @staticmethod
    def genetic_algorithm(pop_size: int):
        init_pop = Population(pop_size)
        