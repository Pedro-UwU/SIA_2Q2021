import time

from Config import Config
from Genetic_Algorithm.Population import Population


class Stop:
    time_method = False
    generations_method = False
    fitness_objective_method = False
    structure_method = False
    content_method = False
    stop_decision = None
    stop_generations = None
    stop_time = None
    min_fitness = None
    population_portion = None
    population_portion_streak = None
    generations_without_change = None
    max_fitness = None
    max_fitness_streak = None
    population_set = None

    @staticmethod
    def initialize_stop():
        if 'Time' in Config.config.stop_decision:
            Stop.time_method = True
        if 'Generations' in Config.config.stop_decision:
            Stop.generations_method = True
        if 'Fitness Objective' in Config.config.stop_decision:
            Stop.fitness_objective_method = True
        if 'Structure' in Config.config.stop_decision:
            Stop.structure_method = True
        if 'Content' in Config.config.stop_decision:
            Stop.content_method = True

        Stop.stop_decision = Config.config.stop_decision
        Stop.stop_generations = Config.config.stop_generations
        Stop.stop_time = Config.config.stop_time
        Stop.min_fitness = Config.config.min_fitness
        Stop.population_portion = Config.config.population_portion
        Stop.generations_without_change = Config.config.generations_without_change
        Stop.population_portion_streak = 0
        Stop.max_fitness_streak = 0
        Stop.max_fitness = 0

    @staticmethod
    def must_continue(generations: int, population: Population, start_time: float):
        # Time
        if Stop.time_method:
            # print("Entramos a ver x Time")
            current_time = time.perf_counter()
            # print(f'Tiempo transcurrido: \n{current_time - start_time}')
            if current_time - start_time >= Stop.stop_time:
                # print('Cortado por Tiempo')
                return False
        # Generations
        if Stop.generations_method:
            # print("Entramos a ver x Generations")
            if Stop.stop_generations <= generations:
                # print('Cortado por Generaciones')
                return False
        # Fitness Objective
        if Stop.fitness_objective_method:
            # print("Entramos a ver x Fitness Objective")
            population.calc_total_fitness()
            total_fitness = population.total_fitness
            if Stop.min_fitness <= total_fitness:
                # print('Cortado por Min Fitness')
                return False
        # Structure
        if Stop.structure_method:
            # print("Entramos a ver x Structure")
            if Stop.population_portion_streak >= Stop.generations_without_change:
                # print('Cortado por Structure')
                return False
            if Stop.population_set is None:
                Stop.init_population_set(population)
            else:
                repeated_portion = Stop.calculate_repeated_portion(population)
                if repeated_portion >= Stop.population_portion:
                    # print("Poblacion repetida")
                    Stop.population_portion_streak += 1
                else:
                    # print("No se repite la poblacion")
                    Stop.init_population_set(population)
                    Stop.population_portion_streak = 0
        # Content
        if Stop.content_method:
            # print("Entramos a ver x Content")

            if Stop.max_fitness_streak >= Stop.generations_without_change:
                # print('Cortado por Content')
                return False

            population.calc_total_fitness()
            if Stop.max_fitness == population.total_fitness:
                Stop.max_fitness_streak += 1

            if population.total_fitness > Stop.max_fitness:
                Stop.max_fitness = population.total_fitness
                Stop.max_fitness_streak = 0

            if population.total_fitness < Stop.max_fitness:
                Stop.max_fitness_streak = 0
        return True

    @staticmethod
    def init_population_set(population: Population):
        # print('Inicializando el Set')

        Stop.population_set = set()
        for p in population.pop:
            Stop.population_set.add(p)

    @staticmethod
    def calculate_repeated_portion(population: Population):
        repeated = 0
        for p in population.pop:
            if p in Stop.population_set:
                repeated += 1

        return repeated / population.size
