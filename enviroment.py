
import pygame
import random
import sys
from sprite_object import Rocket, Rocket_action, Bullet, Asteroid

screen_width = 900
screen_height = 600
black = (0, 0, 0)
white = (255,255,255)




class Enviroment():
    def __init__(self, visual):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.init()
        print("init")
        self.bullets_one = []
        self.asteroids_one = []
        self.rockets = pygame.sprite.Group()
        self.RocketOne = Rocket(self.screen)
        self.rockets.add(self.RocketOne)
        self.visual = visual
        global i
        i = 0

        self.x = 50
        self.y = 50



    def next_step(self, actions):
        # for action in actions:
        #     todo:switch


        if Rocket_action.ROCKET_ONE_ROTATE_LEFT in actions:
            self.RocketOne.rotate_left()
        if Rocket_action.ROCKET_ONE_ROTATE_RIGHT in actions:
            self.RocketOne.rotate_right()
        if Rocket_action.ROCKET_ONE_ACCELERATE in actions:
            self.RocketOne.accelerate()
        if Rocket_action.ROCKET_ONE_SHOOT in actions:
            self.bullets_one.append(Bullet(self.screen, self.RocketOne))

        if "Debug" in actions:
            self.print_debug()

        # if random.randint(0,10) == 5:
        self.asteroids_one.append(Asteroid(self.screen))

        self._check_collisions_()

        self._update_sprites_()

        self._draw_sprites_()

    def _check_collisions_(self):
        for bullet in self.bullets_one:
            for asteroid in self.asteroids_one:
                if bullet.rect.colliderect(asteroid.rect):
                    self.asteroids_one.remove(asteroid)

        for asteroid in self.asteroids_one:
            if asteroid.rect.colliderect(self.RocketOne.rect):
                print("you lost")
                quit()

    def _update_sprites_(self):
        for rocket in self.rockets:
            rocket.update()
        # self.RocketOne.update()

        for bullet in self.bullets_one:
            if bullet.is_alive():
                bullet.update()
            else:
                self.bullets_one.remove(bullet)

        for asteroid in self.asteroids_one:
            asteroid.update()



    def _draw_sprites_(self):
        self.screen.fill((0,0,0))

        # Rockets
        self.RocketOne.draw()

        # Bullets
        for bullet in self.bullets_one:
            bullet.draw()

        # Asteroids
        for asteroid in self.asteroids_one:
            asteroid.draw()


        pygame.display.update()

    def _update_(self):
        pass


    def get_actions_from_keyboard_input(self):
        actions = []
        events = pygame.event.get(pygame.KEYDOWN)
        for event in events:
            if(event.key == pygame.K_SPACE):
                actions.append(Rocket_action.ROCKET_ONE_SHOOT)
            if(event.key == pygame.K_d):
                actions.append("Debug")

        all_keys = pygame.key.get_pressed()
        if all_keys[pygame.K_UP]:
            actions.append(Rocket_action.ROCKET_ONE_ACCELERATE)
        if all_keys[pygame.K_LEFT]:
            actions.append(Rocket_action.ROCKET_ONE_ROTATE_LEFT)
        if all_keys[pygame.K_RIGHT]:
            actions.append(Rocket_action.ROCKET_ONE_ROTATE_RIGHT)
        if all_keys[pygame.K_d]:
            actions.append("Debug")

        # clearing it apparently prevents from stucking
        pygame.event.clear()
        return actions

    def print_debug(self):
        print("bullets: " + str(self.bullets_one))
        print("asteroids: " + str(self.asteroids_one))