import random

from Genetic_Algorithm import Genetic
from Genetic_Algorithm.Population import Population
from Personaje import Personaje


class Crossover:
    @staticmethod
    def pointCross(parents: Population):
        pop = random.sample(parents.pop, parents.size)
        new_pop = Population(parents.size)
        # Si la poblacion es impar, le agrega el primero de nuevo
        if len(pop) % 2 == 1:
            pop.append(pop[0])

        for i in range(0, len(pop), 2):
            locus = random.randint(0, Genetic.GENOTYPE_LENGTH)
            parent1 = pop[i]
            parent2 = pop[i + 1]
            child1_genes = []
            child2_genes = []
            for x in range(locus):
                if x == 0:
                    child1_genes.append(parent1.altura)
                    child2_genes.append(parent2.altura)
                else:
                    child1_genes.append(parent1.equipment[x - 1])
                    child2_genes.append(parent2.equipment[x - 1])
            for x in range(locus, Genetic.GENOTYPE_LENGTH):
                if x == 0:
                    child1_genes.append(parent2.altura)
                    child2_genes.append(parent1.altura)
                else:
                    child1_genes.append(parent2.equipment[x - 1])
                    child2_genes.append(parent1.equipment[x - 1])

            child1 = Personaje(parent1.clase, child1_genes[0], child1_genes[1], child1_genes[2], child1_genes[3],
                               child1_genes[4], child1_genes[5])
            child2 = Personaje(parent2.clase, child2_genes[0], child2_genes[1], child2_genes[2], child2_genes[3],
                               child2_genes[4], child2_genes[5])
            new_pop.pop.append(child1)
            new_pop.pop.append(child2)

        return new_pop
