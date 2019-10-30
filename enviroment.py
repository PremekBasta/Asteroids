
import pygame
import random
import sys, time
from sprite_object import Rocket, Rocket_action, Bullet, Asteroid
from state import State
from constants import *



black = (0, 0, 0)
white = (255,255,255)




class Enviroment():
    def __init__(self, visual, rocket_one_invulnerable, rocket_two_invulnerable):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.init()
        self.bullets_one = []
        self.bullets_two = []
        self.asteroids_neutral = []
        self.asteroids_one = []
        self.asteroids_two = []
        Asteroid.initialize_images()
        self.rockets = []
        self.RocketOne = Rocket(self.screen, 0)
        self.RocketTwo = Rocket(self.screen, 1)
        self.rockets.append(self.RocketOne)
        self.rockets.append(self.RocketTwo)
        self.visual = visual
        self.rocket_one_invulnerable = rocket_one_invulnerable
        self.rocket_two_invlunerable = rocket_two_invulnerable

        self.ticks_elapsed_since_last_asteroid = 0
        self.ticks_amount_to_create_asteroid = 50
        self.step_count = 0
        self.game_over = False
        self.generate_asteroid = True

    def reset(self):
        self.asteroids_neutral = []

        self.RocketOne = Rocket(self.screen, 0)
        self.asteroids_one = []
        self.bullets_one = []

        self.RocketTwo = Rocket(self.screen, 1)
        self.asteroids_two = []
        self.bullets_two = []

        self.game_over = False
        self.step_count = 0
        self.ticks_elapsed_since_last_asteroid = 0
        self.ticks_amount_to_create_asteroid = 50

        return State(self.asteroids_neutral, self.RocketOne, self.asteroids_one, self.bullets_one,
                     self.RocketTwo, self.asteroids_two, self.bullets_two)


    def next_step(self, actions_one, actions_two):
        self.step_count = self.step_count + 1

        self._handle_actions_(actions_one, actions_two)

        self._generate_asteroid_()

        self._check_collisions_()

        self._move_sprites_()

        if self.visual:
            self._draw_sprites_()

        game_over = self._check_end_()

        current_state = State(self.asteroids_neutral, self.RocketOne, self.asteroids_one, self.bullets_one,
                              self.RocketTwo, self.asteroids_two, self.bullets_two)

        return self.step_count, game_over, current_state


    def _handle_actions_(self, actions_one, actions_two):
        if Rocket_action.ROCKET_ONE_ROTATE_LEFT in actions_one:
            self.RocketOne.rotate_left()
        if Rocket_action.ROCKET_ONE_ROTATE_RIGHT in actions_one:
            self.RocketOne.rotate_right()
        if Rocket_action.ROCKET_ONE_ACCELERATE in actions_one:
            self.RocketOne.accelerate()
        if Rocket_action.ROCKET_ONE_SHOOT in actions_one:
            self.bullets_one.append(Bullet(self.screen, self.RocketOne, split=0))
        if Rocket_action.ROCKET_ONE_SPLIT_SHOOT in actions_one:
            self.bullets_one.append(Bullet(self.screen, self.RocketOne, split=1))

        if Rocket_action.ROCKET_TWO_ROTATE_LEFT in actions_two:
            self.RocketTwo.rotate_left()
        if Rocket_action.ROCKET_TWO_ROTATE_RIGHT in actions_two:
            self.RocketTwo.rotate_right()
        if Rocket_action.ROCKET_TWO_ACCELERATE in actions_two:
            self.RocketTwo.accelerate()
        if Rocket_action.ROCKET_TWO_SHOOT in actions_two:
            self.bullets_two.append(Bullet(self.screen, self.RocketTwo, split=0))
        if Rocket_action.ROCKET_TWO_SPLIT_SHOOT in actions_two:
            self.bullets_two.append(Bullet(self.screen, self.RocketTwo, split=1))

    def _generate_asteroid_(self):
        # if self.generate_asteroid:
        #     ast = Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None)
        #     ast.collision_rect.center = (self.RocketTwo.collision_rect.centerx + 400, self.RocketTwo.collision_rect.centery)
        #     ast.speedx = 0
        #     ast.speedy = 0
        #     bullet = Bullet(self.screen, self.RocketOne, split=0)
        #
        #     # ast = Asteroid(self.screen, None, None, ast, self.RocketOne, bullet)
        #     self.asteroids_neutral.append(ast)
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.generate_asteroid = False
        # return

        if self.ticks_elapsed_since_last_asteroid > self.ticks_amount_to_create_asteroid:
            self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
            self.ticks_elapsed_since_last_asteroid = 0
            if self.ticks_amount_to_create_asteroid > 5:
                self.ticks_amount_to_create_asteroid = self.ticks_amount_to_create_asteroid - 1
        else:
            self.ticks_elapsed_since_last_asteroid = self.ticks_elapsed_since_last_asteroid + 1



    def _check_collisions_(self):
        # Bullets ONE with NEUTRAL asteroids
        for bullet_one in self.bullets_one:
            for asteroid in self.asteroids_neutral:
                if bullet_one.collision_rect.colliderect(asteroid.collision_rect):
                    self.asteroids_neutral.remove(asteroid)
                    new_asteroid, new_asteroid_one, new_asteroid_two = None, None, None
                    if bullet_one.split:
                        new_asteroid_one, new_asteroid_two = Asteroid.split_asteroid(self.screen, bullet_one.rocket, asteroid, bullet_one)
                    else:
                        new_asteroid = Asteroid(self.screen, None, None, asteroid, bullet_one.rocket, bullet_one)


                    if bullet_one in self.bullets_one:
                        self.bullets_one.remove(bullet_one)

                    if new_asteroid_one is not None and new_asteroid_one.valid \
                    and new_asteroid_two is not None and new_asteroid_two.valid:
                        self.asteroids_one.append(new_asteroid_one)
                        self.asteroids_one.append(new_asteroid_two)

                    if new_asteroid is not None and  new_asteroid.valid:
                        self.asteroids_one.append(new_asteroid)
                    continue

        # Bullets ONE with TWO's asteroids
        for bullet_one in self.bullets_one:
            for asteroid_two in self.asteroids_two:
                if bullet_one.collision_rect.colliderect(asteroid_two.collision_rect):
                    self.asteroids_two.remove(asteroid_two)

                    new_asteroid, new_asteroid_one, new_asteroid_two = None, None, None
                    if bullet_one.split:
                        new_asteroid_one, new_asteroid_two = Asteroid.split_asteroid(self.screen, bullet_one.rocket, asteroid_two, bullet_one)
                    else:
                        new_asteroid = Asteroid(self.screen, None, None, asteroid_two, bullet_one.rocket,bullet_one)

                    if bullet_one in self.bullets_one:
                        self.bullets_one.remove(bullet_one)

                    if new_asteroid_one is not None and new_asteroid_one.valid \
                            and asteroid_two is not None and asteroid_two.valid:
                        self.asteroids_one.append(new_asteroid_one)
                        self.asteroids_one.append(new_asteroid_two)

                    if new_asteroid is not None and  new_asteroid.valid:
                        self.asteroids_one.append(new_asteroid)

        # Bullets TWO with ONE' asteroids
        for bullet_two in self.bullets_two:
            for asteroid_one in self.asteroids_one:
                if bullet_two.collision_rect.colliderect(asteroid_one.collision_rect):
                    self.asteroids_one.remove(asteroid_one)

                    new_asteroid, new_asteroid_one, new_asteroid_two = None, None, None
                    if bullet_two.split:
                        asteroid_one, asteroid_two = Asteroid.split_asteroid(self.screen, bullet_two.rocket, asteroid_one, bullet_two)
                    else:
                        new_asteroid = Asteroid(self.screen, None, None, asteroid_one, bullet_two.rocket, bullet_two)
                    if bullet_two in self.bullets_two:
                        self.bullets_two.remove(bullet_two)

                    if new_asteroid_one is not None and asteroid_one.valid \
                            and new_asteroid_two is not None and asteroid_two.valid:
                        self.asteroids_two.append(new_asteroid_one)
                        self.asteroids_two.append(new_asteroid_two)

                    if new_asteroid is not None and  new_asteroid.valid:
                        self.asteroids_two.append(new_asteroid)

        # Bullets TWO with NEUTRAL asteroids
        for bullet_two in self.bullets_two:
            for asteroid in self.asteroids_neutral:
                if bullet_two.collision_rect.colliderect(asteroid.collision_rect):
                    self.asteroids_neutral.remove(asteroid)

                    new_asteroid, new_asteroid_one, new_asteroid_two = None, None, None
                    if bullet_two.split:
                        new_asteroid_one, new_asteroid_two = Asteroid.split_asteroid(self.screen, bullet_two.rocket, asteroid, bullet_two)
                    else:
                        new_asteroid = Asteroid(self.screen, self.RocketOne, self.RocketTwo, asteroid, bullet_two.rocket,
                                            bullet_two)

                    if bullet_two in self.bullets_two:
                        self.bullets_two.remove(bullet_two)


                    if new_asteroid_one is not None and new_asteroid_one.valid \
                            and new_asteroid_two is not None and new_asteroid_two.valid:
                        self.asteroids_two.append(new_asteroid_one)
                        self.asteroids_two.append(new_asteroid_two)
                    if new_asteroid is not None and  new_asteroid.valid:
                        self.asteroids_two.append(new_asteroid)
                    continue


        # Rocket ONE collisions
        if self.rocket_one_invulnerable == False:
            for asteroid in self.asteroids_neutral:
                if asteroid.collision_rect.colliderect(self.RocketOne.collision_rect):
                    self.asteroids_neutral.remove(asteroid)
                    self.RocketOne.health = self.RocketOne.health - 10

            for asteroid_two in self.asteroids_two:
                if asteroid_two.collision_rect.colliderect(self.RocketOne.collision_rect):
                    self.asteroids_two.remove(asteroid_two)
                    self.RocketOne.health = self.RocketOne.health - 30

        # Rocket TWO collisions
        if self.rocket_two_invlunerable == False:
            for asteroid in self.asteroids_neutral:
                if asteroid.collision_rect.colliderect(self.RocketTwo.collision_rect):
                    self.asteroids_neutral.remove(asteroid)
                    self.RocketTwo.health = self.RocketTwo.health - 10

            for asteroid_one in self.asteroids_one:
                if asteroid_one.collision_rect.colliderect(self.RocketTwo.collision_rect):
                    self.asteroids_one.remove(asteroid_one)
                    self.RocketTwo.health = self.RocketTwo.health - 30



    def _move_sprites_(self):
        self.RocketOne.move()
        self.RocketTwo.move()


        for bullet_one in self.bullets_one:
            if bullet_one.is_alive():
                bullet_one.move()
            else:
                self.bullets_one.remove(bullet_one)

        for bullet_two in self.bullets_two:
            if bullet_two.is_alive():
                bullet_two.move()
            else:
                self.bullets_two.remove(bullet_two)


        for asteroid in self.asteroids_neutral:
            asteroid.move()

        for asteroid_one in self.asteroids_one:
            asteroid_one.move()

        for asteroid_two in self.asteroids_two:
            asteroid_two.move()



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
        for asteroid_one in self.asteroids_one:
            asteroid_one.draw()
        for asteroid_two in self.asteroids_two:
            asteroid_two.draw()


        pygame.display.update()

    def _check_end_(self):
        if self.RocketOne.health <= 0 or self.RocketTwo.health <= 0:
            return (True, self.RocketOne.health, self.RocketTwo.health)
        return (False, self.RocketOne.health, self.RocketTwo.health)


    def _update_(self):
        pass


    def get_actions_from_keyboard_input(self):
        actions_one = []
        actions_two = []
        actions = []
        events = pygame.event.get(pygame.KEYDOWN)
        for event in events:
            if(event.key == pygame.K_SPACE):
                actions.append(Rocket_action.ROCKET_ONE_SHOOT)
                actions_one.append(Rocket_action.ROCKET_ONE_SHOOT)
            if(event.key == pygame.K_LCTRL):
                actions.append(Rocket_action.ROCKET_TWO_SHOOT)
                actions_two.append(Rocket_action.ROCKET_TWO_SHOOT)


        all_keys = pygame.key.get_pressed()
        if all_keys[pygame.K_UP]:
            actions.append(Rocket_action.ROCKET_ONE_ACCELERATE)
            actions_one.append(Rocket_action.ROCKET_ONE_ACCELERATE)
        if all_keys[pygame.K_LEFT]:
            actions.append(Rocket_action.ROCKET_ONE_ROTATE_LEFT)
            actions_one.append(Rocket_action.ROCKET_ONE_ROTATE_LEFT)
        if all_keys[pygame.K_RIGHT]:
            actions.append(Rocket_action.ROCKET_ONE_ROTATE_RIGHT)
            actions_one.append(Rocket_action.ROCKET_ONE_ROTATE_RIGHT)


        if all_keys[pygame.K_a]:
            actions.append(Rocket_action.ROCKET_TWO_ROTATE_LEFT)
            actions_two.append(Rocket_action.ROCKET_TWO_ROTATE_LEFT)
        if all_keys[pygame.K_d]:
            actions.append(Rocket_action.ROCKET_TWO_ROTATE_RIGHT)
            actions_two.append(Rocket_action.ROCKET_TWO_ROTATE_RIGHT)
        if all_keys[pygame.K_w]:
            actions.append(Rocket_action.ROCKET_TWO_ACCELERATE)
            actions_two.append(Rocket_action.ROCKET_TWO_ACCELERATE)



        # clearing it apparently prevents from stucking
        pygame.event.clear()
        return actions_one, actions_two