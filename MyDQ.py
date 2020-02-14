import random

import tensorflow as tf
import numpy as np

from enviroment import *
from agents import *

if __name__ == '__main__':
    agent_one = DQAgent(player_number = 1, num_inputs = 4, num_outputs = 4)
    agent_two = Stable_defensive_agent(2)

    env = Enviroment(VISUAL, ROCKET_ONE_INVULNERABLE, ROCKET_TWO_INVULNERABLE)

    # spustime trenovani na 1000 epizodach prostredi
    rewards = []
    for i in range(1000):
        agent_one.history = [0,0,0,0]
        state = env.reset()
        transformed_state, action_plans = agent_one.get_state_info(state)

        # reshape
        transformed_state = np.reshape(transformed_state, newshape=(1,-1))
        game_over = False
        R = 0
        while not game_over:
            old_transformed_state = transformed_state
            action_plan_index = agent_one.choose_action_plan_index(transformed_state)
            actions_one = agent_one.get_action_from_action_plan(action_plan_index, action_plans)

            actions_two = agent_two.choose_actions(state, [])

            step_count, (game_over, rocket_one_won), state, _, _ = env.next_step(actions_one, actions_two)
            if not game_over:
                reward = 1
            else:
                if rocket_one_won:
                    reward = 2000
                else:
                    reward = -1000


            transformed_state, action_plans = agent_one.get_state_info(state)
            transformed_state = np.reshape(transformed_state, newshape=(1, -1))

            R += reward

            agent_one.record_experience((old_transformed_state, action_plan_index, reward, transformed_state, game_over))
        agent_one.train()

        # rewards.append(R)
        print(i, R)
        print(agent_one.history)
