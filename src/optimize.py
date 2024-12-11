import util
from const import *
from sim import Simulation
from state import State
from draw import Draw

# lib
from scipy.spatial.distance import cdist
from scipy.stats import truncnorm
import multiprocessing
import numpy as np
import random
import pygad

from mcts.searcher.mcts import MCTS

GENE_SPACE = [
    {'low': P1_BOUNDS[0][0], 'high': P1_BOUNDS[1][0]},
    {'low': P1_BOUNDS[0][1], 'high': P1_BOUNDS[1][1]},
    {'low': P1_BOUNDS[0][0], 'high': P1_BOUNDS[1][0]},
    {'low': P1_BOUNDS[0][1], 'high': P1_BOUNDS[1][1]},
    {'low': P1_BOUNDS[0][0], 'high': P1_BOUNDS[1][0]},
    {'low': P1_BOUNDS[0][1], 'high': P1_BOUNDS[1][1]},
    {'low': P1_BOUNDS[0][0], 'high': P1_BOUNDS[1][0]},
    {'low': P1_BOUNDS[0][1], 'high': P1_BOUNDS[1][1]},
    {'low': P1_BOUNDS[0][0], 'high': P1_BOUNDS[1][0]},
    {'low': P1_BOUNDS[0][1], 'high': P1_BOUNDS[1][1]},
    {'low': P1_BOUNDS[0][0], 'high': P1_BOUNDS[1][0]},
    {'low': P1_BOUNDS[0][1], 'high': P1_BOUNDS[1][1]},
    {'low': P1_BOUNDS[0][0], 'high': P1_BOUNDS[1][0]},
    {'low': P1_BOUNDS[0][1], 'high': P1_BOUNDS[1][1]}
]

