from draw_module import draw_module
from enviroment import Enviroment
from agents import *
from gp import return_individual, return_E01Function, return_E02Function, return_E03Function
import time
import numpy as np
import argparse
import sys


def play_games(num_games, agent_one, agent_two, draw_module = None):
    env = Enviroment(draw_module)
    RocketOne_wins = 0
    RocketTwo_wins = 0
    total_time = 0
    total_steps = 0

    for i in range(num_games):
        game_over = False
        state = env.reset()
        start = time.time()
        while game_over == False:
            if agent_one.input and agent_two.input:
                actions_one, actions_two = agent_one.choose_actions(state)
            elif agent_one.input:
                actions_one, _ = agent_one.choose_actions(state)
                actions_two = agent_two.choose_actions(state)
            elif agent_two.input:
                actions_one = agent_one.choose_actions(state)
                _,actions_two = agent_two.choose_actions(state)
            else:
                actions_one = agent_one.choose_actions(state)
                actions_two = agent_two.choose_actions(state)

            pygame.event.clear()


            step_count, (game_over, rocket_one_won), state, _ = env.next_step(actions_one, actions_two)

        end = time.time()
        total_time = total_time + (end - start)

        print(f"avg_time: {total_time / (i+1)}")
        total_steps = total_steps + step_count
        print(f"avg_steps_count: {total_steps / (i+1)}")


        if rocket_one_won:
            RocketOne_wins = RocketOne_wins + 1
        else:
            RocketTwo_wins = RocketTwo_wins + 1

        print(f"Rocket one wins: {RocketOne_wins}")
        print(f"Rocket two wins: {RocketTwo_wins}")

def assign_agent(player_number, chosen_agent, draw_module):
    if chosen_agent is None or chosen_agent.upper() == AgentsEnums.StableDefense.value:
        return Stable_defensive_agent(player_number)
    if chosen_agent.upper() == AgentsEnums.Input.value:
        return Input_agent(draw_module.screen, player_number)
    if chosen_agent.upper() == AgentsEnums.Evase.value:
        return Evasion_agent(player_number)
    if chosen_agent.upper() == AgentsEnums.Experiment01.value:
        return Genetic_agent(player_number, return_E01Function())
    if chosen_agent.upper() == AgentsEnums.Experiment02.value:
        return Genetic_agent(player_number, return_E02Function())
    if chosen_agent.upper() == AgentsEnums.Experiment03.value:
        return Genetic_agent(player_number, return_E03Function())

    if chosen_agent.upper() == AgentsEnums.Experiment04.value:
        model = tf.keras.models.load_model("HL_DQ/DQ_stable_deffensive_opponent_model_auto_save")
        return DQAgent(player_number, num_inputs=5, num_outputs=4, model = model)
    if chosen_agent.upper() == AgentsEnums.Experiment05.value:
        model = tf.keras.models.load_model("HL_DQ/DQ_stable_deffensive_opponent_extended_model_auto_save")
        return DQAgent(player_number, num_inputs=9, num_outputs=4, model = model)

    if chosen_agent.upper() == AgentsEnums.Experiment06.value:
        model = tf.keras.models.load_model("LL_DQ_stable_deffensive_opponent/10000_base_action_DQ_stable_deffensive_opponent_added_dense_layer_model_1")
        return Low_level_sensor_DQAgent(player_number, num_inputs=14, num_outputs=6, model = model)
    if chosen_agent.upper() == AgentsEnums.Experiment07.value:
        if player_number == 1:
            model = tf.keras.models.load_model(
                "LL_DQ_2_players/20000_LL_DQ_2_players_model_one")
        elif player_number == 2:
            model = tf.keras.models.load_model(
                "LL_DQ_2_players/20000_LL_DQ_2_players_model_two")
        return Low_level_sensor_DQAgent(player_number, num_inputs=14, num_outputs=6, model=model)

class AgentsEnums(Enum):
    StableDefense = "SD"
    Input = "IN"
    Evase = "EV"
    Experiment01 = "E01"
    Experiment02 = "E02"
    Experiment03 = "E03"
    Experiment04 = "E04"
    Experiment05 = "E05"
    Experiment06 = "E06"
    Experiment07 = "E07"


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='''Starts game of asteroids. Set players\' agents. Valid options are: 
    \"SD\" - Stable Defense agent\n
    \"IN\" - Keyboard controlled agent\n
    \"EV\" - Evasion agent\n
    \"E0X\" - Multiple agents choice from results of experiments, replace \"X\" with corresponding number 1-7''')
    parser.add_argument('-dv', type=bool, default=False, help="disable visual game mode", nargs='?')
    parser.add_argument('-a1', type=str, default="SD", help="Agent choosen for player 1")
    parser.add_argument('-a2', type=str, default="SD", help="Agent choosen for player 2")
    parser.add_argument('-ng', type=int, default=10, help="Number of games played")

    args = parser.parse_args()

    if(str(args.a1).upper() == "IN" and str(args.a2).upper() == "IN"):
        sys.exit("Both players cannot use input agents.")

    if((str(args.a1).upper() == "IN" or str(args.a2).upper()) and (args.dv is None or args.dv == True)):
        sys.exit("Invalid combination of disabled visual mode and input agent.")

    if args.dv == False:
        draw_module = draw_module()
    else:
        draw_module = None

    agent_one = assign_agent(1, args.a1, draw_module)
    agent_two = assign_agent(2, args.a2, draw_module)


    play_games(args.ng, agent_one, agent_two, draw_module)

