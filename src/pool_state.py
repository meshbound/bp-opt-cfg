import sim

from __future__ import division

import operator
from copy import deepcopy
from functools import reduce

from mcts.base.base import BaseState, BaseAction
from mcts.searcher.mcts import MCTS

class PoolState(BaseState):
    def __init__(self, ball_info):
        self.ball_info = ball_info
        self.currentPlayer = 1

    def get_current_player(self):
        return self.currentPlayer

    def get_possible_actions(self):
        
        possibleActions = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    possibleActions.append(Action(player=self.currentPlayer, x=i, y=j))
        return possibleActions

    def take_action(self, action):
        newState = deepcopy(self)
        newState.board[action.x][action.y] = action.player
        newState.currentPlayer = self.currentPlayer * -1
        return newState

    def is_terminal(self):
        # can include depth limit in here
        for row in self.board:
            if abs(sum(row)) == 3:
                return True
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == 3:
                return True
        for diagonal in [[self.board[i][i] for i in range(len(self.board))],
                         [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))]]:
            if abs(sum(diagonal)) == 3:
                return True
        return reduce(operator.mul, sum(self.board, []), 1) != 0

    def get_reward(self):
        for row in self.board:
            if abs(sum(row)) == 3:
                return sum(row) / 3
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == 3:
                return sum(column) / 3
        for diagonal in [[self.board[i][i] for i in range(len(self.board))],
                         [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))]]:
            if abs(sum(diagonal)) == 3:
                return sum(diagonal) / 3
        return 0


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
        return self.__class__ == other.__class__ and self.dir == other.dir and self.origin == other.origin and self.power == other.power and self.player == other.player

    def __hash__(self):
        return hash((self.dir, self.origin, self.power, self.player))


if __name__ == "__main__":
    initial_state = NaughtsAndCrossesState()
    searcher = MCTS(time_limit=1000)
    action = searcher.search(initial_state=initial_state)

    print(action)
