import os
from multiprocessing import *
from filelock import FileLock
from datetime import datetime
from enviroment import *
from agents import *

#Experiment 07
def train_single_thread_2_agents(num_episodes, model_one=None, model_two=None, f=None):
    close_file_manually = False
    if f is None:
        close_file_manually = True
        f = open(f"low_sensors_4_actions_2_agents_model_training_{num_episodes}", "w+")
    agent_one = Low_level_sensor_DQAgent(player_number=1, num_inputs=14, num_outputs=6, model=model_one)
    agent_two = Low_level_sensor_DQAgent(player_number=2, num_inputs=14, num_outputs=6, model=model_two)
    env = Enviroment()
    for i in range(num_episodes):
        agent_one.history = [0, 0, 0, 0, 0, 0]
        agent_two.history = [0, 0, 0, 0, 0, 0]
        state = env.reset()
        state_one = agent_one.low_level_state_info(state)
        state_two = agent_two.low_level_state_info(state)
        game_over = False
        R_one = 0
        R_two = 0
        while not game_over:

            old_state_one = state_one
            old_state_two = state_two
            actions_index_one = agent_one.choose_action_index(state_one, train=True)
            actions_one = agent_one.get_simple_actions_from_action_value(actions_index_one)
            actions_one = agent_one.convert_actions(actions_one)

            actions_index_two = agent_two.choose_action_index(state_two, train=True)
            actions_two = agent_two.get_simple_actions_from_action_value(actions_index_two)
            actions_two = agent_two.convert_actions(actions_two)

            step_count, (game_over, rocket_one_won), state, (reward_one, reward_two) = env.next_step(actions_one, actions_two)

            if game_over:
                if rocket_one_won:
                    reward_one += 2000
                    reward_two += -2500
                else:
                    reward_one += -2500
                    reward_two += 2000

            state_one = agent_one.low_level_state_info(state)
            state_two = agent_two.low_level_state_info(state)


            R_one += reward_one
            R_two += reward_two

            agent_one.record_experience((old_state_one, actions_index_one, reward_one, state_one, game_over))
            agent_two.record_experience((old_state_two, actions_index_two, reward_two, state_two, game_over))

        agent_one.train()
        agent_two.train()

        f.write(f"(episode_num, step_count, reward) one: {i} {step_count} {R_one}\n")
        f.write(f"(history: left, right, accelerate, shoot, split_shoot, empty) one: \n {agent_one.history} \n\n")

        f.write(f"(episode_num, reward) two: {i} {R_two}\n")
        f.write(f"(history: left, right, accelerate, shoot, split_shoot, empty) two: \n {agent_two.history} \n\n")


        print(f"{i}, {step_count} {R_one}, {R_two}\n")
        print(f"{agent_one.history}\n{agent_two.history}\n\n")

    model_one = agent_one.model
    model_two = agent_two.model

    if close_file_manually:
        f.close()

    return model_one, model_two

#Experiment 06
def train_single_thread_stable_deffensive_agent(num_episodes, model = None, f = None):
    close_file_manually = False
    if f is None:
        close_file_manually = True
        f = open(f"{num_episodes}_base_action_DQ_stable_deffensive_opponent", "w+")
    agent_one = Low_level_sensor_DQAgent(player_number=1, num_inputs=14, num_outputs=6, model=model)
    agent_two = Stable_defensive_agent(2)
    env = Enviroment()
    train = True
    for i in range(num_episodes):
        agent_one.history = [0, 0, 0, 0, 0, 0]
        state = env.reset()
        state_one = agent_one.low_level_state_info(state)
        game_over = False
        R_one = 0
        #last 5% tries to do the best
        if i > num_episodes * 0.95:
            train = False
        while not game_over:

            old_state_one = state_one
            actions_index_one = agent_one.choose_action_index(state_one, train=train)
            actions_one = agent_one.get_simple_actions_from_action_value(actions_index_one)
            actions_one = agent_one.convert_actions(actions_one)

            actions_two = agent_two.choose_actions(state)

            step_count, (game_over, rocket_one_won), state, (reward_one, reward_two) = env.next_step(actions_one, actions_two)


            if game_over:
                if rocket_one_won:
                    reward_one += 2000
                else:
                    reward_one += -1000

            state_one = agent_one.low_level_state_info(state)


            R_one += reward_one

            agent_one.record_experience((old_state_one, actions_index_one, reward_one, state_one, game_over))

        agent_one.train()

        f.write(f"(episode_num, step_count, reward) one: {i} {step_count} {R_one}\n")
        f.write(f"(history: left, right, accelerate, shoot, split_shoot, empty) one: \n {agent_one.history} \n\n")

        if i % 500 == 0:
            tf.keras.models.save_model(agent_one.model, '/content/drive/My Drive/10000_LL_DQ_stable_defensive_opponent_model')


        print(f"{i}, {step_count} {R_one}\n")
        print(f"{agent_one.history}\n\n")

    model_one = agent_one.model

    if close_file_manually:
        f.close()

    return model_one

if __name__ == "__main__":
    batch = 500
    for i in range(40):
        try:
            model = tf.keras.models.load_model("/content/drive/My Drive/20000_LL_DQ_stable_defensive_opponent_model.txt")
            print("model loading succesful")
        #model_two = tf.keras.models.load_model("/content/drive/My Drive/20000_LL_DQ_2_players_model_two.txt")
        except:
            model = None
            print("failed model loading")
        model = train_single_thread_stable_deffensive_agent(batch, model)
        tf.keras.models.save_model(model, '/content/drive/My Drive/20000_LL_DQ_stable_defensive_opponent_model.txt')
        #tf.keras.models.save_model(model_two, '/content/drive/My Drive/20000_LL_DQ_2_players_model_two.txt')
        print(f"{i*batch} games played")