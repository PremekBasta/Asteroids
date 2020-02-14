
import pygame
import random
import sys, time
from sprite_object import Rocket, Rocket_action, Rocket_base_action, Bullet, Asteroid, collides
from state import State
from constants import *



black = (0, 0, 0)
white = (255,255,255)




class Enviroment():
    def __init__(self, visual, rocket_one_invulnerable, rocket_two_invulnerable, draw_modul = None):
        super().__init__()
        # pygame.init()
        self.draw_modul = draw_modul
        # self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # pygame.display.init()
        self.bullets_one = []
        self.bullets_two = []
        self.asteroids_neutral = []
        self.asteroids_one = []
        self.asteroids_two = []
        # Asteroid.initialize_images()
        # Bullet.initialize_images()
        self.rockets = []
        self.RocketOne = Rocket(0)
        self.RocketOne.speedx = 10
        self.RocketOne.speedy = 10
        self.RocketTwo = Rocket(1)
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

        self.RocketOne = Rocket(0)
        self.RocketOne.speedx = 0
        self.RocketOne.speedy = 0
        self.RocketOne.angle = 0
        self.asteroids_one = []
        self.bullets_one = []

        self.RocketTwo = Rocket(1)
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


        if self.draw_modul is not None:
            self.draw_modul.clear_display()


            self.draw_modul.draw_rocket(self.RocketOne)
            self.draw_modul.draw_rocket(self.RocketTwo)

            for bullet in self.bullets_one:
                self.draw_modul.draw_bullet(bullet)
            for bullet in self.bullets_two:
                self.draw_modul.draw_bullet(bullet)

            for asteroid in self.asteroids_neutral:
                self.draw_modul.draw_asteroid(asteroid)
            for asteroid in self.asteroids_one:
                self.draw_modul.draw_asteroid(asteroid)
            for asteroid in self.asteroids_two:
                self.draw_modul.draw_asteroid(asteroid)

            self.draw_modul.render()

        (game_over, player_one_won) = self._check_end_()

        current_state = State(self.asteroids_neutral, self.RocketOne, self.asteroids_one, self.bullets_one,
                              self.RocketTwo, self.asteroids_two, self.bullets_two)

        return self.step_count, (game_over, player_one_won), current_state, actions_one, actions_two


    def _handle_actions_(self, actions_one, actions_two):
        if Rocket_base_action.ROTATE_LEFT in actions_one:
            self.RocketOne.rotate_left()
        if Rocket_base_action.ROTATE_RIGHT in actions_one:
            self.RocketOne.rotate_right()
        if Rocket_base_action.ACCELERATE in actions_one:
            self.RocketOne.accelerate()
        if Rocket_base_action.SHOT in actions_one:
            self.bullets_one.append(Bullet(self.RocketOne, split=0))
        if Rocket_base_action.SPLIT_SHOOT in actions_one:
            self.bullets_one.append(Bullet(self.RocketOne, split=1))

        if Rocket_base_action.ROTATE_LEFT in actions_two:
            self.RocketTwo.rotate_left()
        if Rocket_base_action.ROTATE_RIGHT in actions_two:
            self.RocketTwo.rotate_right()
        if Rocket_base_action.ACCELERATE in actions_two:
            self.RocketTwo.accelerate()
        if Rocket_base_action.SHOT in actions_two:
            self.bullets_two.append(Bullet(self.RocketTwo, split=0))
        if Rocket_base_action.SPLIT_SHOOT in actions_two:
            self.bullets_two.append(Bullet(self.RocketTwo, split=1))

        ################



        # if Rocket_action.ROCKET_ONE_ROTATE_LEFT in actions_one:
        #     self.RocketOne.rotate_left()
        # if Rocket_action.ROCKET_ONE_ROTATE_RIGHT in actions_one:
        #     self.RocketOne.rotate_right()
        # if Rocket_action.ROCKET_ONE_ACCELERATE in actions_one:
        #     self.RocketOne.accelerate()
        # if Rocket_action.ROCKET_ONE_SHOOT in actions_one:
        #     self.bullets_one.append(Bullet(self.screen, self.RocketOne, split=0))
        # if Rocket_action.ROCKET_ONE_SPLIT_SHOOT in actions_one:
        #     self.bullets_one.append(Bullet(self.screen, self.RocketOne, split=1))
        #
        # if Rocket_action.ROCKET_TWO_ROTATE_LEFT in actions_two:
        #     self.RocketTwo.rotate_left()
        # if Rocket_action.ROCKET_TWO_ROTATE_RIGHT in actions_two:
        #     self.RocketTwo.rotate_right()
        # if Rocket_action.ROCKET_TWO_ACCELERATE in actions_two:
        #     self.RocketTwo.accelerate()
        # if Rocket_action.ROCKET_TWO_SHOOT in actions_two:
        #     self.bullets_two.append(Bullet(self.screen, self.RocketTwo, split=0))
        # if Rocket_action.ROCKET_TWO_SPLIT_SHOOT in actions_two:
        #     self.bullets_two.append(Bullet(self.screen, self.RocketTwo, split=1))

    def _generate_asteroid_(self):
        # if self.generate_asteroid:
        #     ast = Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None)
        #
        #     # ast.collision_rect.center = (self.RocketTwo.centerx + 600, self.RocketTwo.centery)
        #     ast.centerx = self.RocketOne.centerx - 100
        #     ast.centery = self.RocketOne.centery + 200
        #     # ast.centerx = ast.centerx
        #     # ast.centery = ast.centery
        #     ast.speedx = 2
        #     ast.speedy = 2
        #     bullet = Bullet(self.screen, self.RocketOne, split=0)
        #
        #     ast = Asteroid(self.screen, None, None, ast, self.RocketOne, bullet)
        #     self.asteroids_neutral.append(ast)
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))
        #     self.generate_asteroid = False
        # return

        if self.ticks_elapsed_since_last_asteroid > self.ticks_amount_to_create_asteroid:
            self.asteroids_neutral.append(Asteroid(self.RocketOne, self.RocketTwo, None, None, None))
            self.ticks_elapsed_since_last_asteroid = 0
            if self.ticks_amount_to_create_asteroid > 5:
                self.ticks_amount_to_create_asteroid = self.ticks_amount_to_create_asteroid - 1
        else:
            self.ticks_elapsed_since_last_asteroid = self.ticks_elapsed_since_last_asteroid + 1


    def check_collisions_objects_one(self):
        # Bullets ONE with NEUTRAL asteroids
        for bullet_one in self.bullets_one:
            for asteroid in self.asteroids_neutral:
                # if collides(bullet_one, asteroid):
                if collides(bullet_one, asteroid):
                    # if bullet_one.collision_rect.colliderect(asteroid.collision_rect):
                    self.asteroids_neutral.remove(asteroid)
                    new_asteroid, new_asteroid_one, new_asteroid_two = None, None, None
                    if bullet_one.split:
                        new_asteroid_one, new_asteroid_two = Asteroid.split_asteroid(bullet_one.rocket,
                                                                                     asteroid, bullet_one)
                    else:
                        new_asteroid = Asteroid(None, None, asteroid, bullet_one.rocket, bullet_one)

                    if bullet_one in self.bullets_one:
                        self.bullets_one.remove(bullet_one)

                    if new_asteroid_one is not None and new_asteroid_one.valid \
                            and new_asteroid_two is not None and new_asteroid_two.valid:
                        self.asteroids_one.append(new_asteroid_one)
                        self.asteroids_one.append(new_asteroid_two)

                    if new_asteroid is not None and new_asteroid.valid:
                        self.asteroids_one.append(new_asteroid)
                    continue

        # Bullets ONE with TWO's asteroids
        for bullet_one in self.bullets_one:
            for asteroid_two in self.asteroids_two:
                if collides(bullet_one, asteroid_two):
                    # if bullet_one.collision_rect.colliderect(asteroid_two.collision_rect):
                    self.asteroids_two.remove(asteroid_two)

                    new_asteroid, new_asteroid_one, new_asteroid_two = None, None, None
                    if bullet_one.split:
                        new_asteroid_one, new_asteroid_two = Asteroid.split_asteroid(bullet_one.rocket,
                                                                                     asteroid_two, bullet_one)
                    else:
                        new_asteroid = Asteroid(None, None, asteroid_two, bullet_one.rocket,
                                                bullet_one)

                    if bullet_one in self.bullets_one:
                        self.bullets_one.remove(bullet_one)

                    if new_asteroid_one is not None and new_asteroid_one.valid \
                            and asteroid_two is not None and asteroid_two.valid:
                        self.asteroids_one.append(new_asteroid_one)
                        self.asteroids_one.append(new_asteroid_two)

                    if new_asteroid is not None and new_asteroid.valid:
                        self.asteroids_one.append(new_asteroid)

        # Rocket ONE collisions
        if self.rocket_one_invulnerable == False:
            for asteroid in self.asteroids_neutral:
                if collides(asteroid, self.RocketOne):
                    # if asteroid.collision_rect.colliderect(self.RocketOne.collision_rect):
                    self.asteroids_neutral.remove(asteroid)
                    self.RocketOne.health = self.RocketOne.health - 10

            for asteroid_two in self.asteroids_two:
                if collides(asteroid_two, self.RocketOne):
                    # if asteroid_two.collision_rect.colliderect(self.RocketOne.collision_rect):
                    self.asteroids_two.remove(asteroid_two)
                    self.RocketOne.health = self.RocketOne.health - 30

    def check_collisions_objects_two(self):
        # Bullets TWO with ONE' asteroids
        for bullet_two in self.bullets_two:
            for asteroid_one in self.asteroids_one:
                if collides(bullet_two, asteroid_one):
                    # if bullet_two.collision_rect.colliderect(asteroid_one.collision_rect):
                    self.asteroids_one.remove(asteroid_one)

                    new_asteroid, new_asteroid_one, new_asteroid_two = None, None, None
                    if bullet_two.split:
                        new_asteroid_one, new_asteroid_two = Asteroid.split_asteroid(bullet_two.rocket,
                                                                                     asteroid_one,
                                                                                     bullet_two)
                    else:
                        new_asteroid = Asteroid(None, None, asteroid_one,
                                                bullet_two.rocket, bullet_two)
                    if bullet_two in self.bullets_two:
                        self.bullets_two.remove(bullet_two)

                    if new_asteroid_one is not None and new_asteroid_one.valid \
                            and new_asteroid_two is not None and new_asteroid_two.valid:
                        self.asteroids_two.append(new_asteroid_one)
                        self.asteroids_two.append(new_asteroid_two)

                    if new_asteroid is not None and new_asteroid.valid:
                        self.asteroids_two.append(new_asteroid)

        # Bullets TWO with NEUTRAL asteroids
        for bullet_two in self.bullets_two:
            for asteroid in self.asteroids_neutral:
                if collides(bullet_two, asteroid):
                    # if bullet_two.collision_rect.colliderect(asteroid.collision_rect):
                    self.asteroids_neutral.remove(asteroid)

                    new_asteroid, new_asteroid_one, new_asteroid_two = None, None, None
                    if bullet_two.split:
                        new_asteroid_one, new_asteroid_two = Asteroid.split_asteroid(bullet_two.rocket,
                                                                                     asteroid,
                                                                                     bullet_two)
                    else:
                        new_asteroid = Asteroid(self.RocketOne, self.RocketTwo, asteroid,
                                                bullet_two.rocket,
                                                bullet_two)

                    if bullet_two in self.bullets_two:
                        self.bullets_two.remove(bullet_two)

                    if new_asteroid_one is not None and new_asteroid_one.valid \
                            and new_asteroid_two is not None and new_asteroid_two.valid:
                        self.asteroids_two.append(new_asteroid_one)
                        self.asteroids_two.append(new_asteroid_two)
                    if new_asteroid is not None and new_asteroid.valid:
                        self.asteroids_two.append(new_asteroid)
                    continue

        # Rocket TWO collisions
        if self.rocket_two_invlunerable == False:
            for asteroid in self.asteroids_neutral:
                if collides(asteroid, self.RocketTwo):
                    # if asteroid.collision_rect.colliderect(self.RocketTwo.collision_rect):
                    self.asteroids_neutral.remove(asteroid)
                    self.RocketTwo.health = self.RocketTwo.health - 10

            for asteroid_one in self.asteroids_one:
                if collides(asteroid_one, self.RocketTwo):
                    # if asteroid_one.collision_rect.colliderect(self.RocketTwo.collision_rect):
                    self.asteroids_one.remove(asteroid_one)
                    self.RocketTwo.health = self.RocketTwo.health - 30

    def  _check_collisions_(self):
        if self.step_count % 2 == 0:
            self.check_collisions_objects_one()
            self.check_collisions_objects_two()
        else:
            self.check_collisions_objects_two()
            self.check_collisions_objects_one()


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



    # def _draw_sprites_(self):
    #     self.screen.fill((0,0,0))
    #
    #     # Rockets
    #     self.RocketOne.draw()
    #     self.RocketTwo.draw()
    #
    #     # Bullets
    #     for bullet_one in self.bullets_one:
    #         bullet_one.draw()
    #
    #     for bullet_two in self.bullets_two:
    #         bullet_two.draw()
    #
    #     # Asteroids
    #     for asteroid in self.asteroids_neutral:
    #         asteroid.draw()
    #     for asteroid_one in self.asteroids_one:
    #         asteroid_one.draw()
    #     for asteroid_two in self.asteroids_two:
    #         asteroid_two.draw()
    #
    #
    #     pygame.display.update()

    def _check_end_(self):
        # Returns (game_is_over, player_one_won)
        if self.RocketOne.health <= 0:
            return (True, False)
        if self.RocketTwo.health <= 0:
            return (True, True)
        return (False, False)

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