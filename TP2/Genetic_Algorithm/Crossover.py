import random

from Genetic_Algorithm import Genetic
from Genetic_Algorithm.Population import Population
from Personaje import Personaje


class Crossover:
    @staticmethod
    def pointCross(parents: Population):
        pop = random.sample(parents.pop, parents.size)
        new_pop = Population(parents.size)
        odd = False
        # Si la poblacion es impar, le agrega el primero de nuevo
        if len(pop) % 2 == 1:
            pop.append(pop[0])
            odd = True

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

        if odd:
            new_pop.pop.pop(len(new_pop.pop)-1)
        return new_pop

    @staticmethod
    def doubleCross(parents: Population):
        pop = random.sample(parents.pop, parents.size)
        new_pop = Population(parents.size)
        # Si la poblacion es impar, le agrega el primero de nuevo
        if len(pop) % 2 == 1:
            pop.append(pop[0])

        for i in range(0, len(pop), 2):
            locus1 = random.randint(0, Genetic.GENOTYPE_LENGTH - 1)
            locus2 = random.randint(0, Genetic.GENOTYPE_LENGTH)
            while locus2 <= locus1:
                locus2 = random.randint(locus1, Genetic.GENOTYPE_LENGTH)

            parent1 = pop[i]
            parent2 = pop[i + 1]
            child1_genes = []
            child2_genes = []
            if locus1 != 0:
                for x in range(0, locus1):
                    if x == 0:
                        child1_genes.append(parent1.altura)
                        child2_genes.append(parent2.altura)
                    else:
                        child1_genes.append(parent1.equipment[x - 1])
                        child2_genes.append(parent2.equipment[x - 1])

            for x in range(locus1, locus2):
                if x == 0:
                    child1_genes.append(parent2.altura)
                    child2_genes.append(parent1.altura)
                else:
                    child1_genes.append(parent2.equipment[x - 1])
                    child2_genes.append(parent1.equipment[x - 1])

            for x in range(locus2, Genetic.GENOTYPE_LENGTH):
                child1_genes.append(parent1.equipment[x - 1])
                child2_genes.append(parent2.equipment[x - 1])

            child1 = Personaje(parent1.clase, child1_genes[0], child1_genes[1], child1_genes[2], child1_genes[3],
                               child1_genes[4], child1_genes[5])
            child2 = Personaje(parent2.clase, child2_genes[0], child2_genes[1], child2_genes[2], child2_genes[3],
                               child2_genes[4], child2_genes[5])
            new_pop.pop.append(child1)
            new_pop.pop.append(child2)

        return new_pop

    @staticmethod
    def anularCross(parents: Population):
        pop = random.sample(parents.pop, parents.size)
        new_pop = Population(parents.size)
        # Si la poblacion es impar, le agrega el primero de nuevo
        if len(pop) % 2 == 1:
            pop.append(pop[0])

        for i in range(0, len(pop), 2):
            locus = random.randint(0, Genetic.GENOTYPE_LENGTH - 1)
            length = random.randint(0, Genetic.GENOTYPE_LENGTH / 2)
            parent1 = pop[i]
            parent2 = pop[i + 1]
            child1_genes = []
            child2_genes = []

            if length == 0:
                for x in range(0, Genetic.GENOTYPE_LENGTH):
                    if x == 0:
                        child1_genes.append(parent1.altura)
                        child2_genes.append(parent2.altura)
                    else:
                        child1_genes.append(parent1.equipment[x - 1])
                        child2_genes.append(parent2.equipment[x - 1])
            elif locus == 5:
                for x in range(length - 1):
                    if x == 0:
                        child1_genes.append(parent2.altura)
                        child2_genes.append(parent1.altura)
                    else:
                        child1_genes.append(parent2.equipment[x - 1])
                        child2_genes.append(parent1.equipment[x - 1])
                for x in range(length - 1, locus):
                    if x == 0:
                        child1_genes.append(parent1.altura)
                        child2_genes.append(parent2.altura)
                    else:
                        child1_genes.append(parent1.equipment[x - 1])
                        child2_genes.append(parent2.equipment[x - 1])
                child1_genes.append(parent2.equipment[locus - 1])
                child2_genes.append(parent1.equipment[locus - 1])
            elif locus + length > Genetic.GENOTYPE_LENGTH:
                extra = locus + length - Genetic.GENOTYPE_LENGTH
                for x in range(extra):
                    if x == 0:
                        child1_genes.append(parent2.altura)
                        child2_genes.append(parent1.altura)
                    else:
                        child1_genes.append(parent2.equipment[x - 1])
                        child2_genes.append(parent1.equipment[x - 1])
                for x in range(extra, locus):
                    if x == 0:
                        child1_genes.append(parent1.altura)
                        child2_genes.append(parent2.altura)
                    else:
                        child1_genes.append(parent1.equipment[x - 1])
                        child2_genes.append(parent2.equipment[x - 1])
                for x in range(locus, Genetic.GENOTYPE_LENGTH):
                    child1_genes.append(parent2.equipment[x - 1])
                    child2_genes.append(parent1.equipment[x - 1])
            else:
                if locus != 0:
                    for x in range(0, locus):
                        if x == 0:
                            child1_genes.append(parent1.altura)
                            child2_genes.append(parent2.altura)
                        else:
                            child1_genes.append(parent1.equipment[x - 1])
                            child2_genes.append(parent2.equipment[x - 1])

                for x in range(locus, locus + length):
                    if x == 0:
                        child1_genes.append(parent2.altura)
                        child2_genes.append(parent1.altura)
                    else:
                        child1_genes.append(parent2.equipment[x - 1])
                        child2_genes.append(parent1.equipment[x - 1])

                for x in range(locus + length, Genetic.GENOTYPE_LENGTH):
                    child1_genes.append(parent1.equipment[x - 1])
                    child2_genes.append(parent2.equipment[x - 1])

            print(f'locus: {locus}, length: {length}')
            print(f'child1_genes: {child1_genes}')
            print(f'child2_genes: {child2_genes}')

            child1 = Personaje(parent1.clase, child1_genes[0], child1_genes[1], child1_genes[2], child1_genes[3],
                               child1_genes[4], child1_genes[5])
            child2 = Personaje(parent2.clase, child2_genes[0], child2_genes[1], child2_genes[2], child2_genes[3],
                               child2_genes[4], child2_genes[5])
            new_pop.pop.append(child1)
            new_pop.pop.append(child2)

        return new_pop

    @staticmethod
    def uniformCross(parents: Population):
        pop = random.sample(parents.pop, parents.size)
        new_pop = Population(parents.size)
        # Si la poblacion es impar, le agrega el primero de nuevo
        if len(pop) % 2 == 1:
            pop.append(pop[0])

        for i in range(0, len(pop), 2):
            parent1 = pop[i]
            parent2 = pop[i + 1]
            child1_genes = []
            child2_genes = []
            for x in range(0, Genetic.GENOTYPE_LENGTH):
                dice = random.uniform(0, 1)
                swap = dice > 0.5
                if x == 0:
                    if swap:
                        child1_genes.append(parent2.altura)
                        child2_genes.append(parent1.altura)
                    else:
                        child1_genes.append(parent1.altura)
                        child2_genes.append(parent2.altura)
                else:
                    if swap:
                        child1_genes.append(parent2.equipment[x - 1])
                        child2_genes.append(parent1.equipment[x - 1])
                    else:
                        child1_genes.append(parent1.equipment[x - 1])
                        child2_genes.append(parent2.equipment[x - 1])

            child1 = Personaje(parent1.clase, child1_genes[0], child1_genes[1], child1_genes[2], child1_genes[3],
                               child1_genes[4], child1_genes[5])
            child2 = Personaje(parent2.clase, child2_genes[0], child2_genes[1], child2_genes[2], child2_genes[3],
                               child2_genes[4], child2_genes[5])
            new_pop.pop.append(child1)
            new_pop.pop.append(child2)

        return new_pop

