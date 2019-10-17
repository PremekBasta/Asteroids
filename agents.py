import random
from sprite_object import Rocket_action, Bullet, Rocket_base_action
import pygame
import time
import math

class Agent():
    def __init__(self, player_number):
        super().__init__()
        self.player_number = player_number
        self.shoot_reload_ticks = 0


    def first_impact_neutral_asteroid(self, rocket, neutral_asteroids):
        steps_limit = 60

        for steps_count in range(steps_limit):
            for neutral_asteroid in neutral_asteroids:
                if rocket.collision_rect.colliderect(neutral_asteroid.collision_rect):
                    for neutral_asteroid_reverse in neutral_asteroids:
                        neutral_asteroid_reverse.reverse_move(steps_count)
                    rocket.reverse_move(steps_count)
                    return (neutral_asteroid, steps_count)

            for neutral_asteroid in neutral_asteroids:
                neutral_asteroid.move()

            rocket.move()

        rocket.reverse_move(steps_limit - 1)
        for neutral_asteroid in neutral_asteroids:
            neutral_asteroid.reverse_move(steps_limit - 1)
        return (None, steps_limit + 1)

    def first_impact_enemy_asteroid(self, rocket, enemy_asteroids):
        steps_limit = 60

        # for steps_count in range(steps_limit):
        #     for enemy_asteroid in enemy_asteroids:
        #         if rocket.collision_rect.colliderect(enemy_asteroid.collision_rect):
        #             rocket.reverse_move(steps_count)
        #             ene

    def first_impact_asteroid(self, rocket, neutral_asteroids, enemy_asteroids):
        steps_limit = 60

        for steps_count in range(steps_limit):
            for neutral_asteroid in neutral_asteroids:
                if rocket.collision_rect.colliderect(neutral_asteroid.collision_rect):
                    neutral_asteroid.reverse_move(steps_count)
                    rocket.reverse_move(steps_count)
                    return (neutral_asteroid, steps_count)
            for enemy_asteroid in enemy_asteroids:
                if rocket.collision_rect.colliderect(enemy_asteroid.collision_rect):
                    enemy_asteroid.reverse_move(steps_count)
                    rocket.reverse_move(steps_count)
                    return (enemy_asteroid, steps_count)

            rocket.move()
            for neutral_asteroid in neutral_asteroids:
                neutral_asteroid.move()
            for enemy_asteroid in enemy_asteroids:
                enemy_asteroid.move()

        # Place every object to inital place
        rocket.reverse_move(steps_limit)
        for neutral_asteroid in neutral_asteroids:
            neutral_asteroid.reverse_move(steps_limit)

        for enemy_asteroid in enemy_asteroids:
            enemy_asteroid.reverse_move(steps_count)

        return None, steps_limit + 1

    def shoot_impact_asteroid(self, rocket, asteroid):
        moved_steps = 0
        for steps_count in range(30):
            bullet = Bullet(self.screen, rocket, split=0)

            while bullet.is_alive() and rocket.collision_rect.colliderect(asteroid.collision_rect) == False:
                # Asteroid was shot down
                if bullet.collision_rect.colliderect(asteroid.collision_rect):
                    if steps_count == 0:
                        if rocket.player == 1:
                            return [Rocket_action.ROCKET_ONE_SHOOT]
                        else:
                            return [Rocket_action.ROCKET_TWO_SHOOT]
                    if steps_count < 15:
                        if rocket.player == 1:
                            return [Rocket_action.ROCKET_ONE_ROTATE_LEFT]
                        else:
                            return [Rocket_action.ROCKET_TWO_ROTATE_LEFT]
                    else:
                        if rocket.player == 1:
                            return [Rocket_action.ROCKET_ONE_ROTATE_RIGHT]
                        else:
                            return [Rocket_action.ROCKET_TWO_ROTATE_RIGHT]

                asteroid.move()
                rocket.move()
                bullet.move()
                moved_steps = moved_steps + 1

            del bullet
            asteroid.reverse_move(moved_steps)
            rocket.reverse_move(moved_steps)

            rocket.rotate_left()

    def face_asteroid(self, rocket, asteroid):
        asteroid_angle = asteroid.angle

        target_angle = int(math.atan2(-(asteroid.collision_rect.centery - rocket.collision_rect.centery), (asteroid.collision_rect.centerx - rocket.collision_rect.centerx)) * 180 / math.pi - 90) % 360
        # target_angle = (asteroid_angle + 180) % 360


        # Difference in angles is small enough to shoot
        # Rotation would only increase the difference
        difference = (rocket.angle + 360 - target_angle) % 360
        if difference > 7:
            difference = difference - 360
        if math.fabs(difference) < 7:
            return []

        # Decide rotation direction
        if ((rocket.angle + 360 - target_angle) % 360) < 180:
            return [Rocket_base_action.ROTATE_RIGHT]
        else:
            return [Rocket_base_action.ROTATE_LEFT]

    def simple_shot(self):
        return [Rocket_base_action.SHOT]

    def convert_actions(self, actions):
        ret_actions = []
        self.shoot_reload_ticks = self.shoot_reload_ticks + 1

        # Automatic agents cannot shoot all the time
        if (Rocket_base_action.SHOT in actions and self.shoot_reload_ticks % 5 != 0):
            actions.remove(Rocket_base_action.SHOT)
        if (Rocket_base_action.SPLIT_SHOOT in actions and self.shoot_reload_ticks % 5 != 0):
            actions.remove(Rocket_base_action.SPLIT_SHOOT)

        if self.player_number == 1:
            if Rocket_base_action.ROTATE_LEFT in actions:
                ret_actions.append(Rocket_action.ROCKET_ONE_ROTATE_LEFT)
            if Rocket_base_action.ROTATE_RIGHT in actions:
                ret_actions.append(Rocket_action.ROCKET_ONE_ROTATE_RIGHT)
            if Rocket_base_action.ACCELERATE in actions:
                ret_actions.append(Rocket_action.ROCKET_ONE_ACCELERATE)
            if Rocket_base_action.SHOT in actions:
                ret_actions.append(Rocket_action.ROCKET_ONE_SHOOT)
            if Rocket_base_action.SPLIT_SHOOT in actions:
                ret_actions.append(Rocket_action.ROCKET_ONE_SPLIT_SHOOT)
        else:
            if Rocket_base_action.ROTATE_LEFT in actions:
                ret_actions.append(Rocket_action.ROCKET_TWO_ROTATE_LEFT)
            if Rocket_base_action.ROTATE_RIGHT in actions:
                ret_actions.append(Rocket_action.ROCKET_TWO_ROTATE_RIGHT)
            if Rocket_base_action.ACCELERATE in actions:
                ret_actions.append(Rocket_action.ROCKET_TWO_ACCELERATE)
            if Rocket_base_action.SHOT in actions:
                ret_actions.append(Rocket_action.ROCKET_TWO_SHOOT)
            if Rocket_base_action.SPLIT_SHOOT in actions:
                ret_actions.append(Rocket_action.ROCKET_TWO_SPLIT_SHOOT)

        return ret_actions



