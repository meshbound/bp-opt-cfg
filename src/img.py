from optimize import Optimize
from const import *

import numpy as np
import os

if __name__ == '__main__':
    
    root_dir = './data/'
    out_dir = './img/'

    # Positions by generation

    naive_positions_path = '{}naive_positions.csv'.format(root_dir)
    if os.path.exists(naive_positions_path):
        naive_positions_raw = np.genfromtxt(naive_positions_path, delimiter=',')

        for i in range(naive_positions_raw.shape[0]):
            img_path = '{}naive/sol_{}.png'.format(out_dir, i)
            Optimize.save_image_of_solution(naive_positions_raw[i], img_path)
            
    informed_positions_path = '{}informed_positions.csv'.format(root_dir)
    if os.path.exists(informed_positions_path):
        informed_positions = np.genfromtxt(informed_positions_path, delimiter=',')

        for i in range(informed_positions.shape[0]):
            img_path = '{}informed/sol_{}.png'.format(out_dir, i)
            Optimize.save_image_of_solution(informed_positions[i], img_path)

