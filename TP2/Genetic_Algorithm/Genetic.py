from Genetic_Algorithm.Population import Population


class Genetic:
    @staticmethod
    def genetic_algorithm(pop_size: int, total_weapons: int, total_boots: int, total_helmets: int, total_gloves: int, total_chestplates: int):
        init_pop = Population.generate_random(pop_size, total_weapons, total_boots, total_helmets, total_gloves, total_chestplates)
        init_pop.calc_fitness()
        init_pop.sort_by_fitness()
        for p in init_pop.pop:
            print(p)