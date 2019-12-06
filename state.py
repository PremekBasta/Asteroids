from dto import SpaceObjectDTO
from constants import *
import copy
import pygame

class State:
    def __init__(self, neutral_asteroids,
                 player_one_rocket, player_one_asteroids, player_one_bullets,
                 player_two_rocket, player_two_asteroids, player_two_bullets):


        rect = pygame.rect.Rect(0,0,0,0)

        # Neutral asteroids
        self.neutral_asteroids = []
        for neutral_asteroid in neutral_asteroids:
            self.neutral_asteroids.append(SpaceObjectDTO(neutral_asteroid.radius, neutral_asteroid.centerx, neutral_asteroid.centery,
                # neutral_asteroid.collision_rect,
                                                         neutral_asteroid.speedx * 8,
                                                         neutral_asteroid.speedy * 8, neutral_asteroid.get_angle(), size_index = neutral_asteroid.size_index))

        # Player ONE
        # Rocket ONE
        self.player_one_rocket = SpaceObjectDTO(player_one_rocket.radius, player_one_rocket.centerx, player_one_rocket.centery,
                                                # player_one_rocket.collision_rect,
                                                player_one_rocket.speedx
                                                # // 8
                                                ,
                                                player_one_rocket.speedy
                                                # // 8
                                                , player_one_rocket.angle, player = player_one_rocket.player)
        # Asteroids ONE
        self.player_one_asteroids = []
        for player_one_asteroid in player_one_asteroids:
            self.player_one_asteroids.append(SpaceObjectDTO(player_one_asteroid.radius, player_one_asteroid.centerx, player_one_asteroid.centery,
                                                            # player_one_asteroid.collision_rect,
                                                            player_one_asteroid.speedx * 8,
                                                            player_one_asteroid.speedy * 8, player_one_asteroid.get_angle(), size_index = player_one_asteroid.size_index))
        # Bullets ONE
        self.player_one_bullets = []
        for player_one_bullet in player_one_bullets:
            self.player_one_bullets.append(SpaceObjectDTO(player_one_bullet.radius, player_one_bullet.centerx, player_one_bullet.centery,
                                                          # player_one_bullet.collision_rect,
                                                          player_one_bullet.speedx
                                                          # / 8
                                                          ,
                                                          player_one_bullet.speedy
                                                          # / 8
                                                          , player_one_bullet.angle, player_one_bullet.life_count))

        # Player TWO
        # Rocket TWO
        self.player_two_rocket = SpaceObjectDTO(player_two_rocket.radius, player_two_rocket.centerx, player_two_rocket.centery,
                                                # player_two_rocket.collision_rect,
                                                player_two_rocket.speedx
                                                # / 8
                                                ,
                                                player_two_rocket.speedy
                                                # / 8
                                                , player_two_rocket.angle, player = player_two_rocket.player)
        #Asteroids TWO
        self.player_two_asteroids = []
        for player_two_asteroid in player_two_asteroids:
            self.player_two_asteroids.append(SpaceObjectDTO(player_two_asteroid.radius, player_two_asteroid.centerx, player_two_asteroid.centery,
                                                            # player_two_asteroid.collision_rect,
                                                            player_two_asteroid.speedx * 8,
                                                            player_two_asteroid.speedy * 8, player_two_asteroid.get_angle(), size_index = player_two_asteroid.size_index))
        # Bullets TWO
        self.player_two_bullets = []
        for player_two_bullet in player_two_bullets:
            self.player_two_bullets.append(SpaceObjectDTO(player_two_bullet.radius, player_two_bullet.centerx, player_two_bullet.centery,
                                                          # player_two_bullet.collision_rect,
                                                          player_two_bullet.speedx
                                                          # / 8
                                                          ,
                                                          player_two_bullet.speedy
                                                          # / 8
                                                          , player_two_bullet.angle, player_two_bullet.life_count))
