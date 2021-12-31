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

        max_reward = 0.0
        max_reward_action = None
        for action in legal_actions:
            reward = env.obtain_reward_of_action(action_to_action_space(action))
            if reward > max_reward:
                max_reward = reward
                max_reward_action = action

        if max_reward_action is None:
            # Fall back to random action
            max_reward_action = legal_actions[random.randint(0, len(legal_actions)-1)]

        return action_to_action_space(max_reward_action)
