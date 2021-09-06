import random
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
    generations_without_change = None
    fitness_percentage_without_change = None
    max_fitness = None
    max_fitness_streak = None

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
        Stop.fitness_percentage_without_change = Config.config.fitness_percentage_without_change
        Stop.max_fitness_streak = 0
        Stop.max_fitness = 0

    @staticmethod
    def must_continue(generations: int, population: Population, start_time: float):
        # Time
        if Stop.time_method:
            print("Entramos a ver x Time")
            current_time = time.perf_counter()
            print(f'Tiempo transcurrido: \n{current_time - start_time}')
            if current_time - start_time >= Stop.stop_time:
                print('Cortado por Tiempo')
                return False
        # Generations
        if Stop.generations_method:
            print("Entramos a ver x Generations")
            if Stop.stop_generations <= generations:
                print('Cortado por Generaciones')
                return False
        # Fitness Objective
        if Stop.fitness_objective_method:
            print("Entramos a ver x Fitness Objective")
            population.calc_total_fitness()
            total_fitness = population.total_fitness
            if Stop.min_fitness <= total_fitness:
                print('Cortado por Min Fitness')
                return False
        # Structure
        if Stop.structure_method:
            print("Entramos a ver x Structure")
            pass
        # Content
        if Stop.content_method:
            print("Entramos a ver x Content")
            population.calc_total_fitness()

            current_total_fitness = population.total_fitness
            fitness_diff = abs(current_total_fitness - Stop.max_fitness)
            streak = False
            if fitness_diff <= Stop.max_fitness * Stop.fitness_percentage_without_change:
                print(f'Max Fitness: {Stop.max_fitness}, FitnessDiff: {fitness_diff}, generations: {generations}')
                Stop.max_fitness_streak += 1
                streak = True

            if Stop.max_fitness_streak >= Stop.generations_without_change:
                print('Cortado por Content')
                return False

            if current_total_fitness > Stop.max_fitness:
                Stop.max_fitness = current_total_fitness
                if not streak:
                    Stop.max_fitness_streak = 0

        return True
