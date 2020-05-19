# import pygame
from sprite_object import Rocket, RocketBaseAction, Bullet, Asteroid, collides
from state import State
from constants import *


class Enviroment:
    def __init__(self, draw_modul=None):
        super().__init__()
        self.draw_modul = draw_modul
        # self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # pygame.display.init()
        self.bullets_one = []
        self.bullets_two = []
        self.asteroids_neutral = []
        self.asteroids_one = []
        self.asteroids_two = []
        self.rockets = []
        self.rocket_one = Rocket(0)
        self.rocket_one.speedx = 10
        self.rocket_one.speedy = 10
        self.rocket_two = Rocket(1)
        self.rockets.append(self.rocket_one)
        self.rockets.append(self.rocket_two)
        self.reward_one = 0
        self.reward_two = 0

        self.ticks_elapsed_since_last_asteroid = 0
        self.ticks_to_create_asteroid = TICKS_TO_GENERATE_ASTEROID
        self.step_count = 0
        self.game_over = False

    def reset(self):
        self.asteroids_neutral = []
        self.rocket_one = Rocket(0)
        self.rocket_two = Rocket(1)
        self.asteroids_one = []
        self.asteroids_two = []
        self.bullets_one = []
        self.bullets_two = []
        self.game_over = False
        self.step_count = 0
        self.ticks_elapsed_since_last_asteroid = 0
        self.ticks_to_create_asteroid = TICKS_TO_GENERATE_ASTEROID

        return State(self.asteroids_neutral, self.rocket_one, self.asteroids_one, self.bullets_one,
                     self.rocket_two, self.asteroids_two, self.bullets_two)

    def next_step(self, actions_one, actions_two):
        self.step_count = self.step_count + 1
        self.reward_one = 0
        self.reward_two = 0

        self.handle_actions(actions_one, actions_two)
        self.generate_asteroid()
        self.check_collisions()
        self.move_objects()

        if self.draw_modul is not None:
            self.render()

        (game_over, player_one_won) = self.check_end()
        if not game_over:
            self.reward_one += 1
            self.reward_two += 1

        current_state = State(self.asteroids_neutral,
                              self.rocket_one,
                              self.asteroids_one,
                              self.bullets_one,
                              self.rocket_two,
                              self.asteroids_two,
                              self.bullets_two)

        return self.step_count, \
               (game_over, player_one_won), \
               current_state, \
               (self.reward_one, self.reward_two)

    def handle_actions(self, actions_one, actions_two):
        if RocketBaseAction.ROTATE_LEFT in actions_one:
            self.rocket_one.rotate_left()
        if RocketBaseAction.ROTATE_RIGHT in actions_one:
            self.rocket_one.rotate_right()
        if RocketBaseAction.ACCELERATE in actions_one:
            self.rocket_one.accelerate()
        if RocketBaseAction.SHOT in actions_one:
            self.bullets_one.append(Bullet(self.rocket_one, split=0))
        if RocketBaseAction.SPLIT_SHOOT in actions_one:
            self.bullets_one.append(Bullet(self.rocket_one, split=1))

        if RocketBaseAction.ROTATE_LEFT in actions_two:
            self.rocket_two.rotate_left()
        if RocketBaseAction.ROTATE_RIGHT in actions_two:
            self.rocket_two.rotate_right()
        if RocketBaseAction.ACCELERATE in actions_two:
            self.rocket_two.accelerate()
        if RocketBaseAction.SHOT in actions_two:
            self.bullets_two.append(Bullet(self.rocket_two, split=0))
        if RocketBaseAction.SPLIT_SHOOT in actions_two:
            self.bullets_two.append(Bullet(self.rocket_two, split=1))

    def generate_asteroid(self):
        if self.ticks_elapsed_since_last_asteroid > self.ticks_to_create_asteroid:
            self.asteroids_neutral.append(Asteroid(self.rocket_one, self.rocket_two, None, None, None))
            self.ticks_elapsed_since_last_asteroid = 0
            if self.ticks_to_create_asteroid > 5:
                self.ticks_to_create_asteroid = self.ticks_to_create_asteroid - 1
        else:
            self.ticks_elapsed_since_last_asteroid = self.ticks_elapsed_since_last_asteroid + 1

    def check_collisions_objects_one(self):
        # Bullets ONE with NEUTRAL asteroids
        for bullet_one in self.bullets_one:
            for asteroid in self.asteroids_neutral:
                # if collides(bullet_one, asteroid):
                if collides(bullet_one, asteroid):
                    self.reward_one += BULLET_ASTEROID_COLLISION_REWARD
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
                    self.reward_one += BULLET_ASTEROID_COLLISION_REWARD
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
        if not ROCKET_ONE_INVULNERABLE:
            for asteroid in self.asteroids_neutral:
                if collides(asteroid, self.rocket_one):
                    self.reward_one += ASTEROID_ROCKET_COLLISION_PENALTY
                    self.asteroids_neutral.remove(asteroid)
                    self.rocket_one.health = self.rocket_one.health - 10

            for asteroid_two in self.asteroids_two:
                if collides(asteroid_two, self.rocket_one):
                    self.reward_one += ASTEROID_ROCKET_COLLISION_PENALTY
                    self.reward_two += ASTEROID_ROCKET_COLLISION_REWARD
                    self.asteroids_two.remove(asteroid_two)
                    self.rocket_one.health = self.rocket_one.health - 30

    def check_collisions_objects_two(self):
        # Bullets TWO with ONE' asteroids
        for bullet_two in self.bullets_two:
            for asteroid_one in self.asteroids_one:
                if collides(bullet_two, asteroid_one):
                    self.reward_two += BULLET_ASTEROID_COLLISION_REWARD
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
                    self.reward_two += BULLET_ASTEROID_COLLISION_REWARD
                    self.asteroids_neutral.remove(asteroid)

                    new_asteroid, new_asteroid_one, new_asteroid_two = None, None, None
                    if bullet_two.split:
                        new_asteroid_one, new_asteroid_two = Asteroid.split_asteroid(bullet_two.rocket,
                                                                                     asteroid,
                                                                                     bullet_two)
                    else:
                        new_asteroid = Asteroid(self.rocket_one, self.rocket_two, asteroid,
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
        if not ROCKET_TWO_INVULNERABLE:
            for asteroid in self.asteroids_neutral:
                if collides(asteroid, self.rocket_two):
                    self.reward_two += ASTEROID_ROCKET_COLLISION_PENALTY
                    self.asteroids_neutral.remove(asteroid)
                    self.rocket_two.health = self.rocket_two.health - 10

            for asteroid_one in self.asteroids_one:
                if collides(asteroid_one, self.rocket_two):
                    self.reward_two += ASTEROID_ROCKET_COLLISION_PENALTY
                    self.reward_one += ASTEROID_ROCKET_COLLISION_REWARD
                    self.asteroids_one.remove(asteroid_one)
                    self.rocket_two.health = self.rocket_two.health - 30

    def check_collisions(self):
        if self.step_count % 2 == 0:
            self.check_collisions_objects_one()
            self.check_collisions_objects_two()
        else:
            self.check_collisions_objects_two()
            self.check_collisions_objects_one()

    def move_objects(self):
        self.rocket_one.move()
        self.rocket_two.move()

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

    def render(self):
        self.draw_modul.clear_display()

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

        self.draw_modul.draw_rocket(self.rocket_one)
        self.draw_modul.draw_rocket(self.rocket_two)

        self.draw_modul.render()

    def check_end(self):
        # Returns (game_is_over, player_one_won)
        if self.rocket_one.health <= 0:
            return True, False
        if self.rocket_two.health <= 0:
            return True, True
        return False, False

    # def get_actions_from_keyboard_input(self):
    #     actions_one = []
    #     actions_two = []
    #     actions = []
    #     events = pygame.event.get(pygame.KEYDOWN)
    #     for event in events:
    #         if(event.key == pygame.K_SPACE):
    #             actions.append(Rocket_action.ROCKET_ONE_SHOOT)
    #             actions_one.append(Rocket_action.ROCKET_ONE_SHOOT)
    #         if(event.key == pygame.K_LCTRL):
    #             actions.append(Rocket_action.ROCKET_TWO_SHOOT)
    #             actions_two.append(Rocket_action.ROCKET_TWO_SHOOT)
    #
    #
    #     all_keys = pygame.key.get_pressed()
    #     if all_keys[pygame.K_UP]:
    #         actions.append(Rocket_action.ROCKET_ONE_ACCELERATE)
    #         actions_one.append(Rocket_action.ROCKET_ONE_ACCELERATE)
    #     if all_keys[pygame.K_LEFT]:
    #         actions.append(Rocket_action.ROCKET_ONE_ROTATE_LEFT)
    #         actions_one.append(Rocket_action.ROCKET_ONE_ROTATE_LEFT)
    #     if all_keys[pygame.K_RIGHT]:
    #         actions.append(Rocket_action.ROCKET_ONE_ROTATE_RIGHT)
    #         actions_one.append(Rocket_action.ROCKET_ONE_ROTATE_RIGHT)
    #
    #
    #     if all_keys[pygame.K_a]:
    #         actions.append(Rocket_action.ROCKET_TWO_ROTATE_LEFT)
    #         actions_two.append(Rocket_action.ROCKET_TWO_ROTATE_LEFT)
    #     if all_keys[pygame.K_d]:
    #         actions.append(Rocket_action.ROCKET_TWO_ROTATE_RIGHT)
    #         actions_two.append(Rocket_action.ROCKET_TWO_ROTATE_RIGHT)
    #     if all_keys[pygame.K_w]:
    #         actions.append(Rocket_action.ROCKET_TWO_ACCELERATE)
    #         actions_two.append(Rocket_action.ROCKET_TWO_ACCELERATE)
    #
    #
    #
    #     # clearing it apparently prevents from stucking
    #     pygame.event.clear()
    #     return actions_one, actions_two