class Random_agent(Agent):
    def __init__(self, player_number):
        super().__init__(player_number)
        self.steps = 0

    def choose_actions(self):
        self.steps = self.steps + 1
        actions_numbers = []
        number_of_actions = random.randint(0,3)

        for i in range(number_of_actions):

            action_number = random.randint(1,5)
            while action_number in actions_numbers:
                action_number = random.randint(1, 5)
            actions_numbers.append(action_number)

        if 4 in actions_numbers:
            if self.steps % 4 != 0:
                actions_numbers.remove(4)
        if 5 in actions_numbers:
            if self.steps % 4 != 0:
                actions_numbers.remove(5)

        if self.player_number == 2:
            for i in range(len(actions_numbers)):
                actions_numbers[i] = actions_numbers[i] + 5

        actions = []

        for action_number in actions_numbers:
            actions.append(Rocket_action(int(action_number)))

        return actions

class Stable_defensive_agent(Agent):
    def __init__(self, screen, player_number):
        super().__init__(player_number)
        self.screen = screen
        self.shoot_reload_ticks = 0

    def choose_actions(self, state):
        self.shoot_reload_ticks = self.shoot_reload_ticks + 1

        if self.player_number == 1:
            rocket = state.player_one_rocket
            enemy_asteroids = state.player_two_asteroids
        else:
            rocket = state.player_two_rocket
            enemy_asteroids = state.player_one_asteroids

        impact_asteroid, impact_steps = super().first_impact_asteroid(rocket, state.neutral_asteroids, enemy_asteroids)
        # impact_asteroid, impact_steps = super().first_impact_neutral_asteroid(rocket, state.neutral_asteroids)
        if impact_asteroid is not None:
            pygame.draw.rect(self.screen, (200, 200, 200), impact_asteroid.collision_rect)
            pygame.display.update()
            actions = super().face_asteroid(rocket, impact_asteroid)
            if not actions:
                actions = super().simple_shot()
            actions = super().convert_actions(actions)
            # time.sleep(0.005)
            return actions
        return []

