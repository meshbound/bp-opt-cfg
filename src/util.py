# constants
from const import *

import random

def pretty_print_state(state):
    out = ''
    for label in state:
        out += label + '\n'
        for key in state[label]:
            val = state[label][key]
            out += '\t' + key + '\t: ' + str(val) + '\n'
    print(out)

def random_pos(p1):
    (x0, y0), (x1, y1) = P1_BOUNDS if p1 else P2_BOUNDS
    return (x0 + random.random() * (x1 - x0), y0 + random.random() * (y1 - y0))

def eval(state):
    score = 0
    for ball in state:
        if ball in ['p1', 'p2']:
            continue
        if state[ball]['sunk'] == None:
            pos = state[ball]['pos']
            if pos[0] > P2_BOUNDS[0][0]:
                score -= 1
            elif pos[0] < P1_BOUNDS[1][0]:
                score += 1
    return score
