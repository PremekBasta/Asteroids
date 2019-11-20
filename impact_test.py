from dto import SpaceObjectDTO, collides, copy_object
import constants
import time
import numpy as np
import random
import agents


random.seed(100)

asteroids = []
for i in range(16):
    radius = random.randint(3,10)
    centerx = random.randint(0, constants.SCREEN_WIDTH)
    centery = random.randint(0, constants.SCREEN_HEIGHT)
    speedx = random.randint(-4,5)
    speedy = random.randint(-4,5)
    angle = 0
    size_index = 1
    player = 0
    life_count = 100
    ast = SpaceObjectDTO(radius, centerx, centery, speedx, speedy, angle, size_index, player, life_count)
    asteroids.append(ast)

    radius = random.randint(3,10)
    centerx = random.randint(0, constants.SCREEN_WIDTH)
    centery = random.randint(0, constants.SCREEN_HEIGHT)
    speedx = random.randint(-4,5)
    speedy = random.randint(-4,5)
    angle = 0
    size_index = 1
    player = 0
    life_count = 100

rocket_radius = 10
rocket = SpaceObjectDTO(rocket_radius, centerx, centery, speedx, speedy, angle, size_index, player, life_count)

bullets = []
for i in range(3):
    radius = random.randint(3,10)
    centerx = random.randint(0, constants.SCREEN_WIDTH)
    centery = random.randint(0, constants.SCREEN_HEIGHT)
    speedx = random.randint(-4,5)
    speedy = random.randint(-4,5)
    angle = random.randint(0,30)
    size_index = 1
    player = 0
    life_count = 50
    bullet = SpaceObjectDTO(radius, centerx, centery, speedx, speedy, angle, size_index, player, life_count)
    bullets.append(bullet)

agent = agents.Stable_defensive_agent(None, 1)


# start = time.time()
# for i in range(1000):
#     agent.first_impact_neutral_asteroid(rocket, asteroids, bullets)
# end = time.time()
# print(end - start)



total_start = time.time()
for i in range(3000):
    agent.first_impact_neutral_asteroid_numpy(rocket, asteroids, bullets)


print(time.time() - total_start)