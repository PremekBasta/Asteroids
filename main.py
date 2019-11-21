
from enviroment import Enviroment
from agents import *
import time
import timeit
import numpy as np


visual = False
rocket_one_invulnerable = False
rocket_two_invulnerable = False

env = Enviroment(visual, rocket_one_invulnerable, rocket_two_invulnerable)
clock = pygame.time.Clock()
state = env.reset()

agent_one = Attacking_agent(env.screen, 1)
# agent_one = Stable_defensive_agent(env.screen, 1)
agent_two = Attacking_agent(env.screen, 2)
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
        if visual:
            # time.sleep(0.010)
            clock.tick(60)

        # actions_one, actions_two = agent_one.choose_actions(state)
        # actions_one, _ = agent_one.choose_actions(state)

        # _, actions_two = agent_two.choose_actions(state)

        # events = pygame.event.get(pygame.KEYDOWN)
        # all_keys = pygame.key.get_pressed()
        actions_one = agent_one.choose_actions(state, agent_two_actions)
        actions_two = agent_two.choose_actions(state, agent_one_actions)
        # _, actions_two = env.get_actions_from_keyboard_input()

        # start = time.time()
        step_count, (game_over, rocketOne_health, rocketTwo_health), state, agent_one_actions, agent_two_actions = env.next_step(actions_one, actions_two)
    end = time.time()
    total_time = total_time + (end - start)
    print(f"active steps: {agent_one.active_steps}")
    agent_one.active_steps = 0

    print(f"inactive steps: {agent_one.inactive_steps}")
    agent_one.inactive_steps = 0
    print(f"avg_time: {total_time / (i+1)}")
    total_steps = total_steps + step_count
    print(f"avg_steps_count: {total_steps / (i+1)}")
    #
    # print(f"player one python: {agent_one.python_time}")
    # print(f"player one numpy: {agent_one.numpy_time}")
    # print(f"player one asteroids max count: {np.max(agent_one.asteroids_arr)}")
    # print(f"player one asteroids average count: {np.average(agent_one.asteroids_arr)}")
    # print(f"player one asteroids median count: {np.median(agent_one.asteroids_arr)}")
    # print(f"player one bullets average count: {np.average(agent_one.bullets_arr)}")
    # print(f"player one bullets median count: {np.median(agent_one.bullets_arr)}")
    #
    # print(">>>")
    #
    # print(f"player two python: {agent_two.python_time}")
    # print(f"player two numpy: {agent_two.numpy_time}")
    # print(f"player two asteroids max count: {np.max(agent_two.asteroids_arr)}")
    # print(f"player two asteroids average count: {np.average(agent_two.asteroids_arr)}")
    # print(f"player two asteroids median count: {np.median(agent_two.asteroids_arr)}")
    # print(f"player two bullets average count: {np.average(agent_two.bullets_arr)}")
    # print(f"player two bullets median count: {np.median(agent_two.bullets_arr)}")

    if rocketOne_health <= 0:
        RocketTwo_wins = RocketTwo_wins + 1
    else:
        RocketOne_wins = RocketOne_wins + 1





    # print(step_count)
    #
    # # print(f"average steps count: {total_steps / (i + 1)}")
    print(f"Rocket one wins: {RocketOne_wins}")
    print(f"Rocket two wins: {RocketTwo_wins}")


# print(f"longest tick: {longest_step}")
# print(f"shortest tick: {shortest_step}")
# print(f"average tick: {incremental_time / step_count}")