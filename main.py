from draw_module import draw_module
from enviroment import Enviroment
from agents import *
from gp import return_individual
import time


def play_games(num_games, agent_one, agent_two, draw_module = None):
    env = Enviroment(draw_module)
    state = env.reset()

    game_over = False
    RocketOne_wins = 0
    RocketTwo_wins = 0
    total_time = 0
    total_steps = 0

    for i in range(num_games):
        game_over = False
        state = env.reset()
        agent_one_actions = []
        agent_two_actions = []
        start = time.time()
        while game_over == False:
            actions_two = agent_two.choose_actions(state, agent_one_actions)
            actions_one = agent_one.choose_actions(state, agent_two_actions)

            step_count, (game_over, rocket_one_won), state, agent_one_actions, agent_two_actions, _ = env.next_step(actions_one, actions_two)

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


if __name__ == "__main__":

    play_games(10, Evasion_agent(1), Evasion_agent(2))


    draw_module = draw_module()
    draw_module = None

    env = Enviroment(draw_module)
    state = env.reset()

    #agent_one = Genetic_agent(1, return_individual())
    agent_one = Evasion_agent(1, draw_module)
    agent_two = Stable_defensive_agent(2)
    agent_two = Evasion_agent(2, draw_module)
    # agent_two = Stable_defensive_agent(env.screen, 2)

    game_over = False
    longest_step = 0
    shortest_step = 1
    incremental_time = 0

    RocketOne_wins = 0
    RocketTwo_wins = 0
    total_steps = 0
    total_time = 0

    for i in range(1000):
        game_over = False
        state = env.reset()
        agent_one_actions = []
        agent_two_actions = []
        agent_one.finished_plan = True
        agent_two.finished_plan = True
        start = time.time()
        while game_over == False:
            # if visual:
            #     clock.tick(60)

            # actions_one, actions_two = agent_one.choose_actions(state)
            # actions_one, _ = agent_one.choose_actions(state)

            # _, actions_two = agent_two.choose_actions(state)

            # events = pygame.event.get(pygame.KEYDOWN)
            # all_keys = pygame.key.get_pressed()
            actions_two = agent_two.choose_actions(state, agent_one_actions)

            actions_one = agent_one.choose_actions(state, agent_two_actions)

            #
            # # _, actions_two = env.get_actions_from_keyboard_input()
            #
            # # start = time.time()
            step_count, (game_over, rocket_one_won), state, agent_one_actions, agent_two_actions, _ = env.next_step(actions_one, actions_two)

        end = time.time()
        total_time = total_time + (end - start)
        # print(f"active steps: {agent_one.active_steps}")
        agent_one.active_steps = 0

        # print(f"inactive steps: {agent_one.inactive_steps}")
        agent_one.inactive_steps = 0
        print(f"avg_time: {total_time / (i+1)}")
        total_steps = total_steps + step_count
        print(f"avg_steps_count: {total_steps / (i+1)}")
        print(f"attack_count: {agent_one.attack_count}")
        agent_one.attack_count = 0
        print(f"deffense_count: {agent_one.defense_count}")
        agent_one.defense_count = 0
        print(f"evasion_count: {agent_one.evasion_count}")
        agent_one.evasion_count = 0
        print(f"Stop count: {agent_one.stop_count}")
        agent_one.stop_count = 0


        if rocket_one_won:
            RocketOne_wins = RocketOne_wins + 1
        else:
            RocketTwo_wins = RocketTwo_wins + 1

        print(f"Rocket one wins: {RocketOne_wins}")
        print(f"Rocket two wins: {RocketTwo_wins}")




    # print(f"longest tick: {longest_step}")
    # print(f"shortest tick: {shortest_step}")
    # print(f"average tick: {incremental_time / step_count}")