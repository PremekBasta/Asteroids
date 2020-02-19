import random
import os
import tensorflow as tf
import numpy as np
from multiprocessing import *
from filelock import FileLock
import timeit
from datetime import datetime





from enviroment import *
from agents import *

def simulate_one_game(index, env, agent_one, agent_two, episode_num, exp_buffers, file):
    rewards = []
    state = env.reset()
    agent_one.history = [0,0,0,0]
    transformed_state, action_plans = agent_one.get_state_info(state)
    transformed_state = np.reshape(transformed_state, newshape=(1, -1))
    game_over = False
    R = 0
    while not game_over:
        old_transformed_state = transformed_state
        action_plan_index = agent_one.choose_action_plan_index(transformed_state)
        actions_one = agent_one.get_action_from_action_plan(action_plan_index, action_plans)

        actions_two = agent_two.choose_actions(state, [])

        step_count, (game_over, rocket_one_won), state, _, _, reward = env.next_step(actions_one, actions_two)
        if not game_over:
            reward += 1

        else:
            if rocket_one_won:
                reward += 2000
            else:
                reward += -1000

        transformed_state, action_plans = agent_one.get_state_info(state)
        transformed_state = np.reshape(transformed_state, newshape=(1, -1))

        R += reward
        agent_one.record_experience(
            (old_transformed_state, action_plan_index, reward, transformed_state, game_over))
    exp_buffers[index] = agent_one.exp_buffer
    #agent_one.train()

    print(f"episode_num: {episode_num}, thread_num: {index}, reward: {R}, history: {agent_one.history}")
    with FileLock("myfile.txt.lock"):
        file.write("#, " + str(episode_num) + ", " + str(index) + ", " + str(R) + "\n")
        file.write(str(agent_one.history) + "\n\n")
        file.flush()
    #semi_result[index-1] = step_count - agent_one.penalty
    #print(semi_result)
    #return step_count
    #return_vals[index] = result
    #return

def train_parallel(num_cores = 4, num_episodes = 200):
    processes = []
    manager = Manager()

    exp_buffers = manager.list()
    for i in range(num_cores):
        exp_buffers.append(manager.list())
    agents_one = [None for i in range(num_cores)]
    agents_two = [Stable_defensive_agent(2) for i in range(num_cores)]
    envs = [Enviroment(VISUAL, ROCKET_ONE_INVULNERABLE, ROCKET_TWO_INVULNERABLE) for i in range(num_cores)]

    agents_one[0] = DQAgent(player_number=1, num_inputs=4, num_outputs=4)
    for i in range(1, num_cores):
        agents_one[i] = DQAgent(player_number=1, num_inputs=4, num_outputs=4, model=agents_one[0].model)


    with open("model_multiprocessing_training.txt", "w+") as f:
        for episode_num in range(num_episodes):
            for i in range(num_cores):
                processes.append(
                    Process(target=simulate_one_game, args=(i, envs[i], agents_one[i], agents_two[i], episode_num, exp_buffers, f)))



            for i in range(num_cores):
                processes[i].start()
            for i in range(num_cores):
                processes[i].join()

            for i in range(1,4):
                exp_buffers[0] = exp_buffers[0] + exp_buffers[i]



            agents_one[0].train(exp_buffers[0])
            exp_buffers[0] = []
            processes = []

        #result = sum(return_vals.values()) // 6
        #return result,

def train_single_thread(num_episodes):
    with open("model_training_2000", "w+") as f:
        agent_one = DQAgent(player_number=1, num_inputs=4, num_outputs=4)
        agent_two = Stable_defensive_agent(2)
        env = Enviroment(VISUAL, ROCKET_ONE_INVULNERABLE, ROCKET_TWO_INVULNERABLE)
        for i in range(num_episodes):
            rewards = []
            agent_one.history = [0, 0, 0, 0]
            state = env.reset()
            transformed_state, action_plans = agent_one.get_state_info(state)
            transformed_state = np.reshape(transformed_state, newshape=(1, -1))
            game_over = False
            R = 0
            while not game_over:
                old_transformed_state = transformed_state
                action_plan_index = agent_one.choose_action_plan_index(transformed_state)
                actions_one = agent_one.get_action_from_action_plan(action_plan_index, action_plans)

                actions_two = agent_two.choose_actions(state, [])

                step_count, (game_over, rocket_one_won), state, _, _, reward = env.next_step(actions_one, actions_two)
                if not game_over:
                    reward += 1

                else:
                    if rocket_one_won:
                        reward += 2000
                    else:
                        reward += -1000

                transformed_state, action_plans = agent_one.get_state_info(state)
                transformed_state = np.reshape(transformed_state, newshape=(1, -1))

                R += reward

                agent_one.record_experience(
                    (old_transformed_state, action_plan_index, reward, transformed_state, game_over))
            agent_one.train()

            # rewards.append(R)
            print(i, R)
            f.write(str(i) + " " + str(R) + "\n")
            print(agent_one.history)
            f.write(str(agent_one.history))
            f.write('\n\n')
    agent_one.model.save(os.path.dirname(os.path.realpath(__file__)) + "/model_single_2000")
    f.close()





if __name__ == '__main__':
    print(datetime.now())
    train_single_thread(2000)
    print(datetime.now())