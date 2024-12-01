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
    # TODO: reroll if the point is within a pocket
    (x0, y0), (x1, y1) = P1_BOUNDS if p1 else P2_BOUNDS

    pos = (x0 + random.random() * (x1 - x0), y0 + random.random() * (y1 - y0))

    pocket_check_left = pos[0] < P1_BOUNDS[0][0] + BALL_RADIUS and (pos[1] < P1_BOUNDS[0][1] + BALL_RADIUS or pos[1] > P1_BOUNDS[1][1] - BALL_RADIUS)
    pocket_check_right = pos[0] > P2_BOUNDS[1][0] - BALL_RADIUS and (pos[1] < P2_BOUNDS[0][0] + BALL_RADIUS or pos[1] > P2_BOUNDS[1][1] - BALL_RADIUS)
    
    if pocket_check_left or pocket_check_right :
        return random_pos(p1)
    else:
        return pos

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
