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
    def naive_fitness_func(ga_instance, solution, solution_idx):
        positions = Optimize.unpack_positions(solution)
        intersect_count = Optimize.get_intersect_count(positions)

        total_score = 0
        samples_per_action = 20

        for _ in range(samples_per_action):
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
            my_sim = Simulation(False)
            actions = my_sim.actions(sim_init_state, 2) 
            for dir, origin, power in actions:
                end_state = my_sim.move(sim_init_state, 2, dir, origin, power)
                total_score += util.eval(end_state)

        averge_score = total_score / (len(actions) * samples_per_action)
        fitness = averge_score - intersect_count

        print('fitness:', fitness)

        return fitness

    @staticmethod
    def informed_fitness_func(ga_instance, solution, solution_idx):
        positions = Optimize.unpack_positions(solution)
        intersect_count = Optimize.get_intersect_count(positions)

        total_score = 0
        searches_per_sample = 2
        iterations_per_search = 20

        for _ in range(searches_per_sample):
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
            
            my_sim = Simulation(True)

            mcts_init_state = State(sim_init_state, my_sim)
            searcher = MCTS(iteration_limit=iterations_per_search)
            searcher.search(initial_state=mcts_init_state)

            total_score += searcher.root.totalReward

        averge_score = total_score / (searches_per_sample * iterations_per_search)
        fitness = averge_score - intersect_count

        print('fitness:', fitness)

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

        my_sim = Simulation(True)
        my_sim.set_state(sim_init_state)

        while True:
            my_sim.draw.draw_frame(my_sim.geometry)

    @staticmethod
    def naive_approach(num_generations=10, num_parents_mating=2, sol_per_pop=50):
        ga_instance = pygad.GA(
            num_generations=num_generations,
            num_parents_mating=num_parents_mating,
            fitness_func=Optimize.naive_fitness_func,
            mutation_type=Optimize.mutation_func,
            sol_per_pop=sol_per_pop,
            num_genes=len(GENE_SPACE),
            gene_space=GENE_SPACE,
            #parallel_processing=['process', 12]
        )

        ga_instance.run()

        solution, fitness, _ = ga_instance.best_solution()

        print("Best solution:", solution)
        print("Best fitness:", fitness)

        return solution, fitness

    @staticmethod
    def informed_approach(num_generations=10, num_parents_mating=2, sol_per_pop=50):
        ga_instance = pygad.GA(
            num_generations=num_generations,
            num_parents_mating=num_parents_mating,
            fitness_func=Optimize.informed_fitness_func,
            mutation_type=Optimize.mutation_func,
            sol_per_pop=sol_per_pop,
            num_genes=len(GENE_SPACE),
            gene_space=GENE_SPACE,
            #parallel_processing=['process', 12]
        )

        ga_instance.run()

        solution, fitness, _ = ga_instance.best_solution()

        print("Best solution:", solution)
        print("Best fitness:", fitness)

        return solution, fitness

