
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
        self.bullets_one = []
        self.bullets_two = []
        self.asteroids_neutral = []
        Asteroid.initialize_images()
        self.rockets = pygame.sprite.Group()
        self.RocketOne = Rocket(self.screen, 0)
        self.RocketTwo = Rocket(self.screen, 1)
        self.rockets.add(self.RocketOne, self.RocketTwo)
        self.visual = visual
        global i
        i = 0




    def next_step(self, actions):



        if Rocket_action.ROCKET_ONE_ROTATE_LEFT in actions:
            self.RocketOne.rotate_left()
        if Rocket_action.ROCKET_ONE_ROTATE_RIGHT in actions:
            self.RocketOne.rotate_right()
        if Rocket_action.ROCKET_ONE_ACCELERATE in actions:
            self.RocketOne.accelerate()
        if Rocket_action.ROCKET_ONE_SHOOT in actions:
            self.bullets_one.append(Bullet(self.screen, self.RocketOne))

        if Rocket_action.ROCKET_TWO_ROTATE_LEFT in actions:
            self.RocketTwo.rotate_left()
        if Rocket_action.ROCKET_TWO_ROTATE_RIGHT in actions:
            self.RocketTwo.rotate_right()
        if Rocket_action.ROCKET_TWO_ACCELERATE in actions:
            self.RocketTwo.accelerate()
        if Rocket_action.ROCKET_TWO_SHOOT in actions:
            self.bullets_two.append(Bullet(self.screen, self.RocketTwo))

        if "Debug" in actions:
            self.print_debug()

        if random.randint(0,100) == 5:
            self.asteroids_neutral.append(Asteroid(self.screen, 0))

        self._check_collisions_()

        self._update_sprites_()

        self._draw_sprites_()

    def _check_collisions_(self):
        for bullet_one in self.bullets_one:
            for asteroid in self.asteroids_neutral:
                if bullet_one.rect.colliderect(asteroid.collision_rect):
                    self.asteroids_neutral.remove(asteroid)
                    if bullet_one in self.bullets_one:
                        self.bullets_one.remove(bullet_one)
                    continue

        for bullet_two in self.bullets_two:
            for asteroid in self.asteroids_neutral:
                if bullet_two.rect.colliderect(asteroid.collision_rect):
                    self.asteroids_neutral.remove(asteroid)
                    if bullet_two in self.bullets_two:
                        self.bullets_two.remove(bullet_two)
                    continue

        for asteroid in self.asteroids_neutral:
            if asteroid.collision_rect.colliderect(self.RocketOne.collision_rect) or asteroid.collision_rect.colliderect(self.RocketTwo.collision_rect):
                quit()

    def _update_sprites_(self):
        for rocket in self.rockets:
            rocket.update()
        # self.RocketOne.update()

        for bullet_one in self.bullets_one:
            if bullet_one.is_alive():
                bullet_one.update()
            else:
                self.bullets_one.remove(bullet_one)

        for bullet_two in self.bullets_two:
            if bullet_two.is_alive():
                bullet_two.update()
            else:
                self.bullets_two.remove(bullet_two)


        for asteroid in self.asteroids_neutral:
            asteroid.update()



    def _draw_sprites_(self):
        self.screen.fill((0,0,0))

        # Rockets
        self.RocketOne.draw()
        self.RocketTwo.draw()

        # Bullets
        for bullet_one in self.bullets_one:
            bullet_one.draw()

        for bullet_two in self.bullets_two:
            bullet_two.draw()

        # Asteroids
        for asteroid in self.asteroids_neutral:
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
            if(event.key == pygame.K_LCTRL):
                actions.append(Rocket_action.ROCKET_TWO_SHOOT)


        all_keys = pygame.key.get_pressed()
        if all_keys[pygame.K_UP]:
            actions.append(Rocket_action.ROCKET_ONE_ACCELERATE)
        if all_keys[pygame.K_LEFT]:
            actions.append(Rocket_action.ROCKET_ONE_ROTATE_LEFT)
        if all_keys[pygame.K_RIGHT]:
            actions.append(Rocket_action.ROCKET_ONE_ROTATE_RIGHT)


        if all_keys[pygame.K_a]:
            actions.append(Rocket_action.ROCKET_TWO_ROTATE_LEFT)
        if all_keys[pygame.K_d]:
            actions.append(Rocket_action.ROCKET_TWO_ROTATE_RIGHT)
        if all_keys[pygame.K_w]:
            actions.append(Rocket_action.ROCKET_TWO_ACCELERATE)



        # clearing it apparently prevents from stucking
        pygame.event.clear()
        return actions