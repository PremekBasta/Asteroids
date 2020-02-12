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
        state = env.reset()
        transformed_state, action_plans = agent_one.get_state_info(state)

        # reshape

        obs = np.reshape(obs, newshape=(1, -1))
        done = False
        R = 0
        t = 0
        while not done:
            old_transformed_state = transformed_state
            action_plan_index = choose_action_plan_index(transformed_state)
            action = get_action_for_action_plan(action_plan_index)

            old_state = obs
            action = agent.action(obs, train=True)

            step_count, (game_over, rocket_one_won), state, agent_one_actions, agent_two_actions, reward = env.next_step(
                actions_one, actions_two)

            transformed_state, action_plans = transform_state(state)

            R += r

            agent.record_experience((old_transformed_state, action_plan_index, reward, transformed_state, game_over))
        agent.train()

        # rewards.append(R)
        # print(i, R)
