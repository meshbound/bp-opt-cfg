from optimize import Optimize
import const

import csv
import numpy as np

out_dir = './data/'

def gen_naive_data():
    print('naive data')

    num_runs = 10

    gen_per_run = 20
    sol_pop = 80

    for _ in range(num_runs):

        solution, _, gen_fitness = Optimize.naive_approach(gen_per_run, 2, sol_pop)

        with open('{}naive_fitness.csv'.format(out_dir), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(gen_fitness)
            f.close()

        with open('{}naive_positions.csv'.format(out_dir), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(solution)
            f.close()

def gen_informed_data():
    print('informed data')
    
    num_runs = 10

    gen_per_run = 20
    sol_pop = 80

    for _ in range(num_runs):

        solution, _, gen_fitness = Optimize.informed_approach(gen_per_run, 2, sol_pop)

        with open('{}informed_fitness.csv'.format(out_dir), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(gen_fitness)
            f.close()

        with open('{}informed_positions.csv'.format(out_dir), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(solution)
            f.close()

def mcts_naive_final():
    print('mcts naive final')

    const.PLAYOUT_DEPTH_LIMIT = 10
    searches_per_sample = 10
    iterations_per_search = 50

    # For each solution we run MCTS to get the fitness
    naive_positions_path = '{}naive_positions.csv'.format(out_dir)
    naive_positions = np.genfromtxt(naive_positions_path, delimiter=',')

    fitness_vals = []
    for solution in naive_positions:
        fitness = Optimize.get_informed_fitness(solution, searches_per_sample, iterations_per_search)
        fitness_vals.append(fitness)

    with open('{}naive_mcts_final.csv'.format(out_dir), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fitness_vals)
            f.close()

def mcts_informed_final():
    print('mcts informed final')

    const.PLAYOUT_DEPTH_LIMIT = 10
    searches_per_sample = 10
    iterations_per_search = 50

    # For each solution we run MCTS to get the fitness
    informed_positions_path = '{}informed_positions.csv'.format(out_dir)
    informed_positions = np.genfromtxt(informed_positions_path, delimiter=',')

    fitness_vals = []
    for solution in informed_positions:
        fitness = Optimize.get_informed_fitness(solution, searches_per_sample, iterations_per_search)
        fitness_vals.append(fitness)

    with open('{}informed_mcts_final.csv'.format(out_dir), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fitness_vals)
            f.close()
