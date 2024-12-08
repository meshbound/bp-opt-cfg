import sim
import util
import const

import operator
from copy import deepcopy
from functools import reduce

from mcts.base.base import BaseState, BaseAction
from mcts.searcher.mcts import MCTS

class State(BaseState):
    def __init__(self, sim_state, simulation):
        self.sim_state = sim_state
        self.simulation = simulation
        self.current_player = 2
        self.depth = 0
        self.actions = None

    def get_current_player(self):
        return self.current_player

    def get_possible_actions(self):
        if not self.actions:
            actions = self.simulation.actions(self.sim_state, self.current_player)
            proper = []
            for dir, origin, power in actions:
                proper.append(Action(self.current_player, dir, origin, power))
            self.actions = proper

        return self.actions

    def take_action(self, action):
        sim_state = self.simulation.move(
            self.sim_state,
            self.current_player,
            action.dir,
            action.origin,
            action.power
        )

        new_state = State(sim_state, self.simulation)
        new_state.current_player = 1 if self.current_player == 2 else 2
        new_state.depth = self.depth + 1
        
        return new_state

    def is_terminal(self):
        if self.depth > const.PLAYOUT_DEPTH_LIMIT:
            return True
        return util.is_terminal(self.sim_state)

    def get_reward(self):
        return util.eval(self.sim_state)


class Action(BaseAction):
    def __init__(self, player, dir, origin, power):
        self.player = player
        self.dir = dir
        self.origin = origin
        self.power = power

    def __str__(self):
        return str(
            (self.dir,
             self.origin,
             self.power)
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ 
            and self.dir[0] == other.dir[0]
            and self.dir[1] == other.dir[1]
            and self.origin[0] == other.origin[0]
            and self.origin[1] == other.origin[1]
            and self.power == other.power 
            and self.player == other.player
        )

    def __hash__(self):
        return hash(
            (self.dir[0],
             self.dir[1],
             self.origin[0],
             self.origin[1],
             self.power,
             self.player)
        )
