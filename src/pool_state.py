import sim

import operator
from copy import deepcopy
from functools import reduce

from mcts.base.base import BaseState, BaseAction
from mcts.searcher.mcts import MCTS

class PoolState(BaseState):
    def __init__(self, ball_info, simulator):
        self.ball_info = ball_info
        self.simulator = simulator
        self.current_player = 2
        self.depth = 0
        self.actions = None

    def get_current_player(self):
        return self.current_player

    def get_possible_actions(self):
        if not self.actions:
            actions = self.simulator.actions(self.ball_info, self.current_player)
            proper = []
            for (dir, origin) in actions:
                proper.append(Action(self.current_player, dir, origin, 1000000))
            self.actions = proper

        return self.actions

    def take_action(self, action):
        ball_info = self.simulator.move(self.ball_info, self.current_player, action.dir, action.origin, action.power)

        new_state = PoolState(ball_info, self.simulator)
        new_state.current_player = 1 if self.current_player == 2 else 2
        new_state.depth = self.depth + 1
        
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
