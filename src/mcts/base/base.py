from abc import ABC, abstractmethod


class BaseAction(ABC):
    def __eq__(self, other):
        raise NotImplementedError()

    def __hash__(self):
        raise NotImplementedError()


class BaseState(ABC):
    """
    Baseclass for all states of a Monte Carlo Tree Search.

    This describes the state of the game/world, and the actions that can be taken from it.
    """

    @abstractmethod
    def get_current_player(self) -> int:
        """
        Returns the player whose turn it is to play.

         1 ... it is the maximizer player's turn
        -1 ... it is the minimizer player's turn

        Returns
        -------
        int: the player whose turn it is to play
        """
        raise NotImplementedError()

    @abstractmethod
    def get_possible_actions(self) -> [any]:
        """
        Returns a list of all possible actions that can be taken from this state.

        Returns
        -------
        [any]: a list of all possible actions that can be taken from this state
        """
        raise NotImplementedError()

    @abstractmethod
    def take_action(self, action: any) -> 'BaseState':
        """
        Returns the state that results from taking the given action.

        Parameters
        ----------
        action: [any] BaseAction the action to take

        Returns
        -------
        BaseState: the state that results from taking the given action
        """
        raise NotImplementedError()

    @abstractmethod
    def is_terminal(self) -> bool:
        """
        Returns whether this state is a terminal state.

        Returns
        -------
        bool: whether this state is a terminal state
        """
        raise NotImplementedError()

    @abstractmethod
    def get_reward(self) -> float:
        """
        Returns the reward for this state. Only needed for terminal states.

        Returns
        -------
        float: the reward for this state
        """
        # only needed for terminal states
        raise NotImplementedError()
