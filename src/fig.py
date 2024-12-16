from const import *

from scipy.stats import gaussian_kde
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams['font.family'] = 'Serif' 

ROOT_DIR = './data/'
OUT_DIR = './fig/'

def fig_naive_fitness():
    naive_fitness_path = '{}naive_fitness.csv'.format(ROOT_DIR)
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
        plt.savefig('{}naive_fitness.png'.format(OUT_DIR), dpi=300)

def fig_informed_fitness():
    informed_fitness_path = '{}informed_fitness.csv'.format(ROOT_DIR)
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
        plt.savefig('{}informed_fitness.png'.format(OUT_DIR), dpi=300)

def fig_naive_positions():
    naive_positions_path = '{}naive_positions.csv'.format(ROOT_DIR)
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
        plt.savefig('{}naive_positions.png'.format(OUT_DIR), dpi=300)

def fig_informed_positions():
    informed_positions_path = '{}informed_positions.csv'.format(ROOT_DIR)
    if os.path.exists(informed_positions_path):
        informed_positions_raw = np.genfromtxt(informed_positions_path, delimiter=',')

        informed_positions = np.array([
            informed_positions_raw[:, ::2].flatten(), 
            informed_positions_raw[:, 1::2].flatten()
        ])

        plt.figure(4)

        kde = gaussian_kde(informed_positions, bw_method=0.05)
        X, Y = np.meshgrid(np.linspace(P1_BOUNDS[0][0], P1_BOUNDS[1][0], 100), np.linspace(P1_BOUNDS[0][1], P1_BOUNDS[1][1], 100))
        Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

        plt.pcolormesh(X, Y, Z, shading='auto', cmap='viridis')
        plt.colorbar(label='Density')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.savefig('{}informed_positions.png'.format(OUT_DIR), dpi=300)

def fig_mcts_final():
    naive_mcts_final_path = '{}naive_mcts_final.csv'.format(ROOT_DIR)
    informed_mcts_final_path = '{}informed_mcts_final.csv'.format(ROOT_DIR)
    if os.path.exists(naive_mcts_final_path) and os.path.exists(informed_mcts_final_path):
        naive_mcts_final = np.genfromtxt(naive_mcts_final_path, delimiter=',')
        informed_mcts_final = np.genfromtxt(informed_mcts_final_path, delimiter=',')

        fig = plt.figure(5)

        ax = fig.add_subplot(111)
        ax.set_aspect(2)

        bplot = ax.boxplot([naive_mcts_final, informed_mcts_final], vert=True, patch_artist=True, widths=[0.5,0.5])

        for patch, color in zip(bplot['boxes'], ['lightblue','salmon']):
            patch.set_facecolor(color)

        for median in bplot['medians']:
            median.set_color('black')

        plt.xticks([1,2],['Naive', 'Informed'])
        plt.ylabel('Fitness')

        plt.savefig('{}mcts_final.png'.format(OUT_DIR), dpi=300)

def fig_mutation_prob_helper(steepness, offset, above_avg_prob, fig, name):
    f = lambda diff : (
        np.exp(steepness*diff + offset) / (1 + np.exp(steepness*diff + offset))
    )

    g = lambda fitness, mean: (
        f(np.abs(fitness - mean)) if fitness < mean else above_avg_prob
    )

    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)

    Z = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = g(X[i, j], Y[i, j])

    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='coolwarm')

    ax.set_xlabel('Fitness', fontsize=14)
    ax.set_ylabel('Mean Fitness', fontsize=14)
    ax.set_zlabel('Mutation Probability', fontsize=14)

    ax.view_init(elev=30, azim=30) 
    ax.set_zlim(0, 1)

    plt.tight_layout()
    plt.savefig('{}{}.png'.format(OUT_DIR, name), dpi=300)

def fig_naive_mutation_prob():
    steepness = NAIVE_MUTATION_PROB['steepness']
    offset = NAIVE_MUTATION_PROB['offset']
    above_avg_prob = NAIVE_MUTATION_PROB['above_avg_prob']

    fig = plt.figure(6)
    name = 'naive_mutation_prob'

    fig_mutation_prob_helper(steepness, offset, above_avg_prob, fig, name)

def fig_informed_mutation_prob():
    steepness = INFORMED_MUTATION_PROB['steepness']
    offset = INFORMED_MUTATION_PROB['offset']
    above_avg_prob = INFORMED_MUTATION_PROB['above_avg_prob']

    fig = plt.figure(7)
    name = 'informed_mutation_prob'

    fig_mutation_prob_helper(steepness, offset, above_avg_prob, fig, name)

def fig_mutation_sd(steepness, offset, scale, minimum, color, name):
    f = lambda gen : (
        scale*np.exp(steepness*gen + offset)/(1 + np.exp(steepness*gen + offset)) + minimum
    )

    x = np.linspace(0, 20, 200)
    y = np.array([f(i) for i in x])
    plt.plot(x, y, color=color)

    plt.xlabel('Generation', fontsize=16)
    plt.ylabel('Mutation Std Dev', fontsize=16)

    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.ylim(0,40)

    plt.tight_layout()
    plt.savefig('{}{}.png'.format(OUT_DIR, name), dpi=300)

def fig_naive_mutation_sd():
    steepness = NAIVE_MUTATION_SD['steepness']
    offset = NAIVE_MUTATION_SD['offset']
    scale = NAIVE_MUTATION_SD['scale']
    minimum = NAIVE_MUTATION_SD['minimum']

    plt.figure(8)
    color = 'blue'
    name = 'naive_mutation_sd'

    fig_mutation_sd(steepness, offset, scale, minimum, color, name)

def fig_informed_mutation_sd():
    steepness = INFORMED_MUTATION_SD['steepness']
    offset = INFORMED_MUTATION_SD['offset']
    scale = INFORMED_MUTATION_SD['scale']
    minimum = INFORMED_MUTATION_SD['minimum']

    plt.figure(9)
    color = 'red'
    name = 'informed_mutation_sd'

    fig_mutation_sd(steepness, offset, scale, minimum, color, name)


def fig_penalty_mult():
    steepness = PENALTY_MULT['steepness']
    offset = PENALTY_MULT['offset']

    penalty_mult = lambda gen : np.exp(steepness*gen+offset)/(1+np.exp(steepness*gen+offset))

    plt.figure(10)

    x = np.linspace(0, 20, 100)
    y = np.array([penalty_mult(i) for i in x])
    plt.plot(x, y, color='green')

    plt.xlabel('Generation', fontsize=16)
    plt.ylabel('Penalty Multiplier', fontsize=16)

    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()
    plt.savefig('{}penalty_mult.png'.format(OUT_DIR), dpi=300)

if __name__ == '__main__':
    # Parameters
    fig_naive_mutation_prob()
    fig_informed_mutation_prob()

    fig_naive_mutation_sd()
    fig_informed_mutation_sd()

    fig_penalty_mult()

    # Data analysis
    fig_naive_fitness()
    fig_naive_positions()

    fig_informed_fitness()
    fig_informed_positions()

    fig_mcts_final()
