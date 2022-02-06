import random
from gym_xiangqi.constants import ADVISOR_1, ADVISOR_2, ELEPHANT_1, ELEPHANT_2, GENERAL, SOLDIER_1, SOLDIER_2, SOLDIER_3, SOLDIER_4, SOLDIER_5

from gym_xiangqi.utils import action_to_action_space, ScopeExit
from gym_xiangqi.action import ActionTreeNode


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

        max_reward = -999999
        max_reward_action = None

        steps_lookahead = 1
        action_tree_root = ActionTreeNode(parent=None, action=None)
        self._visit(action_tree_root, env, max_depth=2*steps_lookahead, carried_result=0)

        max_reward = action_tree_root.result
        max_reward_action = action_tree_root.selected_child.action
        print(f'Choose max reward {max_reward}')

        if max_reward_action is None:
            # Fall back to random action
            max_reward_action = legal_actions[random.randint(0, len(legal_actions)-1)]

        return action_to_action_space(max_reward_action)

    def _visit(self, node: ActionTreeNode, env, max_depth, carried_result):
        if node.depth == max_depth:
            node.result = carried_result
            #print(f'Leaf node reward: {node.result}')
            node.finalizeResult()
            return

        legal_actions = env.get_actions_for_agent()

        extreme_result = None
        for action in legal_actions:
            if (not node.same_player_as_root()) and abs(action.piece) in [GENERAL, ADVISOR_1, ADVISOR_2, ELEPHANT_1, ELEPHANT_2, SOLDIER_1, SOLDIER_2, SOLDIER_3, SOLDIER_4, SOLDIER_5]:
                continue

            if node.alpha is not None and node.beta is not None and node.alpha > node.beta:
                # early return
                #print(f'Early return!')
                break
            else:
                #print(f'alpha: {node.alpha} beta: {node.beta}')
                pass
            child = node.addChild(action)

            # Visit child
            meta_info = env.save_meta_info()
            assert not env.done
            _, reward, done, info = env.step(action_to_action_space(action))
            if not child.same_player_as_root():
                reward = -reward
            if done:
                child.result = reward    # Should already include the reward of slaying general
                child.finalizeResult()
            else:
                self._visit(child, env, max_depth, carried_result=carried_result + reward)
            env.restore_from_playback(info['playback'], meta_info)

            if extreme_result is None:
                extreme_result = child.result
                node.selected_child = child
            else:
                if (not child.same_player_as_root()) and child.result < extreme_result:
                    #print(f'Update best result from {extreme_result} to {child.result} as it is lower')
                    extreme_result = child.result
                    node.selected_child = child
                elif child.same_player_as_root() and child.result > extreme_result:
                    #print(f'Update best result from {extreme_result} to {child.result} as it is higher')
                    extreme_result = child.result
                    node.selected_child = child
        
        #print(f'Node reward: {extreme_result}')
        node.result = extreme_result
        node.finalizeResult()
