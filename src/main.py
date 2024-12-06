import sim
from pool_state import PoolState
from draw import Draw

# lib
from scipy.spatial.distance import cdist
import numpy as np
import random
import pygad

from mcts.base.base import BaseState, BaseAction
from mcts.searcher.mcts import MCTS

def naive_fitness_func(ga_instance, solution, solution_idx):
    positions = [(solution[i], solution[i+1]) for i in range(0, len(solution), 2)]

    distance_matrix = cdist(positions, positions)
    intersect_matrix = distance_matrix <= (sim.BALL_RADIUS*2)
    np.fill_diagonal(intersect_matrix, False)
    intersect_count = np.count_nonzero(intersect_matrix)

    total_score = 0
    samples_per_action = 20

    for _ in range(samples_per_action):
        init_state = {
            'p1' : {'sunk': 'init', 'pos': sim.random_pos(True)},
            'p2' : {'sunk': None, 'pos': sim.random_pos(False)},
            '1' : {'sunk': None, 'pos': positions[0]},
            '2' : {'sunk': None, 'pos': positions[1]},
            '3' : {'sunk': None, 'pos': positions[2]},
            '4' : {'sunk': None, 'pos': positions[3]},
            '5' : {'sunk': None, 'pos': positions[4]},
            '6' : {'sunk': None, 'pos': positions[5]},
            '7' : {'sunk': None, 'pos': positions[6]},
            '9' : {'sunk': None, 'pos': sim.random_pos(False)},
            '10' : {'sunk': None, 'pos': sim.random_pos(False)},
            '11' : {'sunk': None, 'pos': sim.random_pos(False)},
            '12' : {'sunk': None, 'pos': sim.random_pos(False)},
            '13' : {'sunk': None, 'pos': sim.random_pos(False)},
            '14' : {'sunk': None, 'pos': sim.random_pos(False)},
            '15' : {'sunk': None, 'pos': sim.random_pos(False)}
        }
        my_sim = sim.Simulation(True)
        actions = my_sim.actions(init_state, 2) 
        for dir, origin in actions:
            power = 1000000 * random.uniform(0.5, 1.5)
            end_state = my_sim.move(init_state, 2, dir, origin, power)
            total_score += sim.eval(end_state)

    averge_score = total_score / (len(actions) * samples_per_action)
    fitness = averge_score - intersect_count

    print('fitness:', fitness)

    return fitness

def informed_fitness_func(ga_instance, solution, solution_idx):
    positions = [(solution[i], solution[i+1]) for i in range(0, len(solution), 2)]

    distance_matrix = cdist(positions, positions)
    intersect_matrix = distance_matrix <= (sim.BALL_RADIUS*2)
    np.fill_diagonal(intersect_matrix, False)
    intersect_count = np.count_nonzero(intersect_matrix)

    total_score = 0
    searches_per_sample = 2
    iterations_per_search = 20

    for _ in range(searches_per_sample):
        init_state = {
            'p1' : {'sunk': 'init', 'pos': sim.random_pos(True)},
            'p2' : {'sunk': None, 'pos': sim.random_pos(False)},
            '1' : {'sunk': None, 'pos': positions[0]},
            '2' : {'sunk': None, 'pos': positions[1]},
            '3' : {'sunk': None, 'pos': positions[2]},
            '4' : {'sunk': None, 'pos': positions[3]},
            '5' : {'sunk': None, 'pos': positions[4]},
            '6' : {'sunk': None, 'pos': positions[5]},
            '7' : {'sunk': None, 'pos': positions[6]},
            '9' : {'sunk': None, 'pos': sim.random_pos(False)},
            '10' : {'sunk': None, 'pos': sim.random_pos(False)},
            '11' : {'sunk': None, 'pos': sim.random_pos(False)},
            '12' : {'sunk': None, 'pos': sim.random_pos(False)},
            '13' : {'sunk': None, 'pos': sim.random_pos(False)},
            '14' : {'sunk': None, 'pos': sim.random_pos(False)},
            '15' : {'sunk': None, 'pos': sim.random_pos(False)}
        }
        
        my_sim = sim.Simulation(False)
        initial_state = PoolState(init_state, my_sim)
        searcher = MCTS(iteration_limit=iterations_per_search)
        searcher.search(initial_state=initial_state)
        total_score += searcher.root.totalReward

    averge_score = total_score / (searches_per_sample * iterations_per_search)
    fitness = averge_score - intersect_count

    print('fitness:', fitness)

    return fitness

if __name__ == '__main__':
    p1, p2 = sim.P1_BOUNDS
    gene_space = [
        range(p1[0], p2[0]),
        range(p1[1], p2[1]),
        range(p1[0], p2[0]),
        range(p1[1], p2[1]),
        range(p1[0], p2[0]),
        range(p1[1], p2[1]),
        range(p1[0], p2[0]),
        range(p1[1], p2[1]),
        range(p1[0], p2[0]),
        range(p1[1], p2[1]),
        range(p1[0], p2[0]),
        range(p1[1], p2[1]),
        range(p1[0], p2[0]),
        range(p1[1], p2[1]),
    ]

    ga_instance = pygad.GA(
        num_generations=10,
        num_parents_mating=2,
        fitness_func=informed_fitness_func,
        sol_per_pop=50,
        num_genes=len(gene_space),
        gene_space=gene_space,
        parallel_processing=["process", 12]
    )

    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Best solution:", solution)
    print("Best fitness:", solution_fitness)

    positions = [(solution[i], solution[i+1]) for i in range(0, len(solution), 2)]
    init_state = {
        'p1' : {'sunk': 'init', 'pos': sim.random_pos(True)},
        'p2' : {'sunk': None, 'pos': sim.random_pos(False)},
        '1' : {'sunk': None, 'pos': positions[0]},
        '2' : {'sunk': None, 'pos': positions[1]},
        '3' : {'sunk': None, 'pos': positions[2]},
        '4' : {'sunk': None, 'pos': positions[3]},
        '5' : {'sunk': None, 'pos': positions[4]},
        '6' : {'sunk': None, 'pos': positions[5]},
        '7' : {'sunk': None, 'pos': positions[6]},
        '9' : {'sunk': None, 'pos': sim.random_pos(False)},
        '10' : {'sunk': None, 'pos': sim.random_pos(False)},
        '11' : {'sunk': None, 'pos': sim.random_pos(False)},
        '12' : {'sunk': None, 'pos': sim.random_pos(False)},
        '13' : {'sunk': None, 'pos': sim.random_pos(False)},
        '14' : {'sunk': None, 'pos': sim.random_pos(False)},
        '15' : {'sunk': None, 'pos': sim.random_pos(False)}
    }

    sol_sim = sim.Simulation(True)
    sol_sim.set_state(init_state)

    while True:
        sol_sim.draw.draw_frame(sol_sim.geometry)
