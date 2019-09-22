import sys, pygame, sprite_object
from enviroment import Enviroment
import time
import timeit


env = Enviroment(True)
while True:
    time.sleep(0.05)
    env.next_step(env.get_actions_from_keyboard_input())
