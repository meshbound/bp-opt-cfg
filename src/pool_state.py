import sim

import operator
from copy import deepcopy
from functools import reduce

from mcts.base.base import BaseState, BaseAction
from mcts.searcher.mcts import MCTS

state_sim = sim.Simulation()

class PoolState(BaseState):
    def __init__(self, ball_info):
        self.ball_info = ball_info
        self.current_player = 2
        self.depth = 0

    def get_current_player(self):
        return self.current_player

    def get_possible_actions(self):
        actions = state_sim.actions(self.ball_info, self.current_player)
        
        proper = []
        for (dir, origin) in actions:
            proper.append(Action(self.current_player, dir, origin, 1000000))

        return proper

    def take_action(self, action):
        new_state = deepcopy(self)
        new_state.ball_info = state_sim.move(self.ball_info, self.current_player, action.dir, action.origin, action.power)
        new_state.current_player = 1 if self.current_player == 2 else 2
        new_state.depth += 1
        return new_state

    def is_terminal(self):
        if self.depth > 4:
            return True
        return sim.is_terminal(self.ball_info)

    def get_reward(self):
        return sim.eval(self.ball_info)


class Action(BaseAction):
    def __init__(self, player, dir, origin, power):
        self.player = player
        self.dir = dir
        self.origin = origin
        self.power = power

    def __str__(self):
        return str((self.dir, self.origin, self.power))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.dir[0] == other.dir[0] and self.dir[1] == other.dir[1] and self.origin[0] == other.origin[0] and self.origin[1] == other.origin[1] and self.power == other.power and self.player == other.player

    def __hash__(self):
        return hash((self.dir[0], self.dir[1], self.origin[0], self.origin[1], self.power, self.player))


if __name__ == "__main__":
    init_state = {
        'p1' : {'sunk': 'init', 'pos': sim.random_pos(True)},
        'p2' : {'sunk': None, 'pos': sim.random_pos(False)},
        '1' : {'sunk': None, 'pos': sim.random_pos(True)},
        '2' : {'sunk': None, 'pos': sim.random_pos(True)},
        '3' : {'sunk': None, 'pos': sim.random_pos(True)},
        '4' : {'sunk': None, 'pos': sim.random_pos(True)},
        '5' : {'sunk': None, 'pos': sim.random_pos(True)},
        '6' : {'sunk': None, 'pos': sim.random_pos(True)},
        '7' : {'sunk': None, 'pos': sim.random_pos(True)},
        '9' : {'sunk': None, 'pos': sim.random_pos(False)},
        '10' : {'sunk': None, 'pos': sim.random_pos(False)},
        '11' : {'sunk': None, 'pos': sim.random_pos(False)},
        '12' : {'sunk': None, 'pos': sim.random_pos(False)},
        '13' : {'sunk': None, 'pos': sim.random_pos(False)},
        '14' : {'sunk': None, 'pos': sim.random_pos(False)},
        '15' : {'sunk': None, 'pos': sim.random_pos(False)}
    }
    
    initial_state = PoolState(init_state)
    searcher = MCTS(iteration_limit=25)
    searcher.search(initial_state=initial_state)

    print(searcher.root.totalReward / searcher.root.numVisits)
 