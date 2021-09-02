from Genetic_Algorithm.Crossover import Crossover
from Genetic_Algorithm.Population import Population
from Selection_Algorithm.Selection import *
from clases.Arquero import Arquero
from clases.Clase import Clase
from clases.Defensor import Defensor
from clases.Guerrero import Guerrero
from clases.Infiltrado import Infiltrado

GENOTYPE_LENGTH = 6


class Genetic:
    _classNames = {
        'Archer': Arquero,
        'Defender': Defensor,
        'Warrior': Guerrero,
        'Spy': Infiltrado
    }

    @staticmethod
    def genetic_algorithm(player_class, pop_size: int, total_weapons: int, total_boots: int, total_helmets: int,
                          total_gloves: int, total_chestplates: int):
        init_pop = Population.generate_random(Genetic._classNames[player_class], pop_size, total_weapons, total_boots,
                                              total_helmets, total_gloves, total_chestplates)
        init_pop.calc_fitness()
        init_pop.sort_by_fitness()
        fathers = Selection.elite(init_pop, 6)
        for p in fathers.pop:
            print(p)
        cross = Crossover.pointCross(fathers)
        cross.calc_fitness()
        cross.sort_by_fitness()
        print('\n#################\n\n')
        for p in cross.pop:
            print(p)

