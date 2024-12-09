from const import *

from scipy.stats import gaussian_kde
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import numpy as np
import os

if __name__ == '__main__':
    
    root_dir = './data/'
    out_dir = './fig/'

    # Best fitness by generation

    naive_fitness_path = '{}naive_fitness.csv'.format(root_dir)
    if os.path.exists(naive_fitness_path):
        naive_fitness = np.genfromtxt(naive_fitness_path, delimiter=',')

        plt.figure(1)

        mean_fitness_naive = naive_fitness.mean(axis=0)
        std_fitness_naive = naive_fitness.std(axis=0)

        x_naive = np.arange(naive_fitness.shape[1])
        plt.plot(x_naive, mean_fitness_naive, color='blue')
        plt.fill_between(x_naive, mean_fitness_naive - std_fitness_naive, mean_fitness_naive + std_fitness_naive, alpha=0.2, color='blue')

        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.savefig('{}naive_fitness.png'.format(out_dir))

    informed_fitness_path = '{}informed_fitness.csv'.format(root_dir)
    if os.path.exists(informed_fitness_path):
        informed_fitness = np.genfromtxt(informed_fitness_path, delimiter=',')

        plt.figure(2)

        mean_fitness_informed = informed_fitness.mean(axis=0)
        std_fitness_informed = informed_fitness.std(axis=0)

        x_informed = np.arange(informed_fitness.shape[1])
        plt.plot(x_informed, mean_fitness_informed, color='red')
        plt.fill_between(x_informed, mean_fitness_informed - std_fitness_informed, mean_fitness_informed + std_fitness_informed, alpha=0.2, color='red')

        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.savefig('{}informed_fitness.png'.format(out_dir))

    # Positions by generation

    naive_positions_path = '{}naive_positions.csv'.format(root_dir)
    if os.path.exists(naive_positions_path):
        naive_positions_raw = np.genfromtxt(naive_positions_path, delimiter=',')

        naive_positions = np.array([
            naive_positions_raw[:, ::2].flatten(), 
            naive_positions_raw[:, 1::2].flatten()
        ])

        plt.figure(3)

        kde = gaussian_kde(naive_positions, bw_method=0.05)
        X, Y = np.meshgrid(np.linspace(P1_BOUNDS[0][0], P1_BOUNDS[1][0], 100), np.linspace(P1_BOUNDS[0][1], P1_BOUNDS[1][1], 100))
        Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

        plt.pcolormesh(X, Y, Z, shading='auto', cmap='viridis')
        plt.colorbar(label='Density')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.savefig('{}naive_positions.png'.format(out_dir))

    informed_positions_path = '{}informed_positions.csv'.format(root_dir)
    if os.path.exists(informed_positions_path):
        informed_positions = np.genfromtxt(informed_positions_path, delimiter=',')

        informed_positions = np.array([
            informed_positions[:, ::2].flatten(), 
            naive_positions[:, 1::2].flatten()
        ])

        plt.figure(4)

        kde = gaussian_kde(informed_positions, bw_method=0.05)
        X, Y = np.meshgrid(np.linspace(P1_BOUNDS[0][0], P1_BOUNDS[1][0], 100), np.linspace(P1_BOUNDS[0][1], P1_BOUNDS[1][1], 100))
        Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

        plt.pcolormesh(X, Y, Z, shading='auto', cmap='viridis')
        plt.colorbar(label='Density')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.savefig('{}informed_positions.png'.format(out_dir))


    # MCTS eval by final solution

    naive_mcts_final_path = '{}naive_mcts_final.csv'.format(root_dir)
    informed_mcts_final_path = '{}informed_mcts_final.csv'.format(root_dir)
    if os.path.exists(naive_mcts_final_path) and os.path.exists(informed_mcts_final_path):
        naive_mcts_final = np.genfromtxt(naive_mcts_final_path, delimiter=',')
        informed_mcts_final = np.genfromtxt(informed_mcts_final_path, delimiter=',')

        plt.figure(5)

        plt.boxplot([naive_mcts_final, informed_mcts_final], vert=False, patch_artist=True, 
                boxprops=dict(facecolor='lightblue', color='black'),
                whiskerprops=dict(color='black', linewidth=1.5),
                flierprops=dict(marker='o', color='red', markersize=5),
                widths=[0.3,0.3])
        plt.yticks([1,2],['Naive', 'Informed'])
        plt.xlabel('Fitness')
        
        plt.savefig('{}mcts_final.png'.format(out_dir))
