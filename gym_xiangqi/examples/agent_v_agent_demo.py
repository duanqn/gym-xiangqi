from gym_xiangqi.agents import RandomAgent, GreedyAgent
from gym_xiangqi.constants import ALLY, PIECE_ID_TO_NAME_CHS
from gym_xiangqi.utils import action_space_to_move

import gym
import time


def main():
    env = gym.make('gym_xiangqi:xiangqi-v0')
    env.render()
    red_agent = RandomAgent()
    black_agent = GreedyAgent()

    done = False
    round = 0
    env.reset()
    while not done:
        # Add a slight delay to properly visualize the game.
        time.sleep(0.1)

        agent = black_agent if env.turn == ALLY else red_agent
        action = agent.move(env)
        _, reward, done, _ = env.step(action)

        player = "黑方" if env.turn == ALLY else "红方"
        move = action_space_to_move(action)
        piece = PIECE_ID_TO_NAME_CHS[0 if env.turn == ALLY else 1][move[0]]
        print(f"Round: {round}")
        print(f"{player} made the move {piece} from {move[1]} to {move[2]}.")
        print(f"Reward: {reward}")
        if env.jiangjun:
            print("将军！")
        print("================")

        round += 1
        env.render()

    print("Game finished!")
    env.close()


if __name__ == '__main__':
    main()
