from typing import OrderedDict

import pygame, math
from constants import *
import numba

spec = OrderedDict()
spec['radius'] = numba.int32
spec['centerx'] = numba.int32
spec['centery'] = numba.int32
spec['speedx'] = numba.int32
spec['speedy'] = numba.int32
spec['angle'] = numba.int32
spec['size_index'] = numba.int32
spec['player'] = numba.int32
spec['life_count'] = numba.int32

# @numba.jitclass(spec)
class SpaceObjectDTO():
    def __init__(self, radius, centerx, centery, speedx, speedy, angle, size_index = 0, player = 1, life_count = 0):
        self.radius = radius
        self.centerx = centerx
        self.centery = centery
        self.speedx = int(speedx)
        self.speedy = int(speedy)
        self.angle = angle
        self.size_index = size_index
        self.player = player
        self.life_count = life_count


    def move(self, steps_count = 1):
        self.centerx = int((self.centerx + steps_count * self.speedx) % SCREEN_WIDTH)
        self.centery = int((self.centery + steps_count * self.speedy) % SCREEN_HEIGHT)
        self.life_count = self.life_count - steps_count * 1

    def reverse_move(self, steps_count = 1):
        self.centerx = int((self.centerx - steps_count * self.speedx) % SCREEN_WIDTH)
        self.centery = int((self.centery - steps_count * self.speedy) % SCREEN_HEIGHT)
        self.life_count = self.life_count + steps_count

    def is_alive(self):
        return self.life_count > 0

    def rotate_left(self, steps_count = 1):
        self.angle = self.angle +  steps_count * ROCKET_ANGLE_ROTATION + 360
        self.angle = self.angle % 360

    def rotate_right(self, steps_count = 1):
        self.angle = self.angle - steps_count * ROCKET_ANGLE_ROTATION
        self.angle = self.angle % 360

    def accelerate(self):
        self.speedx = self.speedx - int(math.sin(self.angle / 180 * math.pi) * 20 / 2)
        self.speedy = self.speedy - int(math.cos(self.angle / 180 * math.pi) * 20 / 2)
        if math.sqrt(math.pow(self.speedx, 2) + math.pow(self.speedy, 2)) > MAX_ROCKET_SPEED:
            minusx = False
            minusy = False
            if self.speedx < 0:
                minusx = True
            if self.speedy < 0:
                minusy = True

            if self.speedy == 0:
                self.speedx = int(self.speedx * math.sqrt(math.pow(MAX_ROCKET_SPEED, 2) / math.pow(self.speedx, 2)))
            else:
                ratio = self.speedx / self.speedy
                self.speedy = int(math.sqrt(math.pow(MAX_ROCKET_SPEED, 2) / (math.pow(ratio, 2) + 1)))
                self.speedx = int(math.sqrt(math.pow(MAX_ROCKET_SPEED, 2) - math.pow(self.speedy, 2)))

            if minusx:
                self.speedx = -self.speedx
            if minusy:
                self.speedy = -self.speedy


    def collides(self, object):
        return math.sqrt(math.pow(self.centerx - object.centerx, 2) + math.pow(self.centery - object.centery, 2)) < (self.radius + object.radius)


def collides(objectA, objectB):
    return math.sqrt(math.pow(objectA.centerx - objectB.centerx, 2) + math.pow(objectA.centery - objectB.centery, 2)) < (
                objectA.radius + objectB.radius)

# @numba.jit(nopython=True)
def collides_numba(objectA_centerx, objectA_centery, objectB_centerx, objectB_centery, objectA_radius, objectB_radius):
    return math.sqrt(
        math.pow(objectA_centerx - objectB_centerx, 2) + math.pow(objectA_centery - objectB_centery, 2)) < (
                   objectA_radius + objectB_radius)