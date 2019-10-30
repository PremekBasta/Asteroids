import random, copy
from sprite_object import Rocket_action, Bullet, Rocket_base_action, Asteroid
from constants import *
import pygame
import time
import math

class Agent():
    def __init__(self, player_number):
        super().__init__()
        self.player_number = player_number
        self.shoot_reload_ticks = 0

    def assign_objects_to_agent(self, state):
        if self.player_number == 1:
            own_rocket = state.player_one_rocket
            enemy_rocket = state.player_two_rocket
            own_asteroids = state.player_one_asteroids
            enemy_asteroids = state.player_two_asteroids
            own_bullets = state.player_one_bullets
            enemy_bullets = state.player_two_bullets

        else:
            own_rocket = state.player_two_rocket
            enemy_rocket = state.player_one_rocket
            own_asteroids = state.player_two_asteroids
            enemy_asteroids = state.player_one_asteroids
            enemy_bullets = state.player_one_bullets
            own_bullets = state.player_two_bullets

        return own_rocket, enemy_rocket, state.neutral_asteroids, own_asteroids, enemy_asteroids, own_bullets, enemy_bullets

    def evade_asteroid(self, rocket, asteroid):

        rotation_limit = 7
        for left_turns in range(rotation_limit):
            if self.evade_by_accelerating(rocket, asteroid):
                if left_turns == 0:
                    return [Rocket_base_action.ACCELERATE]
                else:
                    return [Rocket_base_action.ROTATE_LEFT]

            rocket.rotate_left()
            rocket.move()
            asteroid.move()

        rocket.rotate_right(rotation_limit)
        rocket.reverse_move(rotation_limit)
        asteroid.reverse_move(rotation_limit)

        return []





    def evade_by_accelerating(self, rocket, asteroid):
        rocket_copy = copy.deepcopy(rocket)
        accelerate_limit = 10
        for accelerate_count in range(accelerate_limit):
            if rocket_copy.collision_rect.colliderect(asteroid.collision_rect):
                asteroid.reverse_move(accelerate_count)
                return False

            rocket_copy.accelerate()
            rocket_copy.move()
            asteroid.move()

        asteroid.reverse_move(accelerate_limit)
        return False

    def first_impact_neutral_asteroid(self, rocket, neutral_asteroids, own_bullets):
        steps_limit = 60
        own_bullets = copy.deepcopy(own_bullets)



        for steps_count in range(steps_limit):
            for neutral_asteroid in neutral_asteroids:
                if rocket.collision_rect.colliderect(neutral_asteroid.collision_rect):
                    for neutral_asteroid_reverse in neutral_asteroids:
                        neutral_asteroid_reverse.reverse_move(steps_count)
                    # for bullet in own_bullets:
                    #     bullet.reverse_move(steps_count)
                    rocket.reverse_move(steps_count)
                    return (neutral_asteroid, steps_count)

            for neutral_asteroid in neutral_asteroids:
                for bullet in own_bullets:
                    if neutral_asteroid.collision_rect.colliderect(bullet.collision_rect):
                        own_bullets.remove(bullet)
                        neutral_asteroids.remove(neutral_asteroid)
                        break

            for neutral_asteroid in neutral_asteroids:
                neutral_asteroid.move()


            for bullet in own_bullets:
                bullet.move()

            rocket.move()

        rocket.reverse_move(steps_limit - 1)
        for neutral_asteroid in neutral_asteroids:
            neutral_asteroid.reverse_move(steps_limit - 1)
        # for bullet in own_bullets:
        #     bullet.reverese_move(steps_limit - 1)
        return (None, steps_limit + 1)

    def first_impact_enemy_asteroid(self, rocket, enemy_asteroids, own_bullets):
        steps_limit = 60

        own_bullets = copy.deepcopy(own_bullets)

        for steps_count in range(steps_limit):
            for enemy_asteroid in enemy_asteroids:
                if rocket.collision_rect.colliderect(enemy_asteroid.collision_rect):
                    for enemy_asteroid_reverse in enemy_asteroids:
                        enemy_asteroid_reverse.reverse_move(steps_count)
                    rocket.reverse_move(steps_count)
                    return(enemy_asteroid, steps_count)

            for enemy_asteroid in enemy_asteroids:
                for bullet in own_bullets:
                    if enemy_asteroid.collision_rect.colliderect(bullet.collision_rect):
                        enemy_asteroids.remove(enemy_asteroid)
                        own_bullets.remove(bullet)
                        break

            for bullet in own_bullets:
                bullet.move()

            for enemy_asteroid in enemy_asteroids:
                enemy_asteroid.move()
            rocket.move()

        rocket.reverse_move(steps_limit - 1)
        for enemy_asteroid in enemy_asteroids:
            enemy_asteroid.reverse_move(steps_limit - 1)
        return(None, steps_limit + 1)

    def unshot_enemy_and_neutral_asteroids(self, own_bullets, enemy_bullets, neutral_asteroids, enemy_asteroids):
        own_bullets_copy = copy.deepcopy(own_bullets)
        enemy_bullets_copy = copy.deepcopy(enemy_bullets)
        neutral_asteroids_copy = copy.deepcopy(neutral_asteroids)
        enemy_asteroids_copy = copy.deepcopy(enemy_asteroids)

        for step in range(BULLET_LIFE_COUNT):
            for neutral_asteroid in neutral_asteroids_copy:
                for own_bullet in own_bullets_copy:
                    if own_bullet.is_alive():
                        if own_bullet.collision_rect.colliderect(neutral_asteroid.collision_rect):
                            neutral_asteroids_copy.remove(neutral_asteroid)
                            own_bullets_copy.remove(own_bullet)

            for enemy_asteroid in enemy_asteroids_copy:
                for own_bullet in own_bullets_copy:
                    if own_bullet.is_alive():
                        if own_bullet.collision_rect.colliderect(enemy_asteroid.collision_rect):
                            enemy_asteroids_copy.remove(enemy_asteroid)
                            own_bullets_copy.remove(own_bullet)


            for neutral_asteroid in neutral_asteroids_copy:
                for enemy_bullet in enemy_bullets_copy:
                    if enemy_bullet.is_alive():
                        if enemy_bullet.collision_rect.colliderect(neutral_asteroid.collision_rect):
                            neutral_asteroids_copy.remove(neutral_asteroid)
                            enemy_bullets_copy.remove(enemy_bullet)

            for own_bullet in own_bullets_copy:
                own_bullet.move()
            for enemy_bullet in enemy_bullets_copy:
                enemy_bullet.move()
            for neutral_asteroid in neutral_asteroids_copy:
                neutral_asteroid.move()
            for enemy_asteroid in enemy_asteroids_copy:
                enemy_asteroid.move()

        for neutral_asteroid in neutral_asteroids_copy:
            neutral_asteroid.reverse_move(BULLET_LIFE_COUNT)
        for enemy_asteroid in enemy_asteroids_copy:
            enemy_asteroid.reverse_move(BULLET_LIFE_COUNT)

        return (neutral_asteroids_copy, enemy_asteroids_copy)



    def shoot_in_all_directions_to_hit_enemy(self, own_rocket, enemy_rocket, neutral_asteroids, enemy_asteroids, own_bullets, enemy_bullets):
        # incrementalni pohyb prostredi
        # mozna bude nutne to postupne vzdy posunout,  vratit a zkusit dalsi

        left_found = False
        # zkusim kruh doleva
        for rotation_count in range(int(360 / 12) ):
            if self.try_shoot_some_asteroid_to_enemy_rocket(own_rocket, enemy_rocket, neutral_asteroids, enemy_asteroids, own_bullets, enemy_bullets):
                left_found, left_steps = True, rotation_count
                break

            own_rocket.rotate_left()
            own_rocket.move()

            enemy_rocket.move()
            for neutral_asteroid in neutral_asteroids:
                neutral_asteroid.move()
            for enemy_asteroid in enemy_asteroids:
                enemy_asteroid.move()

        if left_found:
            back_steps_count = left_steps
        else:
            back_steps_count = 360 / 12

        own_rocket.rotate_right(back_steps_count)
        own_rocket.reverse_move(back_steps_count)

        enemy_rocket.reverse_move(back_steps_count)
        for neutral_asteroid in neutral_asteroids:
            neutral_asteroid.reverse_move(back_steps_count)
        for enemy_asteroid in enemy_asteroids:
            enemy_asteroid.reverse_move(back_steps_count)

        if left_found:
            if left_steps == 0:
                return True, [Rocket_base_action.SHOT], 1
            if left_steps < 15:
                return True, [Rocket_base_action.ROTATE_LEFT], left_steps + 1
            else:
                return True, [Rocket_base_action.ROTATE_RIGHT], 30 - left_steps + 1
        else:
            return False, [], 31


    def try_shoot_some_asteroid_to_enemy_rocket(self, own_rocket, enemy_rocket, neutral_asteroids, enemy_asteroids, own_bullets, enemy_bullets):
        shot, created_asteroid, steps_count = self.shoot_will_hit_asteroid(own_rocket, neutral_asteroids, enemy_asteroids, own_bullets, enemy_bullets)
        if shot and created_asteroid.valid:
            hit, steps_count = self.asteroid_will_hit_rocket(enemy_rocket, created_asteroid)
            return hit
        return False

    def asteroid_will_hit_rocket(self, enemy_rocket, shot_asteroid):
        steps_limit = 100

        for step_count in range(steps_limit):
            if enemy_rocket.collision_rect.colliderect(shot_asteroid.collision_rect):
                enemy_rocket.reverse_move(step_count)
                shot_asteroid.reverse_move(step_count)

                return (True, step_count)

            enemy_rocket.move()
            shot_asteroid.move()

        enemy_rocket.reverse_move(steps_limit - 1)
        shot_asteroid.reverse_move(steps_limit - 1)
        return (False, steps_limit + 1)


    def shoot_will_hit_asteroid(self, own_rocket, neutral_asteroids, enemy_asteroids, own_bullets, enemy_bullets, split = 0):
        bullet = Bullet(self.screen, own_rocket, split=split)
        own_rocket_copy = copy.deepcopy(own_rocket)
        neutral_asteroids_copy = copy.deepcopy(neutral_asteroids)
        enemy_asteroids_copy = copy.deepcopy(enemy_asteroids)
        own_bullets_copy = copy.deepcopy(own_bullets)
        enemy_bullets_copy = copy.deepcopy(enemy_bullets)


        for step_count in range(BULLET_LIFE_COUNT):
            for neutral_asteroid in neutral_asteroids_copy:
                if bullet.collision_rect.colliderect(neutral_asteroid.collision_rect):
                    return (True, Asteroid(self.screen, None, None, neutral_asteroid, own_rocket_copy, bullet), step_count)

                for own_bullet in own_bullets_copy:
                    if own_bullet.collision_rect.colliderect(neutral_asteroid.collision_rect):
                        own_bullets_copy.remove(own_bullet)
                        neutral_asteroids_copy.remove(neutral_asteroid)
                        break



            for enemy_asteroid in enemy_asteroids_copy:
                if bullet.collision_rect.colliderect(enemy_asteroid.collision_rect):
                    return(True, Asteroid(self.screen, None, None, enemy_asteroid, own_rocket_copy, bullet), step_count)

                for own_bullet in own_bullets_copy:
                    if own_bullet.collision_rect.colliderect(enemy_asteroid.collision_rect):
                        own_bullets_copy.remove(own_bullet)
                        enemy_asteroids_copy.remove(enemy_asteroid)
                        break

            bullet.move()
            own_rocket_copy.move()
            for neutral_asteroid in neutral_asteroids_copy:
                neutral_asteroid.move()
            for enemy_asteroid in enemy_asteroids_copy:
                enemy_asteroid.move()
            for own_bullet in own_bullets_copy:
                own_bullet.move()
            for enemy_bullet in enemy_bullets_copy:
                enemy_bullet.move()

        return(False, None, BULLET_LIFE_COUNT + 1)



    def first_impact_asteroid(self, rocket, neutral_asteroids, enemy_asteroids):
        steps_limit = 30

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


