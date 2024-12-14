from optimize import Optimize
from const import *

import numpy as np
import os

ROOT_DIR = './data/'
OUT_DIR = './img/'

def img_naive_positions():
    naive_positions_path = '{}naive_positions.csv'.format(ROOT_DIR)
    if os.path.exists(naive_positions_path):
        naive_positions_raw = np.genfromtxt(naive_positions_path, delimiter=',')

        for i in range(naive_positions_raw.shape[0]):
            img_path = '{}naive/sol_{}.png'.format(OUT_DIR, i)
            Optimize.save_image_of_solution(naive_positions_raw[i], img_path)

def img_informed_positions():
    informed_positions_path = '{}informed_positions.csv'.format(ROOT_DIR)
    if os.path.exists(informed_positions_path):
        informed_positions = np.genfromtxt(informed_positions_path, delimiter=',')

        for i in range(informed_positions.shape[0]):
            img_path = '{}informed/sol_{}.png'.format(OUT_DIR, i)
            Optimize.save_image_of_solution(informed_positions[i], img_path)

if __name__ == '__main__':
    img_naive_positions()
    img_informed_positions()
