import sys, pygame, sprite_object
from enviroment import Enviroment
from agents import Random_agent, Input_agent
import time
import timeit


visual = True
rocket_one_invulnerable = False
rocket_two_invulnerable = False

env = Enviroment(visual, rocket_one_invulnerable, rocket_two_invulnerable)

agent_one = Input_agent(1)
agent_two = Input_agent(2)



game_over = False
while game_over == False:
    if visual:
        time.sleep(0.05)

    actions_one, actions_two = agent_one.choose_actions()
    # actions_two = agent_two.choose_actions()
    # _, actions_two = env.get_actions_from_keyboard_input()

    step_count, game_over = env.next_step(actions_one, actions_two)


print(step_count)
