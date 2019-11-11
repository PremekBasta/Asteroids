
from enviroment import Enviroment
from agents import *
import time
import timeit


visual = False
rocket_one_invulnerable = False
rocket_two_invulnerable = False

env = Enviroment(visual, rocket_one_invulnerable, rocket_two_invulnerable)
clock = pygame.time.Clock()
state = env.reset()

agent_one = Stable_defensive_agent(env.screen, 1)
# agent_one = Stable_defensive_agent(env.screen, 1)
agent_two = Stable_defensive_agent(env.screen, 2)
# agent_two = Stable_defensive_agent(env.screen, 2)


game_over = False
longest_step = 0
shortest_step = 1
incremental_time = 0



RocketOne_wins = 0
RocketTwo_wins = 0
total_steps = 0
total_time = 0

for i in range(2):
    game_over = False
    state = env.reset()
    start = time.time()
    while game_over == False:
        if visual:
            # time.sleep(0.010)
            clock.tick(30)

        # actions_one, actions_two = agent_one.choose_actions(state)
        # actions_one, _ = agent_one.choose_actions(state)

        # _, actions_two = agent_two.choose_actions(state)

        # events = pygame.event.get(pygame.KEYDOWN)
        # all_keys = pygame.key.get_pressed()
        actions_one = agent_one.choose_actions(state)
        actions_two = agent_two.choose_actions(state)
        # _, actions_two = env.get_actions_from_keyboard_input()

        # start = time.time()
        step_count, (game_over, rocketOne_health, rocketTwo_health), state = env.next_step(actions_one, actions_two)
    end = time.time()
    total_time = total_time + (end - start)
    print(f"avg_time: {total_time / (i+1)}")
    total_steps = total_steps + step_count
    print(f"avg_steps_count: {total_steps / (i+1)}")
    if rocketOne_health <= 0:
        RocketTwo_wins = RocketTwo_wins + 1
    else:
        RocketOne_wins = RocketOne_wins + 1





    print(step_count)

    # print(f"average steps count: {total_steps / (i + 1)}")
    print(f"Rocket one wins: {RocketOne_wins}")
    print(f"Rocket two wins: {RocketTwo_wins}")


# print(f"longest tick: {longest_step}")
# print(f"shortest tick: {shortest_step}")
# print(f"average tick: {incremental_time / step_count}")