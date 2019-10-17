import pygame
import math

class SpaceObjectDTO():
    def __init__(self, rect, speedx, speedy, width, height, angle):
        self.collision_rect = pygame.Rect(rect)
        self.speedx = int(speedx)
        self.speedy = int(speedy)
        self.width = width
        self.height = height
        self.angle = angle

    def move(self):
        self.collision_rect.centerx = (self.collision_rect.centerx + self.speedx) % self.width
        self.collision_rect.centery = (self.collision_rect.centery + self.speedy) % self.height

    def reverse_move(self, steps_count):
        self.collision_rect.centerx = (self.collision_rect.centerx - steps_count * self.speedx) % self.width
        self.collision_rect.centery = (self.collision_rect.centery - steps_count * self.speedy) % self.height