class Optimize():

    @staticmethod
    def unpack_positions(solution):
        return [(solution[i], solution[i+1]) for i in range(0, len(solution), 2)]

    @staticmethod
    def get_intersect_count(positions):
        distance_matrix = cdist(positions, positions)
        intersect_matrix = distance_matrix <= (BALL_RADIUS*2)
        np.fill_diagonal(intersect_matrix, False)
        return np.count_nonzero(intersect_matrix)

    @staticmethod
    def get_naive_fitness(solution, opponent_samples):
        positions = Optimize.unpack_positions(solution)
        intersect_count = Optimize.get_intersect_count(positions)

        total_actions = 0
        total_score = 0

        for _ in range(opponent_samples):
            sim_init_state = {
                'p1' : {'sunk': 'init', 'pos': util.random_pos(True)},
                'p2' : {'sunk': None, 'pos': util.random_pos(False)},
                '1' : {'sunk': None, 'pos': positions[0]},
                '2' : {'sunk': None, 'pos': positions[1]},
                '3' : {'sunk': None, 'pos': positions[2]},
                '4' : {'sunk': None, 'pos': positions[3]},
                '5' : {'sunk': None, 'pos': positions[4]},
                '6' : {'sunk': None, 'pos': positions[5]},
                '7' : {'sunk': None, 'pos': positions[6]},
                '9' : {'sunk': None, 'pos': util.random_pos(False)},
                '10' : {'sunk': None, 'pos': util.random_pos(False)},
                '11' : {'sunk': None, 'pos': util.random_pos(False)},
                '12' : {'sunk': None, 'pos': util.random_pos(False)},
                '13' : {'sunk': None, 'pos': util.random_pos(False)},
                '14' : {'sunk': None, 'pos': util.random_pos(False)},
                '15' : {'sunk': None, 'pos': util.random_pos(False)}
            }
            my_sim = Simulation(draw=-1)
            actions = my_sim.actions(sim_init_state, -1)
            total_actions += len(actions)
            for dir, origin, power in actions:
                end_state = my_sim.move(sim_init_state, -1, dir, origin, power)
                total_score += util.eval(end_state)

        averge_score = total_score / total_actions
        fitness = averge_score - intersect_count

        print('fitness:', fitness)

        return fitness

    @staticmethod
    def naive_fitness_func(ga_instance, solution, solution_idx):
        opponent_samples = 4

        fitness = Optimize.get_naive_fitness(solution, opponent_samples)

        return fitness


    @staticmethod
    def get_informed_fitness(solution, opponent_samples, iteration_limit):
        positions = Optimize.unpack_positions(solution)
        intersect_count = Optimize.get_intersect_count(positions)

        total_score = 0

        for _ in range(opponent_samples):
            sim_init_state = {
                'p1' : {'sunk': 'init', 'pos': util.random_pos(True)},
                'p2' : {'sunk': None, 'pos': util.random_pos(False)},
                '1' : {'sunk': None, 'pos': positions[0]},
                '2' : {'sunk': None, 'pos': positions[1]},
                '3' : {'sunk': None, 'pos': positions[2]},
                '4' : {'sunk': None, 'pos': positions[3]},
                '5' : {'sunk': None, 'pos': positions[4]},
                '6' : {'sunk': None, 'pos': positions[5]},
                '7' : {'sunk': None, 'pos': positions[6]},
                '9' : {'sunk': None, 'pos': util.random_pos(False)},
                '10' : {'sunk': None, 'pos': util.random_pos(False)},
                '11' : {'sunk': None, 'pos': util.random_pos(False)},
                '12' : {'sunk': None, 'pos': util.random_pos(False)},
                '13' : {'sunk': None, 'pos': util.random_pos(False)},
                '14' : {'sunk': None, 'pos': util.random_pos(False)},
                '15' : {'sunk': None, 'pos': util.random_pos(False)}
            }
            
            my_sim = Simulation(draw=-1)

            mcts_init_state = State(sim_init_state, my_sim)
            searcher = MCTS(iteration_limit=iteration_limit)
            searcher.search(initial_state=mcts_init_state)

            total_score += searcher.root.totalReward

        averge_score = total_score / (opponent_samples * iteration_limit)
        fitness = averge_score - intersect_count

        print('fitness:', fitness)

        return fitness

    @staticmethod
    def informed_fitness_func(ga_instance, solution, solution_idx):
        opponent_samples = 4
        iteration_limit = 20

        fitness = Optimize.get_informed_fitness(solution, opponent_samples, iteration_limit)

        return fitness

    @staticmethod
    def mutation_func(offspring, ga_instance):
        for sol_idx in range(offspring.shape[0]):
            for gene_idx in range(offspring.shape[1]):
                if random.random() > 1 / offspring.shape[1]:
                    continue

                mean = offspring[sol_idx][gene_idx]
                std_dev = 32*np.exp(-0.25*ga_instance.generations_completed) + 1
                lower_bound = ga_instance.gene_space[gene_idx]['low']
                upper_bound = ga_instance.gene_space[gene_idx]['high']

                dist = truncnorm((lower_bound - mean) / std_dev, (upper_bound - mean) / std_dev, loc=mean, scale=std_dev)
                sample = dist.rvs()

                # print(std_dev, 'MUTATION!', sol_idx, gene_idx, offspring[sol_idx][gene_idx], sample)

                offspring[sol_idx][gene_idx] = sample

        return offspring
    
    @staticmethod
    def adaptive_mutation_func(offspring, ga_instance):
        average_fitness, offspring_fitness = ga_instance.adaptive_mutation_population_fitness(offspring)

        for sol_idx in range(offspring.shape[0]):
            for gene_idx in range(offspring.shape[1]):

                if offspring_fitness[sol_idx] < average_fitness:
                    mutation_prob = 0.25
                else:
                    mutation_prob = 1 / offspring.shape[1]

                if random.random() > mutation_prob:
                    continue

                mean = offspring[sol_idx][gene_idx]
                std_dev = 32*np.exp(-0.25*ga_instance.generations_completed) + 1
                lower_bound = ga_instance.gene_space[gene_idx]['low']
                upper_bound = ga_instance.gene_space[gene_idx]['high']

                dist = truncnorm((lower_bound - mean) / std_dev, (upper_bound - mean) / std_dev, loc=mean, scale=std_dev)
                sample = dist.rvs()

                # print(std_dev, 'MUTATION!', sol_idx, gene_idx, offspring[sol_idx][gene_idx], sample)

                offspring[sol_idx][gene_idx] = sample

        return offspring

    @staticmethod
    def draw_solution(solution):
        positions = Optimize.unpack_positions(solution)
        sim_init_state = {
            'p1' : {'sunk': 'init', 'pos': (0,0)},
            'p2' : {'sunk': 'init', 'pos': (0,0)},
            '1' : {'sunk': None, 'pos': positions[0]},
            '2' : {'sunk': None, 'pos': positions[1]},
            '3' : {'sunk': None, 'pos': positions[2]},
            '4' : {'sunk': None, 'pos': positions[3]},
            '5' : {'sunk': None, 'pos': positions[4]},
            '6' : {'sunk': None, 'pos': positions[5]},
            '7' : {'sunk': None, 'pos': positions[6]},
            '9' : {'sunk': 'init', 'pos': (0,0)},
            '10' : {'sunk': 'init', 'pos': (0,0)},
            '11' : {'sunk': 'init', 'pos': (0,0)},
            '12' : {'sunk': 'init', 'pos': (0,0)},
            '13' : {'sunk': 'init', 'pos': (0,0)},
            '14' : {'sunk': 'init', 'pos': (0,0)},
            '15' : {'sunk': 'init', 'pos': (0,0)}
        }

        my_sim = Simulation(draw=0)
        my_sim.set_state(sim_init_state)

        while True:
            my_sim.draw.draw_frame(my_sim.geometry)
    
    @staticmethod
    def save_image_of_solution(solution, filename):
        positions = Optimize.unpack_positions(solution)
        sim_init_state = {
            'p1' : {'sunk': 'init', 'pos': (0,0)},
            'p2' : {'sunk': 'init', 'pos': (0,0)},
            '1' : {'sunk': None, 'pos': positions[0]},
            '2' : {'sunk': None, 'pos': positions[1]},
            '3' : {'sunk': None, 'pos': positions[2]},
            '4' : {'sunk': None, 'pos': positions[3]},
            '5' : {'sunk': None, 'pos': positions[4]},
            '6' : {'sunk': None, 'pos': positions[5]},
            '7' : {'sunk': None, 'pos': positions[6]},
            '9' : {'sunk': 'init', 'pos': (0,0)},
            '10' : {'sunk': 'init', 'pos': (0,0)},
            '11' : {'sunk': 'init', 'pos': (0,0)},
            '12' : {'sunk': 'init', 'pos': (0,0)},
            '13' : {'sunk': 'init', 'pos': (0,0)},
            '14' : {'sunk': 'init', 'pos': (0,0)},
            '15' : {'sunk': 'init', 'pos': (0,0)}
        }

        my_sim = Simulation(draw=1)
        my_sim.set_state(sim_init_state)

        my_sim.draw.draw_frame(my_sim.geometry)
        my_sim.draw.save_image(filename)

    @staticmethod
    def on_gen(ga_instance):
        ga_instance.stats['gen_fitness'].append(ga_instance.best_solution()[1])
        print("Generation : ", ga_instance.generations_completed)
        print("Fitness of the best solution :", ga_instance.best_solution()[1])

    @staticmethod
    def naive_approach(num_generations=10, num_parents_mating=2, sol_per_pop=50):
        ga_instance = pygad.GA(
            num_generations=num_generations,
            num_parents_mating=num_parents_mating,
            fitness_func=Optimize.naive_fitness_func,
            mutation_type=Optimize.adaptive_mutation_func,
            sol_per_pop=sol_per_pop,
            num_genes=len(GENE_SPACE),
            gene_space=GENE_SPACE,
            parallel_processing=['process', 12],
            on_generation=Optimize.on_gen
        )
        ga_instance.stats = {
            'gen_fitness': []
        }

        ga_instance.run()

        solution, fitness, _ = ga_instance.best_solution()
        return solution, fitness, ga_instance.stats

    @staticmethod
    def informed_approach(num_generations=10, num_parents_mating=2, sol_per_pop=50):
        ga_instance = pygad.GA(
            num_generations=num_generations,
            num_parents_mating=num_parents_mating,
            fitness_func=Optimize.informed_fitness_func,
            mutation_type=Optimize.adaptive_mutation_func,
            sol_per_pop=sol_per_pop,
            num_genes=len(GENE_SPACE),
            gene_space=GENE_SPACE,
            parallel_processing=['process', 12],
            on_generation=Optimize.on_gen
        )
        ga_instance.stats = {
            'gen_fitness': []
        }

        ga_instance.run()

        solution, fitness, _ = ga_instance.best_solution()
        return solution, fitness, ga_instance.stats