class Attacking_agent(Agent):
    def __init__(self, screen, player_number):
        super().__init__(player_number)
        self.screen = screen
        self.shoot_reload_ticks = 0

    def choose_actions(self, state):
        self.shoot_reload_ticks = self.shoot_reload_ticks + 1

        own_rocket, enemy_rocket, neutral_asteroids, own_asteroids, enemy_asteroids, own_bullets, enemy_bullets = super().assign_objects_to_agent(state)

        hit, actions, count = super().shoot_in_all_directions_to_hit_enemy(own_rocket, enemy_rocket,
                                                                           state.neutral_asteroids, enemy_asteroids,
                                                                           own_bullets, enemy_bullets)
        if hit:
            actions = super().convert_actions(actions)

        return actions

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

class Evasion_agent(Agent):
    def __init__(self, screen, player_number):
        super().__init__(player_number)
        self.screen = screen
        self.shoot_reload_ticks = 0

    def choose_actions(self, state):
        own_rocket, enemy_rocket, neutral_asteroids, own_asteroids, enemy_asteroids, own_bullets, enemy_bullets = super().assign_objects_to_agent(state)
        impact_asteroid, step_count = super().first_impact_neutral_asteroid(own_rocket, neutral_asteroids, own_bullets)

        if impact_asteroid is not None:
            actions = super().evade_asteroid(own_rocket, impact_asteroid)
            actions = super().convert_actions(actions)
            return actions
        return []



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
            enemy_bullets = state.player_two_bullets
            own_bullets = state.player_one_bullets
        else:
            rocket = state.player_two_rocket
            enemy_asteroids = state.player_one_asteroids
            enemy_bullets = state.player_one_bullets
            own_bullets = state.player_two_bullets

        # impact_asteroid, impact_steps = super().first_impact_asteroid(rocket, state.neutral_asteroids, enemy_asteroids)
        impact_neutral_asteroid, impact_neutral_asteroid_steps = super().first_impact_neutral_asteroid(rocket, state.neutral_asteroids, own_bullets)
        impact_enemy_asteroid, impact_enemy_asteroid_steps = super().first_impact_enemy_asteroid(rocket, enemy_asteroids, own_bullets)

        if impact_neutral_asteroid_steps < impact_enemy_asteroid_steps:
            impact_asteroid = impact_neutral_asteroid
        elif impact_neutral_asteroid_steps > impact_enemy_asteroid_steps:
            impact_asteroid = impact_enemy_asteroid
        elif impact_neutral_asteroid is None and impact_enemy_asteroid is None:
            return []
        else:
            impact_asteroid = impact_enemy_asteroid

        # pygame.draw.rect(self.screen, (200, 200, 200), impact_asteroid.collision_rect)
        # pygame.display.update()
        # time.sleep(0.005)
        actions = super().face_asteroid(rocket, impact_asteroid)
        if not actions:
            actions = super().simple_shot()
        actions = super().convert_actions(actions)
        # time.sleep(0.005)
        return actions

