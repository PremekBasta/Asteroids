import sys, pygame, sprite_object
from enviroment import Enviroment
from agents import *
import time
import timeit


visual = True
rocket_one_invulnerable = False
rocket_two_invulnerable = False

env = Enviroment(visual, rocket_one_invulnerable, rocket_two_invulnerable)
state = env.reset()

# agent_one = Input_agent(env.screen, 1)
agent_one = Stable_defensive_agent(env.screen, 1)
# agent_two = Input_agent(env.screen, 2)
agent_two = Stable_defensive_agent(env.screen, 2)


game_over = False
longest_step = 0
shortest_step = 1
incremental_time = 0

while game_over == False:

    if visual:
        time.sleep(0.010)

    # actions_one, actions_two = agent_one.choose_actions(state)
    # actions_one, _ = agent_one.choose_actions(state)
    # _, actions_two = agent_two.choose_actions(state)
    actions_one = agent_one.choose_actions(state)
    actions_two = agent_two.choose_actions(state)
    # _, actions_two = env.get_actions_from_keyboard_input()

    # start = time.time()
    step_count, game_over, state = env.next_step(actions_one, actions_two)

    # end = time.time()
    # if end - start < shortest_step:
    #     shortest_step = end - start
    # if end - start > longest_step:
    #     longest_step = end - start
    # incremental_time = incremental_time + end - start


print(step_count)
# print(f"longest tick: {longest_step}")
# print(f"shortest tick: {shortest_step}")
# print(f"average tick: {incremental_time / step_count}")