class Defensive_agent(Agent):
    def __init__(self, screen, player_number):
        super().__init__(player_number)
        self.screen = screen

    def choose_actions(self, state):
        if self.player_number == 1:
            rocket = state.player_one_rocket
            enemy_asteroids = state.player_two_asteroids
        else:
            rocket = state.player_two_rocket
            enemy_asteroids = state.player_one_asteroids

        impact_asteroid = super().first_impact_asteroid(rocket, state.neutral_asteroids, enemy_asteroids)
        if impact_asteroid is not None:
            # pygame.draw.rect(self.screen, (200, 200, 200), impact_asteroid[0].collision_rect)
            pygame.display.update()
            time.sleep(0.05)

        actions = Random_agent.choose_actions(Random_agent(self.player_number))
        return actions

class Input_agent(Agent):
    def __init__(self,  screen, player_number):
        super().__init__(player_number)
        self.screen = screen

    def choose_actions(self, state):
        actions_one = []
        actions_two = []
        actions = []
        events = pygame.event.get(pygame.KEYDOWN)


        # if self.player_number == 1:
        #     for event in events:
        #         if event.key == pygame.K_SPACE:
        #             actions.append(Rocket_action.ROCKET_ONE_SHOOT)
        #
        #     all_keys = pygame.key.get_pressed()
        #     if all_keys[pygame.K_UP]:
        #         actions.append(Rocket_action.ROCKET_ONE_ACCELERATE)
        #     if all_keys[pygame.K_LEFT]:
        #         actions.append(Rocket_action.ROCKET_ONE_ROTATE_LEFT)
        #     if all_keys[pygame.K_RIGHT]:
        #         actions.append(Rocket_action.ROCKET_ONE_ROTATE_RIGHT)
        #
        # else:
        #     for event in events:
        #         if event.key == pygame.K_f:
        #             actions.append(Rocket_action.ROCKET_TWO_SHOOT)
        #
        #     all_keys = pygame.key.get_pressed()
        #     if all_keys[pygame.K_a]:
        #         actions.append(Rocket_action.ROCKET_TWO_ROTATE_LEFT)
        #     if all_keys[pygame.K_d]:
        #         actions.append(Rocket_action.ROCKET_TWO_ROTATE_RIGHT)
        #     if all_keys[pygame.K_w]:
        #         actions.append(Rocket_action.ROCKET_TWO_ACCELERATE)


        for event in events:
            if(event.key == pygame.K_KP5):
                actions.append(Rocket_action.ROCKET_ONE_SHOOT)
                actions_one.append(Rocket_action.ROCKET_ONE_SHOOT)
            if(event.key == pygame.K_KP6):
                actions.append(Rocket_action.ROCKET_ONE_SPLIT_SHOOT)
                actions_one.append(Rocket_action.ROCKET_ONE_SPLIT_SHOOT)
            if(event.key == pygame.K_g):
                actions.append(Rocket_action.ROCKET_TWO_SHOOT)
                actions_two.append(Rocket_action.ROCKET_TWO_SHOOT)
            if(event.key == pygame.K_h):
                actions.append(Rocket_action.ROCKET_TWO_SPLIT_SHOOT)
                actions_two.append(Rocket_action.ROCKET_TWO_SPLIT_SHOOT)



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

        if self.player_number == 1:
            rocket = state.player_one_rocket
            enemy_asteroids = state.player_two_asteroids
        else:
            rocket = state.player_two_rocket
            enemy_asteroids = state.player_one_asteroids

        # impact_asteroid, impact_steps = super().first_impact_asteroid(rocket, state.neutral_asteroids, enemy_asteroids)
        # if impact_asteroid is not None:
        #     # pygame.draw.rect(self.screen, (200, 200, 200), impact_asteroid.collision_rect)
        #     # pygame.display.update()
        #     # time.sleep(0.05)
        #     pass

        return actions_one, actions_two
