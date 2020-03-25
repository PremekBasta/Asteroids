import pygame
from constants import *

class draw_module(object):
    rocket_rotation_images = [
        [pygame.image.load('images/rocket_one_0.png'), pygame.image.load('images/rocket_one_12.png'),
         pygame.image.load('images/rocket_one_24.png'), pygame.image.load('images/rocket_one_36.png'),
         pygame.image.load('images/rocket_one_48.png'), pygame.image.load('images/rocket_one_60.png'),
         pygame.image.load('images/rocket_one_72.png'), pygame.image.load('images/rocket_one_84.png'),
         pygame.image.load('images/rocket_one_96.png'), pygame.image.load('images/rocket_one_108.png'),
         pygame.image.load('images/rocket_one_120.png'), pygame.image.load('images/rocket_one_132.png'),
         pygame.image.load('images/rocket_one_144.png'), pygame.image.load('images/rocket_one_156.png'),
         pygame.image.load('images/rocket_one_168.png'), pygame.image.load('images/rocket_one_180.png'),
         pygame.image.load('images/rocket_one_192.png'), pygame.image.load('images/rocket_one_204.png'),
         pygame.image.load('images/rocket_one_216.png'), pygame.image.load('images/rocket_one_228.png'),
         pygame.image.load('images/rocket_one_240.png'), pygame.image.load('images/rocket_one_252.png'),
         pygame.image.load('images/rocket_one_264.png'), pygame.image.load('images/rocket_one_276.png'),
         pygame.image.load('images/rocket_one_288.png'), pygame.image.load('images/rocket_one_300.png'),
         pygame.image.load('images/rocket_one_312.png'), pygame.image.load('images/rocket_one_324.png'),
         pygame.image.load('images/rocket_one_336.png'), pygame.image.load('images/rocket_one_348.png')],
        [pygame.image.load('images/rocket_two_0.png'), pygame.image.load('images/rocket_two_12.png'),
         pygame.image.load('images/rocket_two_24.png'), pygame.image.load('images/rocket_two_36.png'),
         pygame.image.load('images/rocket_two_48.png'), pygame.image.load('images/rocket_two_60.png'),
         pygame.image.load('images/rocket_two_72.png'), pygame.image.load('images/rocket_two_84.png'),
         pygame.image.load('images/rocket_two_96.png'), pygame.image.load('images/rocket_two_108.png'),
         pygame.image.load('images/rocket_two_120.png'), pygame.image.load('images/rocket_two_132.png'),
         pygame.image.load('images/rocket_two_144.png'), pygame.image.load('images/rocket_two_156.png'),
         pygame.image.load('images/rocket_two_168.png'), pygame.image.load('images/rocket_two_180.png'),
         pygame.image.load('images/rocket_two_192.png'), pygame.image.load('images/rocket_two_204.png'),
         pygame.image.load('images/rocket_two_216.png'), pygame.image.load('images/rocket_two_228.png'),
         pygame.image.load('images/rocket_two_240.png'), pygame.image.load('images/rocket_two_252.png'),
         pygame.image.load('images/rocket_two_264.png'), pygame.image.load('images/rocket_two_276.png'),
         pygame.image.load('images/rocket_two_288.png'), pygame.image.load('images/rocket_two_300.png'),
         pygame.image.load('images/rocket_two_312.png'), pygame.image.load('images/rocket_two_324.png'),
         pygame.image.load('images/rocket_two_336.png'), pygame.image.load('images/rocket_two_348.png')]]
    bullet_angle_images = [
        [[pygame.image.load('images/bullet_one_0.png'), pygame.image.load('images/bullet_one_12.png'),
          pygame.image.load('images/bullet_one_24.png'), pygame.image.load('images/bullet_one_36.png'),
          pygame.image.load('images/bullet_one_48.png'), pygame.image.load('images/bullet_one_60.png'),
          pygame.image.load('images/bullet_one_72.png'), pygame.image.load('images/bullet_one_84.png'),
          pygame.image.load('images/bullet_one_96.png'), pygame.image.load('images/bullet_one_108.png'),
          pygame.image.load('images/bullet_one_120.png'), pygame.image.load('images/bullet_one_132.png'),
          pygame.image.load('images/bullet_one_144.png'), pygame.image.load('images/bullet_one_156.png'),
          pygame.image.load('images/bullet_one_168.png'), pygame.image.load('images/bullet_one_180.png'),
          pygame.image.load('images/bullet_one_192.png'), pygame.image.load('images/bullet_one_204.png'),
          pygame.image.load('images/bullet_one_216.png'), pygame.image.load('images/bullet_one_228.png'),
          pygame.image.load('images/bullet_one_240.png'), pygame.image.load('images/bullet_one_252.png'),
          pygame.image.load('images/bullet_one_264.png'), pygame.image.load('images/bullet_one_276.png'),
          pygame.image.load('images/bullet_one_288.png'), pygame.image.load('images/bullet_one_300.png'),
          pygame.image.load('images/bullet_one_312.png'), pygame.image.load('images/bullet_one_324.png'),
          pygame.image.load('images/bullet_one_336.png'), pygame.image.load('images/bullet_one_348.png')],
         [pygame.image.load('images/bullet_two_0.png'), pygame.image.load('images/bullet_two_12.png'),
          pygame.image.load('images/bullet_two_24.png'), pygame.image.load('images/bullet_two_36.png'),
          pygame.image.load('images/bullet_two_48.png'), pygame.image.load('images/bullet_two_60.png'),
          pygame.image.load('images/bullet_two_72.png'), pygame.image.load('images/bullet_two_84.png'),
          pygame.image.load('images/bullet_two_96.png'), pygame.image.load('images/bullet_two_108.png'),
          pygame.image.load('images/bullet_two_120.png'), pygame.image.load('images/bullet_two_132.png'),
          pygame.image.load('images/bullet_two_144.png'), pygame.image.load('images/bullet_two_156.png'),
          pygame.image.load('images/bullet_two_168.png'), pygame.image.load('images/bullet_two_180.png'),
          pygame.image.load('images/bullet_two_192.png'), pygame.image.load('images/bullet_two_204.png'),
          pygame.image.load('images/bullet_two_216.png'), pygame.image.load('images/bullet_two_228.png'),
          pygame.image.load('images/bullet_two_240.png'), pygame.image.load('images/bullet_two_252.png'),
          pygame.image.load('images/bullet_two_264.png'), pygame.image.load('images/bullet_two_276.png'),
          pygame.image.load('images/bullet_two_288.png'), pygame.image.load('images/bullet_two_300.png'),
          pygame.image.load('images/bullet_two_312.png'), pygame.image.load('images/bullet_two_324.png'),
          pygame.image.load('images/bullet_two_336.png'), pygame.image.load('images/bullet_two_348.png')]],

        [[pygame.image.load('images/bullet_one_split_0.bmp'), pygame.image.load('images/bullet_one_split_12.bmp'),
          pygame.image.load('images/bullet_one_split_24.bmp'), pygame.image.load('images/bullet_one_split_36.bmp'),
          pygame.image.load('images/bullet_one_split_48.bmp'), pygame.image.load('images/bullet_one_split_60.bmp'),
          pygame.image.load('images/bullet_one_split_72.bmp'), pygame.image.load('images/bullet_one_split_84.bmp'),
          pygame.image.load('images/bullet_one_split_96.bmp'), pygame.image.load('images/bullet_one_split_108.bmp'),
          pygame.image.load('images/bullet_one_split_120.bmp'), pygame.image.load('images/bullet_one_split_132.bmp'),
          pygame.image.load('images/bullet_one_split_144.bmp'), pygame.image.load('images/bullet_one_split_156.bmp'),
          pygame.image.load('images/bullet_one_split_168.bmp'), pygame.image.load('images/bullet_one_split_180.bmp'),
          pygame.image.load('images/bullet_one_split_192.bmp'), pygame.image.load('images/bullet_one_split_204.bmp'),
          pygame.image.load('images/bullet_one_split_216.bmp'), pygame.image.load('images/bullet_one_split_228.bmp'),
          pygame.image.load('images/bullet_one_split_240.bmp'), pygame.image.load('images/bullet_one_split_252.bmp'),
          pygame.image.load('images/bullet_one_split_264.bmp'), pygame.image.load('images/bullet_one_split_276.bmp'),
          pygame.image.load('images/bullet_one_split_288.bmp'), pygame.image.load('images/bullet_one_split_300.bmp'),
          pygame.image.load('images/bullet_one_split_312.bmp'), pygame.image.load('images/bullet_one_split_324.bmp'),
          pygame.image.load('images/bullet_one_split_336.bmp'), pygame.image.load('images/bullet_one_split_348.bmp')],
         [pygame.image.load('images/bullet_two_split_0.bmp'), pygame.image.load('images/bullet_two_split_12.bmp'),
          pygame.image.load('images/bullet_two_split_24.bmp'), pygame.image.load('images/bullet_two_split_36.bmp'),
          pygame.image.load('images/bullet_two_split_48.bmp'), pygame.image.load('images/bullet_two_split_60.bmp'),
          pygame.image.load('images/bullet_two_split_72.bmp'), pygame.image.load('images/bullet_two_split_84.bmp'),
          pygame.image.load('images/bullet_two_split_96.bmp'), pygame.image.load('images/bullet_two_split_108.bmp'),
          pygame.image.load('images/bullet_two_split_120.bmp'), pygame.image.load('images/bullet_two_split_132.bmp'),
          pygame.image.load('images/bullet_two_split_144.bmp'), pygame.image.load('images/bullet_two_split_156.bmp'),
          pygame.image.load('images/bullet_two_split_168.bmp'), pygame.image.load('images/bullet_two_split_180.bmp'),
          pygame.image.load('images/bullet_two_split_192.bmp'), pygame.image.load('images/bullet_two_split_204.bmp'),
          pygame.image.load('images/bullet_two_split_216.bmp'), pygame.image.load('images/bullet_two_split_228.bmp'),
          pygame.image.load('images/bullet_two_split_240.bmp'), pygame.image.load('images/bullet_two_split_252.bmp'),
          pygame.image.load('images/bullet_two_split_264.bmp'), pygame.image.load('images/bullet_two_split_276.bmp'),
          pygame.image.load('images/bullet_two_split_288.bmp'), pygame.image.load('images/bullet_two_split_300.bmp'),
          pygame.image.load('images/bullet_two_split_312.bmp'), pygame.image.load('images/bullet_two_split_324.bmp'),
          pygame.image.load('images/bullet_two_split_336.bmp'), pygame.image.load('images/bullet_two_split_348.bmp')]]]
    asteroid_images = [
        [
            [pygame.image.load('images/asteroid_one_50x50_00.bmp'),
             pygame.image.load('images/asteroid_one_50x50_01.bmp'),
             pygame.image.load('images/asteroid_one_50x50_02.bmp')],

            [pygame.image.load('images/asteroid_one_71x71_00.bmp'),
             pygame.image.load('images/asteroid_one_71x71_01.bmp'),
             pygame.image.load('images/asteroid_one_71x71_02.bmp')]],

        [
            [pygame.image.load('images/asteroid_two_50x50_00.bmp'),
             pygame.image.load('images/asteroid_two_50x50_01.bmp'),
             pygame.image.load('images/asteroid_two_50x50_02.bmp')],

            [pygame.image.load('images/asteroid_two_71x71_00.bmp'),
             pygame.image.load('images/asteroid_two_71x71_01.bmp'),
             pygame.image.load('images/asteroid_two_71x71_02.bmp')]],

        [
            [pygame.image.load('images/asteroid_40x40_00.bmp'),
             pygame.image.load('images/asteroid_40x40_01.bmp'),
             pygame.image.load('images/asteroid_40x40_02.bmp')],

            [pygame.image.load('images/asteroid_71x71_00.bmp'),
             pygame.image.load('images/asteroid_71x71_01.bmp'),
             pygame.image.load('images/asteroid_71x71_02.bmp')],

            [pygame.image.load('images/asteroid_110x110_00.bmp'),
             pygame.image.load('images/asteroid_110x110_01.bmp'),
             pygame.image.load('images/asteroid_110x110_02.bmp')]]
        ]

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.init()
        self.clock = pygame.time.Clock()
        for i in range(2):
            for image in self.rocket_rotation_images[i]:
                image.set_colorkey((0,0,0))

        for i in range(3):
            for images in self.asteroid_images[i]:
                for image in images:
                    image.set_colorkey((0, 0, 0, 0))

        for split_set in self.bullet_angle_images:
            for player_set in split_set:
                for image in player_set:
                    image.set_colorkey(COLOR_BLACK)


    def clear_display(self):
        self.clock.tick(FRAME_RATE)
        self.screen.fill(COLOR_BLACK)

    def draw_rocket(self, rocket):
        pygame.draw.rect(self.screen, rocket.health_bar_color, pygame.Rect(0.85*SCREEN_WIDTH - rocket.player * 0.82*SCREEN_WIDTH, 0.95*SCREEN_HEIGHT, rocket.health, 10))
        self.screen.blit(self.rocket_rotation_images[rocket.player][rocket.angle // 12], (rocket.centerx - ROCKET_IMAGE_WIDTH / 2, rocket.centery - ROCKET_IMAGE_HEIGHT / 2))

    def draw_asteroid(self, asteroid):
        self.screen.blit(self.asteroid_images[asteroid.player][int(asteroid.size_index)][asteroid.random_image_index], (asteroid.centerx - asteroid.image_width / 2, asteroid.centery - asteroid.image_height / 2))

    def draw_bullet(self, bullet):
        self.screen.blit(self.bullet_angle_images[bullet.split][bullet.rocket.player][bullet.angle // 12], (bullet.centerx - BULLET_IMAGE_WIDTH / 2, bullet.centery - BULLET_IMAGE_HEIGHT / 2))

    def draw_line(self, pointA, pointB):
        pygame.draw.line(self.screen, PLAYER_ONE_COLOR, pointA, pointB)

    def save_image(self):
        pygame.image.save(self.screen, "bp/Obrazky/N_nearest_asteroids.png")

    def render(self):
        pygame.display.update()