class Dummy_agent(Agent):
    def __init__(self, screen, player_name):
        super().__init__(player_name)
        self.screen = screen
    def choose_actions(self, state):
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
            own_rocket = state.player_one_rocket
            enemy_rocket = state.player_two_rocket
            own_asteroids = state.player_one_asteroids
            enemy_asteroids = state.player_two_asteroids
            own_bullets = state.player_one_bullets
            enemy_bullets = state.player_two_bullets
        else:
            own_rocket = state.player_two_rocket
            enemy_rocket = state.player_one_rocket
            own_asteroids = state.player_two_asteroids
            enemy_asteroids = state.player_one_asteroids
            own_bullets = state.player_two_bullets
            enemy_bullets = state.player_one_bullets



        # hit, actions, count  = super().shoot_in_all_directions_to_hit_enemy(own_rocket, enemy_rocket, state.neutral_asteroids, enemy_asteroids, own_bullets, enemy_bullets)
        # if hit:
        #     # actions_one = super().convert_actions(actions)
        #     actions_two = super().convert_actions(actions)


        # pygame.draw.rect(self.screen, (200,200,200), own_asteroid.collision_rect)
        # pygame.display.update()
        # time.sleep(0.05)

        # impact_asteroid, impact_steps = super().first_impact_asteroid(rocket, state.neutral_asteroids, enemy_asteroids)
        # if impact_asteroid is not None:
        #     # pygame.draw.rect(self.screen, (200, 200, 200), impact_asteroid.collision_rect)
        #     # pygame.display.update()
        #     # time.sleep(0.05)
        #     pass

        return actions_one, actions_two
