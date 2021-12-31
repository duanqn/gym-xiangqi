import random

from gym_xiangqi.utils import action_to_action_space


class GreedyAgent:
    """
    This is the implementation of the greediest
    agent possible to play the game of Xiang Qi.
    The agent will choose the move with max reward.
    """
    def __init__(self):
        pass

    def move(self, env):
        """
        Make a greedy move based on the environment.
        """
        legal_actions = env.get_actions_for_agent()
        idx = random.randint(0, len(legal_actions)-1)
        return action_to_action_space(legal_actions[idx])
