import pygame, math
from constants import *


class SpaceObjectDTO():
    def __init__(self, rect, speedx, speedy, angle, size_index = 0, player = 1, life_count = 0):
        self.collision_rect = pygame.Rect(rect)
        self.speedx = int(speedx)
        self.speedy = int(speedy)
        self.angle = angle
        self.size_index = size_index
        self.player = player
        self.life_count = life_count

    def move(self, steps_count = 1):
        self.collision_rect.centerx = (self.collision_rect.centerx + steps_count * self.speedx) % SCREEN_WIDTH
        self.collision_rect.centery = (self.collision_rect.centery + steps_count * self.speedy) % SCREEN_HEIGHT
        self.life_count = self.life_count - steps_count * 1

    def reverse_move(self, steps_count = 1):
        self.collision_rect.centerx = (self.collision_rect.centerx - steps_count * self.speedx) % SCREEN_WIDTH
        self.collision_rect.centery = (self.collision_rect.centery - steps_count * self.speedy) % SCREEN_HEIGHT
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