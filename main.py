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



RocketOne_wins = 0
RocketTwo_wins = 0
total_steps = 0

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
    step_count, (game_over, rocketOne_health, rocketTwo_health), state = env.next_step(actions_one, actions_two)
if rocketOne_health <= 0:
    RocketOne_wins = RocketOne_wins + 1
else:
    RocketTwo_wins = RocketTwo_wins + 1
total_steps = total_steps + step_count

print(step_count)

# print(f"average steps count: {total_steps / (i + 1)}")
print(f"Rocket one wins: {RocketOne_wins}")
print(f"Rocket two wins: {RocketTwo_wins}")


# print(f"longest tick: {longest_step}")
# print(f"shortest tick: {shortest_step}")
# print(f"average tick: {incremental_time / step_count}")