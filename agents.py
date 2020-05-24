import random, copy
from space_objects import Bullet, RocketBaseAction, Asteroid,Rocket, AsteroidSize
from constants import *
import pygame
import time
import math
from dto import collides, Space_object_DTO, copy_object
from enum import Enum
import tensorflow as tf
import numpy as np



class Agent():
    def __init__(self, player_number):
        super().__init__()
        self.input=False
        self.player_number = player_number
        self.shoot_reload_ticks = 0
        self.plan = []
        self.target_asteroid = None
        self.inactiv_ticks = 0
        self.active_ticks = 0
        self.finished_plan = False
        self.finished_plan_attack = False
        self.previous_actions_empty = False
        self.attack_count = 0
        self.evasion_count = 0
        self.defense_count = 0
        self.stop_count = 0


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


    def finish_plan(self):
        if self.finished_plan:
            self.previous_actions_empty = True
        self.finished_plan = True
        self.plan = []
        self.target_asteroid = None

    def store_plan(self, actions):
        self.plan = actions
        #self.finished_plan = False
        self.finished_plan_attack = False
        self.finished_plan_evasion = False
        self.finished_plan_gp = False

    def choose_action_from_plan(self):
        actions = []
        if len(self.plan) > 0:
            actions = self.plan.pop(0)
        else:
            if self.finished_plan:
                self.previous_actions_empty = True
            actions = []
            self.plan = []
            # TODO: added, check
            self.finished_plan = True
            self.finished_plan_attack = True
            self.finished_plan_evasion = True
            self.finished_plan_gp = True

        return actions


    def reevaluate_plan(self):
        if (self.inactiv_ticks > get_inactive_steps_limit()):
        #if (self.inactiv_ticks > INACTIV_STEPS_LIMIT):
            self.inactiv_ticks = 0
            self.previous_actions_empty = False
            self.finished_plan = False
            return True

        if self.finished_plan and not self.previous_actions_empty:
            #self.finished_plan = False
            self.inactiv_ticks = 0
            self.previous_actions_empty = False
            return True


        self.inactiv_ticks = self.inactiv_ticks + 1

        return False


    def two_points_distance_squared(self, pointA, pointB):
        return int(math.pow(pointA[0]-pointB[0], 2)+math.pow(pointA[1]-pointB[1], 2))

    def rocket_asteroid_distance_squared(self, rocket, asteroid):
        ast_x = asteroid.centerx
        ast_y = asteroid.centery

        rocket_x = rocket.centerx
        rocket_y = rocket.centery

        ast_x_width = ast_x + SCREEN_WIDTH
        ast_y_height = ast_y + SCREEN_HEIGHT

        min_distance = self.two_points_distance_squared((ast_x, ast_y), (rocket_x, rocket_y))

        #shift asteroid to + SCREEN_WIDTH
        dist = self.two_points_distance_squared((rocket_x,rocket_y), (ast_x_width, ast_y))
        if dist < min_distance:
            min_distance = dist

        #shift asteroid to + SCREEN_HEIGHT
        dist = self.two_points_distance_squared((rocket_x,rocket_y), (ast_x, ast_y_height))
        if dist < min_distance:
            min_distance = dist

        #shift asteroid to + SCREEN_HEIGHT and + SCREEN_WIDTH
        dist = self.two_points_distance_squared((rocket_x, rocket_y), (ast_x_width, ast_y_height))
        if dist < min_distance:
            min_distance = dist

        return min_distance

    def object_object_vector(self, objA, objB):
        return [objA.centerx - objB.centerx, objA.centery - objB.centery]

    def number_of_asteroids_in_range(self, rocket, neutral_asteroids, enemy_asteroids, range=ENEMY_ASTEROIDS_RADIUS):
        range_squared = range * range
        number_of_asteroids = 0
        for neutral_asteroid in neutral_asteroids:
            if self.rocket_asteroid_distance_squared(rocket, neutral_asteroid) < range_squared:
                number_of_asteroids +=1

        for enemy_asteroid in enemy_asteroids:
            if self.rocket_asteroid_distance_squared(rocket, enemy_asteroid) < range_squared:
                number_of_asteroids += 1
        return number_of_asteroids

    def find_N_closest_asteroids(self, rocket, neutral_asteroids, enemy_asteroids, N=3):
        arr = []
        for neutral_asteroid in neutral_asteroids:
            arr.append([self.object_object_vector(neutral_asteroid, rocket),
                        self.rocket_asteroid_distance_squared(rocket, neutral_asteroid)])

        for enemy_asteroid in enemy_asteroids:
            arr.append([self.object_object_vector(enemy_asteroid, rocket),
                        self.rocket_asteroid_distance_squared(rocket, enemy_asteroid)])

        sorted_by_distance = sorted(arr, key=lambda x: x[1])

        if len(sorted_by_distance) < N:
            for i in range(N-len(sorted_by_distance)):
                sorted_by_distance.append([(SCREEN_WIDTH, SCREEN_HEIGHT), SCREEN_FULL_DISTANCE_SQUARED])


        return sorted_by_distance[0:N]

    def low_level_state_info(self, state, N_nearest_asteroids = 3):
        # self speed, self angle, self shoot cooldown, enemy vector, enemy speed, N nearest asteroids vectors

        own_rocket, enemy_rocket, neutral_asteroids, own_asteroids, enemy_asteroids, own_bullets, enemy_bullets \
            = self.assign_objects_to_agent(state)

        own_rocket_speed = [own_rocket.speedx, own_rocket.speedy]
        own_rocket_angle = [own_rocket.angle]
        own_rocket_shoot_ticks = [self.shoot_reload_ticks]

        enemy_rocket_vector = self.object_object_vector(own_rocket, enemy_rocket)
        enemy_speed = [enemy_rocket.speedx, enemy_rocket.speedy]
        near_asteroids = self.find_N_closest_asteroids(own_rocket, neutral_asteroids, enemy_asteroids, N=3)

        asteroids_positions = []
        for near_asteroid in near_asteroids:
            asteroids_positions.append(near_asteroid[0][0])
            asteroids_positions.append(near_asteroid[0][1])

        result = np.array(own_rocket_speed +
                          own_rocket_angle +
                          own_rocket_shoot_ticks +
                          enemy_rocket_vector +
                          enemy_speed +
                          asteroids_positions)

        result = np.reshape(result, newshape=(1, -1))

        return result



    def evade_asteroid(self, rocket, asteroid):

        rocket_copy = copy_object(rocket)
        asteroid_copy = copy_object(asteroid)

        rotation_limit = 15
        for left_turns in range(0, rotation_limit):
            evaded, accelerate_steps = self.evade_by_continual_accelerating(rocket_copy, asteroid_copy)
            if evaded:
                if left_turns == 0:
                    plan = [[RocketBaseAction.ACCELERATE] for i in range(accelerate_steps)]
                    return plan, accelerate_steps
                elif left_turns < 15:
                    plan = [[RocketBaseAction.ROTATE_LEFT] for i in range(left_turns)]
                    plan.extend([[RocketBaseAction.ACCELERATE] for i in range(accelerate_steps)])
                    return plan, left_turns + accelerate_steps

            #if self.evade_by_accelerating(rocket_copy, asteroid_copy):
            #    if left_turns == 0:
            #        plan = [[RocketBaseAction.ACCELERATE] for i in range(10)]
            #        return plan, 5
            #    elif left_turns < 15:
            #        plan = [[RocketBaseAction.ROTATE_LEFT] for i in range(left_turns)]
            #        plan.extend([[RocketBaseAction.ACCELERATE, RocketBaseAction.ROTATE_LEFT] for i in range(10)])
            #        return plan, left_turns + 5

            rocket_copy.rotate_left()
            rocket_copy.move()
            asteroid_copy.move()

        rocket_copy = copy_object(rocket)
        asteroid_copy = copy_object(asteroid)
        for right_turns in range(0, rotation_limit):
            evaded, accelerate_steps = self.evade_by_continual_accelerating(rocket_copy, asteroid_copy)
            if evaded:
                if right_turns == 0:
                    plan = [[RocketBaseAction.ACCELERATE] for i in range(accelerate_steps)]
                    return plan, accelerate_steps
                elif right_turns < 15:
                    plan = [[RocketBaseAction.ROTATE_RIGHT] for i in range(right_turns)]
                    plan.extend([[RocketBaseAction.ACCELERATE] for i in range(accelerate_steps)])
                    return plan, right_turns + accelerate_steps

            #if self.evade_by_accelerating(rocket_copy, asteroid_copy):
            #    plan = [[RocketBaseAction.ROTATE_RIGHT] for i in range(right_turns)]
            #    plan.extend([[RocketBaseAction.ACCELERATE, RocketBaseAction.ROTATE_RIGHT] for i in range(10)])
            #    return plan, right_turns + 5

            rocket_copy.rotate_right()
            rocket_copy.move()
            asteroid_copy.move()

        return [], NOT_FOUND_STEPS_COUNT

    def stop_moving(self, rocket):
        rocket_copy = copy_object(rocket)

        if (math.fabs(rocket_copy.speedx) + math.fabs(rocket_copy.speedy)) < 16:
            return False, [], 0

        if rocket_copy.speedx == 0:
            if rocket_copy.speedy > 0:
                move_angle = 270
            elif rocket_copy.speedy < 0:
                move_angle = 90
        else:
            move_angle = (math.atan(- rocket_copy.speedy / rocket_copy.speedx) * 180) / math.pi
            if rocket_copy.speedx < 0:
                move_angle = move_angle + 180
            move_angle = move_angle % 360

        reverse_angle = (move_angle + 180 - 90) % 360

        left_turns = 0
        right_turns = 0
        if ((reverse_angle + 360 - rocket_copy.angle) % 360) < 180:
            left_turns = int(((reverse_angle + 360 - rocket_copy.angle) % 360) // 12)
        else:
            right_turns = int((360 - ((reverse_angle + 360 - rocket_copy.angle) % 360)) // 12)


        rocket_copy.rotate_left(left_turns)
        rocket_copy.rotate_right(right_turns)

        accelerate_count = 0

        while (math.fabs(rocket_copy.speedx) + math.fabs(rocket_copy.speedy)) > 14 and accelerate_count < 10:
            rocket_copy.accelerate()
            accelerate_count = accelerate_count + 1

        actions = []

        if left_turns > 0:
            actions = [[RocketBaseAction.ROTATE_LEFT] for i in range(left_turns)]
        if right_turns > 0:
            actions = [[RocketBaseAction.ROTATE_RIGHT] for i in range(right_turns)]

        for i in range(accelerate_count):
            actions.append([RocketBaseAction.ACCELERATE])
        return True, actions, left_turns + right_turns + accelerate_count


    def evade_by_continual_accelerating(self, rocket, asteroid):
        # how many maximal times can rocket accelerate in attemp to avoid asteroid
        accelerate_limit = 20
        # how many steps it is checking whether they collided or rocket escaped
        evade_steps_limit = 20
        for accelerate_count in range(accelerate_limit):
            rocket_copy = copy_object(rocket)
            asteroid_copy = copy_object(asteroid)
            collided = False
            for step_number in range(evade_steps_limit):
                if collides(rocket_copy, asteroid_copy):
                    collided = True
                    break
                if step_number < accelerate_count:
                    rocket_copy.accelerate()
                #rocket_copy.health_bar_color = PLAYER_TWO_COLOR
                #draw_module.draw_rocket_only(rocket_copy)
                #draw_module.draw_circle((rocket_copy.centerx, rocket_copy.centery))
                #draw_module.draw_circle((asteroid_copy.centerx, asteroid_copy.centery))
                #draw_module.render()
                #pygame.draw.circle(self.screen, (0, 0, 0, 0), (rocket_copy.centerx, rocket_copy.centery), 10)
                #pygame.draw.circle(self.screen, (0, 0, 0, 0), (asteroid_copy.centerx, asteroid_copy.centery), 10)
                #pygame.display.update()
                rocket_copy.move()
                asteroid_copy.move()
            if not collided:
                return True, accelerate_count
        return False, NOT_FOUND_STEPS_COUNT


    def evade_by_accelerating(self, rocket, asteroid):
        rocket_copy = copy_object(rocket)
        asteroid_copy = copy_object(asteroid)
        accelerate_limit = 20
        for accelerate_count in range(accelerate_limit):
            if collides(rocket_copy, asteroid_copy):
                # time.sleep(0.2)
                return False

            # pygame.draw.circle(self.screen, (255,0,0), (asteroid_copy.centerx, asteroid_copy.centery), asteroid_copy.radius)
            # pygame.draw.circle(self.screen, (0, 255, 0), (rocket_copy.centerx, rocket_copy.centery), rocket_copy.radius)
            # pygame.display.update()

            rocket_copy.accelerate()
            rocket_copy.move()
            asteroid_copy.move()

        # time.sleep(0.2)

        return True

    def first_impact_neutral_asteroid_numpy(self, rocket, neutral_asteroids, own_bullets):
        steps_limit = 60
        (ret_ast, ret_count) = (None, steps_limit + 1)

        if len(neutral_asteroids) == 0:
            return (None, steps_limit + 1)



        asteroids_pos = np.array([[neutral_asteroid.centerx, neutral_asteroid.centery] for neutral_asteroid in neutral_asteroids])
        asteroids_speed = np.array([[neutral_asteroid.speedx, neutral_asteroid.speedy] for neutral_asteroid in neutral_asteroids])
        asteroids_radii = np.array([neutral_asteroid.radius for neutral_asteroid in neutral_asteroids])

        own_bullets_pos = np.array([[bullet.centerx, bullet.centery] for bullet in own_bullets])
        own_bullets_speed = np.array([[bullet.speedx, bullet.speedy] for bullet in own_bullets])
        own_bullets_radii = np.array([bullet.radius for bullet in own_bullets])


        # Soucet polomeru Asteroid x strela
        radii = np.add(asteroids_radii[:, np.newaxis], own_bullets_radii)

        asteroids_rocket_differences = np.zeros((len(neutral_asteroids), 2))

        if (len(own_bullets) > 0):
            asteroids_bullets_differences = np.zeros((len(neutral_asteroids), len(own_bullets), 2))



        for steps_count in range(steps_limit):
            # ASTEROID -- ROCKET collisions
            # Odecitam to oboustrane, protoze tim, ze se pohybuju v uzavrenem souradnicovem prostoru 0-900 x 0-600,
            # tak mi jednostrane odecitani nemusi dat jejich nejmensi rozdily v souradnicich
            np.minimum(np.mod(np.subtract(asteroids_pos, [rocket.centerx, rocket.centery]), MOD_VAL),
                       np.mod(np.subtract([rocket.centerx, rocket.centery], asteroids_pos), MOD_VAL),
                            out = asteroids_rocket_differences)



            ast_rocket_distances = np.linalg.norm(asteroids_rocket_differences, axis=1)
            itemindex = np.where(ast_rocket_distances < asteroids_radii + rocket.radius)
            if len(itemindex[0]) > 0:
                index_of_ast_np = itemindex[0][0]
                ret_ast = neutral_asteroids[index_of_ast_np]
                ret_count = steps_count
                break


            # ASTEROID -- BULLET collisions
            if (len(own_bullets)>0):
                np.minimum(np.mod(np.subtract(asteroids_pos[:, np.newaxis], own_bullets_pos), MOD_VAL),
                           np.mod(np.subtract(own_bullets_pos, asteroids_pos[:, np.newaxis]), MOD_VAL),
                                out = asteroids_bullets_differences)



                ast_bullets_distances = np.linalg.norm(asteroids_bullets_differences, axis=2)
                itemindex = np.where(ast_bullets_distances < radii)
                if len(itemindex[0]>0):
                    # nastavim strele a asteroidu, ktere se srazili, zaporny polomer == uz se nemohou s nicim srazit v dalsim kroku
                    radii[itemindex[0][0], :] = -100
                    radii[:, itemindex[1][0]] = -100
                    asteroids_radii[itemindex[0][0]] = -100

                own_bullets_pos = np.add(own_bullets_pos, own_bullets_speed)
                own_bullets_pos = np.mod(own_bullets_pos, MOD_VAL)


            asteroids_pos = np.add(asteroids_pos, asteroids_speed)
            asteroids_pos = np.mod(asteroids_pos, MOD_VAL)

        return (ret_ast, ret_count)



    def first_impact_neutral_asteroid(self, rocket, neutral_asteroids, own_bullets):
        steps_limit = IMPACT_RADIUS

        own_bullets_copy = [copy_object(own_bullet) for own_bullet in own_bullets]
        neutral_asteroids_copy = [copy_object(neutral_asteroid) for neutral_asteroid in neutral_asteroids]
        neutral_asteroids_copy2 = [copy_object(neutral_asteroid) for neutral_asteroid in neutral_asteroids]
        rocket_copy = copy_object(rocket)

        for neutral_asteroid in neutral_asteroids_copy:
            neutral_asteroid.valid = True


        for steps_count in range(steps_limit):

            # pygame.draw.circle(self.screen, (0, 255, 0), (rocket_copy.centerx, rocket_copy.centery), rocket_copy.radius)

            for neutral_asteroid in neutral_asteroids_copy:
                # pygame.draw.circle(self.screen, (255, 0, 0), (neutral_asteroid.centerx, neutral_asteroid.centery),
                #                    neutral_asteroid.radius)
                if collides(rocket_copy, neutral_asteroid):
                    for neutral_asteroid_reverse in neutral_asteroids_copy:
                        neutral_asteroid_reverse.reverse_move(steps_count)

                    return (neutral_asteroid, steps_count)

            for neutral_asteroid in neutral_asteroids_copy:
                    for bullet in own_bullets_copy:
                        if collides(neutral_asteroid, bullet):
                            own_bullets_copy.remove(bullet)
                            neutral_asteroids_copy.remove(neutral_asteroid)
                            break

            for neutral_asteroid in neutral_asteroids_copy:
                neutral_asteroid.move()


            for bullet in own_bullets_copy:
                bullet.move()


            rocket_copy.move()

        return (None, steps_limit + 1)

    def first_impact_enemy_asteroid(self, rocket, enemy_asteroids, own_bullets):
        steps_limit = IMPACT_RADIUS


        own_bullets_copy = [copy_object(own_bullet) for own_bullet in own_bullets]
        rocket_copy = copy_object(rocket)
        enemy_asteroids_copy = [copy_object(enemy_asteroid) for enemy_asteroid in enemy_asteroids]

        for steps_count in range(steps_limit):
            for enemy_asteroid in enemy_asteroids_copy:
                # if rocket.collision_rect.colliderect(enemy_asteroid.collision_rect):
                if collides(rocket_copy, enemy_asteroid):
                    for enemy_asteroid_reverse in enemy_asteroids_copy:
                        enemy_asteroid_reverse.reverse_move(steps_count)
                    # rocket.reverse_move(steps_count)
                    return(enemy_asteroid, steps_count)

            for enemy_asteroid in enemy_asteroids_copy:
                for bullet in own_bullets_copy:
                    # if enemy_asteroid.collision_rect.colliderect(bullet.collision_rect):
                    if collides(enemy_asteroid, bullet):
                        enemy_asteroids_copy.remove(enemy_asteroid)
                        own_bullets_copy.remove(bullet)
                        break

            for bullet in own_bullets_copy:
                bullet.move()

            for enemy_asteroid in enemy_asteroids_copy:
                enemy_asteroid.move()
            rocket_copy.move()

        # rocket.reverse_move(steps_limit - 1)
        for enemy_asteroid in enemy_asteroids_copy:
            enemy_asteroid.reverse_move(steps_limit - 1)
        return(None, steps_limit + 1)

    def unshot_enemy_and_neutral_asteroids(self, own_bullets, enemy_bullets, neutral_asteroids, enemy_asteroids):
        own_bullets_copy = [copy_object(own_bullet) for own_bullet in own_bullets]
        enemy_bullets_copy = [copy_object(enemy_bullet) for enemy_bullet in enemy_bullets]
        neutral_asteroids_copy = [copy_object(neutral_asteroid) for neutral_asteroid in neutral_asteroids]
        enemy_asteroids_copy = [copy_object(enemy_asteroid) for enemy_asteroid in enemy_asteroids]

        for step in range(BULLET_LIFE_COUNT):
            for neutral_asteroid in neutral_asteroids_copy:
                for own_bullet in own_bullets_copy:
                    if own_bullet.is_alive():
                        if collides(own_bullet, neutral_asteroid):
                        # if own_bullet.collision_rect.colliderect(neutral_asteroid.collision_rect):
                            neutral_asteroids_copy.remove(neutral_asteroid)
                            own_bullets_copy.remove(own_bullet)

            for enemy_asteroid in enemy_asteroids_copy:
                for own_bullet in own_bullets_copy:
                    if own_bullet.is_alive():
                        if collides(own_bullet, enemy_asteroid):
                        # if own_bullet.collision_rect.colliderect(enemy_asteroid.collision_rect):
                            enemy_asteroids_copy.remove(enemy_asteroid)
                            own_bullets_copy.remove(own_bullet)


            for neutral_asteroid in neutral_asteroids_copy:
                for enemy_bullet in enemy_bullets_copy:
                    if enemy_bullet.is_alive():
                        if collides(enemy_bullet, neutral_asteroid):
                        # if enemy_bullet.collision_rect.colliderect(neutral_asteroid.collision_rect):
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

        own_rocket_copy = copy_object(own_rocket)
        enemy_rocket_copy = copy_object(enemy_rocket)
        neutral_asteroids_copy = [copy_object(neutral_asteroid) for neutral_asteroid in neutral_asteroids]
        # enemy_asteroids_copy = [copy_object(enemy_asteroid) for enemy_asteroid in enemy_asteroids]
        enemy_asteroids_copy = [copy_object(enemy_asteroid) for enemy_asteroid in enemy_asteroids if enemy_asteroid.size_index != AsteroidSize.SMALL]
        own_bullets_copy = [copy_object(own_bullet) for own_bullet in own_bullets]
        enemy_bullets_copy = [copy_object(enemy_bullet) for enemy_bullet in enemy_bullets]

        shoot_type = RocketBaseAction.SHOT


        left_found = False
        # zkouším postupně všechny rotace vlevo
        for rotation_count in range(int(360 / 12)):
            # if self.try_shoot_some_asteroid_to_enemy_rocket(own_rocket, enemy_rocket, neutral_asteroids, enemy_asteroids, own_bullets, enemy_bullets):
            #     left_found, left_steps = True, rotation_count
            #     break

            hit, shoot_type = self.try_shoot_some_asteroid_to_enemy_rocket(own_rocket_copy, enemy_rocket_copy, neutral_asteroids_copy, enemy_asteroids_copy, own_bullets_copy, enemy_bullets_copy)
            if hit:
                left_found, left_steps = True, rotation_count
                break


            own_rocket_copy.rotate_left()
            own_rocket_copy.move()

            enemy_rocket_copy.move()
            for neutral_asteroid in neutral_asteroids_copy:
                neutral_asteroid.move()
            for enemy_asteroid in enemy_asteroids_copy:
                enemy_asteroid.move()

        plan = []

        if left_found:
            if left_steps == 0:
                return True, [[shoot_type]], 1
            if left_steps < 15:
                for i in range(left_steps):
                    plan.append([RocketBaseAction.ROTATE_LEFT])
                plan.append([shoot_type])
                return True, plan, left_steps + 1
            else:
                for i in range(30 - left_steps):
                    plan.append([RocketBaseAction.ROTATE_RIGHT])
                plan.append([shoot_type])
                return True, plan, 30 - left_steps + 1
        else:
            return False, [], NOT_FOUND_STEPS_COUNT


    def try_shoot_some_asteroid_to_enemy_rocket(self, own_rocket, enemy_rocket, neutral_asteroids, enemy_asteroids, own_bullets, enemy_bullets):
        # shot, created_asteroid, steps_count = self.shoot_will_hit_asteroid(own_rocket, neutral_asteroids, enemy_asteroids, own_bullets, enemy_bullets)
        # if shot and created_asteroid.valid:
        #     hit, steps_count = self.asteroid_will_hit_rocket(enemy_rocket, created_asteroid)
        #     return hit




        shot, bullet, impact_asteroid, steps_count = self.shoot_will_hit_asteroid(own_rocket, neutral_asteroids, enemy_asteroids, own_bullets, enemy_bullets)
        if shot:
            created_asteroid_single = Asteroid(None, None, impact_asteroid, own_rocket, bullet)
            if created_asteroid_single.valid:
                hit, steps_count = self.asteroid_will_hit_rocket(enemy_rocket, created_asteroid_single)
                if hit:
                    return True, RocketBaseAction.SHOT

            created_asteroid_split_one, created_asteroid_split_two = Asteroid.split_asteroid(own_rocket, impact_asteroid, bullet)
            if created_asteroid_split_one is not None:
                hit, steps_count = self.asteroid_will_hit_rocket(enemy_rocket, created_asteroid_split_one)
                if hit:
                    return True, RocketBaseAction.SPLIT_SHOOT

            if created_asteroid_split_two is not None:
                hit, steps_count = self.asteroid_will_hit_rocket(enemy_rocket, created_asteroid_split_two)
                if hit:
                    return True, RocketBaseAction.SPLIT_SHOOT

        return False, RocketBaseAction.SHOT


    def asteroid_will_hit_rocket(self, enemy_rocket, shot_asteroid):
        steps_limit = 100

        for step_count in range(steps_limit):
            # if collides_numba(enemy_rocket.centerx, enemy_rocket.centery, shot_asteroid.centerx, shot_asteroid.centery,
            #                   enemy_rocket.radius, shot_asteroid.radius):
            if collides(enemy_rocket, shot_asteroid):
                enemy_rocket.reverse_move(step_count)
                shot_asteroid.reverse_move(step_count)

                return (True, step_count)

            enemy_rocket.move()
            shot_asteroid.move()

        enemy_rocket.reverse_move(steps_limit - 1)
        shot_asteroid.reverse_move(steps_limit - 1)
        return (False, steps_limit + 1)

    def shoot_will_hit_explicit_asteroid(self, rocket, asteroid):
        bullet = Bullet(rocket)
        asteroid_copy = copy_object(asteroid)

        for step_count in range(BULLET_LIFE_COUNT):
            if collides(bullet, asteroid_copy):
                return True

            bullet.move()
            asteroid_copy.move()
        return False

    def shoot_will_hit_asteroid(self, own_rocket, neutral_asteroids, enemy_asteroids, own_bullets, enemy_bullets, split = 0):
        bullet = Bullet(own_rocket, split=split)

        # neutral_asteroids_risk = [neutral_asteroid for neutral_asteroid in neutral_asteroids if self.risk_of_collision(neutral_asteroid, bullet)]
        # enemy_asteroids_risk = [enemy_asteroid for enemy_asteroid in enemy_asteroids if self.risk_of_collision(enemy_asteroid, bullet)]
        #
        # for neutral_asteroid in neutral_asteroids_risk:
        #     pygame.draw.circle(self.screen, (255, 255, 255), (neutral_asteroid.centerx, neutral_asteroid.centery), 30, 3)
        #
        # for enemy_asteroid in enemy_asteroids_risk:
        #     pygame.draw.circle(self.screen, (255, 255, 255), (enemy_asteroid.centerx, enemy_asteroid.centery), 30,
        #                        3)
        #
        # pygame.draw.line(self.screen, (255,255,255), (bullet.centerx, bullet.centery), (bullet.centerx + 10*bullet.speedx, bullet.centery + 10* bullet.speedy),5)
        #
        # events = pygame.event.get(pygame.KEYDOWN)
        # all_keys = pygame.key.get_pressed()
        # if all_keys[pygame.K_d] and self.player_number == 1:
        #     pygame.display.update()
        #     time.sleep(0.5)



        # own_rocket_copy = Space_object_DTO(own_rocket.radius, own_rocket.centerx, own_rocket.centery, own_rocket.speedx,
        #                                  own_rocket.speedy, own_rocket.angle, own_rocket.size_index, own_rocket.player)
        own_rocket_copy = copy_object(own_rocket)
        neutral_asteroids_copy = [copy_object(neutral_asteroid) for neutral_asteroid in neutral_asteroids]
        enemy_asteroids_copy = [copy_object(enemy_asteroid) for enemy_asteroid in enemy_asteroids]
        own_bullets_copy = [copy_object(own_bullet) for own_bullet in own_bullets]
        enemy_bullets_copy = [copy_object(enemy_bullet) for enemy_bullet in enemy_bullets]

        # neutral_asteroids_copy = [copy_object(neutral_asteroid) for neutral_asteroid in neutral_asteroids if self.risk_of_collision(neutral_asteroid, bullet)]
        # enemy_asteroids_copy = [copy_object(enemy_asteroid) for enemy_asteroid in enemy_asteroids if self.risk_of_collision(enemy_asteroid, bullet)]





        for step_count in range(BULLET_LIFE_COUNT):
            for neutral_asteroid in neutral_asteroids_copy:
                if collides(bullet, neutral_asteroid):
                    return (True, bullet, neutral_asteroid, step_count)

                for own_bullet in own_bullets_copy:
                    if collides(own_bullet, neutral_asteroid):
                        own_bullets_copy.remove(own_bullet)
                        neutral_asteroids_copy.remove(neutral_asteroid)
                        break



            for enemy_asteroid in enemy_asteroids_copy:
                if collides(bullet, enemy_asteroid):
                    # return(True, Asteroid(self.screen, None, None, enemy_asteroid, own_rocket_copy, bullet), step_count)
                    return(True, bullet, enemy_asteroid, step_count)

                for own_bullet in own_bullets_copy:
                    # if collides_numba(own_bullet.centerx, own_bullet.centery, enemy_asteroid.centerx, enemy_asteroid.centery,
                    #                   own_bullet.radius, enemy_asteroid.radius):
                    if collides(own_bullet, enemy_asteroid):
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

        return(False, None, None, BULLET_LIFE_COUNT + 1)



    def first_impact_asteroid(self, own_rocket, neutral_asteroids, own_bullets, enemy_asteroids):
        impact_neutral_asteroid, impact_neutral_asteroid_steps = self.first_impact_neutral_asteroid(own_rocket, neutral_asteroids, own_bullets)
        impact_enemy_asteroid, impact_enemy_asteroid_steps = self.first_impact_enemy_asteroid(own_rocket,
                                                                                                 enemy_asteroids,
                                                                                                 own_bullets)

        if impact_neutral_asteroid_steps < impact_enemy_asteroid_steps:
            impact_asteroid = impact_neutral_asteroid
            impact_steps = impact_neutral_asteroid_steps
        elif impact_neutral_asteroid_steps > impact_enemy_asteroid_steps:
            impact_asteroid = impact_enemy_asteroid
            impact_steps = impact_enemy_asteroid_steps
        elif impact_neutral_asteroid is None and impact_enemy_asteroid is None:
            return False, None, IMPACT_RADIUS + 1
        else:
            impact_asteroid = impact_enemy_asteroid
            impact_steps = impact_enemy_asteroid_steps

        return True, impact_asteroid, impact_steps

    def recalculate_target_position(self, rocket, asteroid):
        a1 = [rocket.centerx, rocket.centery]
        a2 = [rocket.centerx + rocket.speedx, rocket.centery + rocket.speedy]
        b1 = [asteroid.centerx, asteroid.centery]
        b2 = [asteroid.centerx + asteroid.speedx, asteroid.centery + asteroid.speedy]

        if a1 == a2 or b1 == b2:
            (target_x, target_y) = b1
        else:
            (intersection_x, intersection_y), found = self.get_intersect(a1, a2, b1, b2)
            target_x = int(intersection_x * 0.15 + asteroid.centerx * 0.85)
            target_y = int(intersection_y * 0.15 + asteroid.centery * 0.85)


        temp_x, temp_y = target_x, target_y
        # Try
        distance = self.distance(temp_x, rocket.centerx, temp_y, rocket.centery)

        # -x
        temp_x = temp_x - SCREEN_WIDTH
        temp_distance = self.distance(temp_x, rocket.centerx, temp_y, rocket.centery)
        if temp_distance < distance:
            target_x = temp_x
            distance = temp_distance
        temp_x = temp_x + SCREEN_WIDTH

        # -y
        temp_y = temp_y - SCREEN_HEIGHT
        temp_distance = self.distance(temp_x, rocket.centerx, temp_y, rocket.centery)
        if temp_distance < distance:
            target_y = temp_y
            distance = temp_distance
        temp_y = temp_distance + SCREEN_HEIGHT

        # -x -y
        temp_x = temp_x - SCREEN_WIDTH
        temp_y = temp_y - SCREEN_HEIGHT
        temp_distance = self.distance(temp_x, rocket.centerx, temp_y, rocket.centery)
        if temp_distance < distance:
            target_y = temp_y
            target_x = temp_x

        asteroid.centerx, asteroid.centery = target_x, target_y

    def distance(self,x1, x2, y1, y2):
        return math.sqrt(math.pow(x1-x2, 2) + math.pow(y1 - y2, 2))

    def risk_of_collision(self, objectA, objectB):

        found, (pointx, pointy) = self.intersect_point(objectA, objectB)
        if found:
            if objectA.speedx == 0:
                steps_A = 1000
            else:
                steps_A = (pointx - objectA.centerx) / objectA.speedx

            if objectB.speedx == 0:
                steps_B = - 1000
            else:
                steps_B = - (pointx - objectB.centerx) / objectB.speedx

            if math.fabs(steps_A - steps_B) < 60:
                return True
            return False
        return True

    def intersect_point(self,objectA, objectB):
        c1 = objectA.speedy * objectA.centerx - objectA.speedx * objectA.centery
        a1 = -objectA.speedy
        b1 = objectA.speedx

        c2 = objectB.speedy * objectB.centerx - objectB.speedx * objectB.centery
        a2 = -objectB.speedy
        b2 = objectB.speedx



        if a1 == 0:
            if (a1*b2 - a2*b1 != 0):
                x = objectB.centerx
                y = (-a1*c2 + a2*c1)/(a1*b2 - a2*b1)
                return True, (int(x),int(y))
            return False, (0,0)
        if (a1*b2 - a2*b1 == 0):
            return False, (0,0)

        x = (-c1 - b1*((-a1*c2 + a2*c1)/(a1*b2 - a2*b1))) / a1
        y = (-a1*c2 + a2*c1)/(a1*b2 - a2*b1)

        return True, (int(x), int(y))

    def get_intersect(self, a1, a2, b1, b2):
        """
        Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
        a1: [x, y] a point on the first line
        a2: [x, y] another point on the first line
        b1: [x, y] a point on the second line
        b2: [x, y] another point on the second line
        """
        s = np.vstack([a1, a2, b1, b2])  # s for stacked
        h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
        l1 = np.cross(h[0], h[1])  # get first line
        l2 = np.cross(h[2], h[3])  # get second line
        x, y, z = np.cross(l1, l2)  # point of intersection
        if z == 0:  # lines are parallel
            return (float('inf'), float('inf')), False
        return (x / z, y / z), True

    def defense_shoot_asteroid_actions(self, rocket, asteroid):
        if self.shoot_will_hit_explicit_asteroid(rocket, asteroid):
            return [[RocketBaseAction.SHOT]], 1
        else:
            return self.face_asteroid(rocket, asteroid)

    def face_asteroid(self, rocket, asteroid):
        asteroid_angle = asteroid.angle

        target_angle = int(math.atan2(-(asteroid.centery - rocket.centery), (asteroid.centerx - rocket.centerx)) * 180 / math.pi - 90) % 360


        # Difference in angles is small enough to shoot
        # Rotation would only increase the difference
        difference = (rocket.angle + 360 - target_angle) % 360
        if difference > 7:
            difference = difference - 360
        if math.fabs(difference) < 7:
            return [], 0


        temp_rocket_angle = rocket.angle
        number_of_rotation = 0
        actions = []
        # Decide rotation direction
        if ((rocket.angle + 360 - target_angle) % 360) < 180:
            while (rocket.angle + 360 - target_angle) % 360 > 11:
                rocket.rotate_right()
                number_of_rotation = number_of_rotation + 1

            for i in range(number_of_rotation):
                actions.append([RocketBaseAction.ROTATE_RIGHT])

            actions.append([RocketBaseAction.SHOT])

            rocket.angle = temp_rocket_angle

            return actions, number_of_rotation + 1
        else:
            while (rocket.angle + 360 - target_angle) % 360 > 11:
                rocket.rotate_left()
                number_of_rotation = number_of_rotation + 1

            for i in range(number_of_rotation):
                actions.append([RocketBaseAction.ROTATE_LEFT])

            actions.append([RocketBaseAction.SHOT])

            rocket.angle = temp_rocket_angle

            return actions, number_of_rotation + 1

    def simple_shot(self):
        return [RocketBaseAction.SHOT]

    def can_shoot(self):
        return self.shoot_reload_ticks >= 5

    def convert_actions(self, actions):
        self.shoot_reload_ticks = self.shoot_reload_ticks + 1

        # Automatic agents cannot shoot all the time
        if(RocketBaseAction.SHOT in actions):
            if self.shoot_reload_ticks < 5:
                actions.remove(RocketBaseAction.SHOT)
            else:
                self.shoot_reload_ticks = 0

        if (RocketBaseAction.SPLIT_SHOOT in actions):
            if self.shoot_reload_ticks < 5:
                actions.remove(RocketBaseAction.SPLIT_SHOOT)
            else:
                self.shoot_reload_ticks = 0


        return actions

    def get_state_info(self, state):
        # Return action_plan_lengths (attack, deffense, evasion, stop), and their corresponding action_plans
        own_rocket, enemy_rocket, neutral_asteroids, own_asteroids, enemy_asteroids, own_bullets, enemy_bullets = self.assign_objects_to_agent(state)
        impact, impact_asteroid, impact_steps_count = self.first_impact_asteroid(own_rocket, neutral_asteroids,
                                                                                    own_bullets, enemy_asteroids)

        number_of_close_asteroids = self.number_of_asteroids_in_range(own_rocket, neutral_asteroids, enemy_asteroids)
        total_number_of_dangerous_asteroids = len(neutral_asteroids) + len(enemy_asteroids)

        attack_actions = []
        attack_steps_count = NOT_FOUND_STEPS_COUNT

        evade_actions = []
        evade_steps_count = NOT_FOUND_STEPS_COUNT

        defense_shoot_actions = []
        defense_steps_count = NOT_FOUND_STEPS_COUNT

        stop_actions = []
        stop_steps_count = NOT_FOUND_STEPS_COUNT

        _, stop_actions, stop_steps_count = self.stop_moving(own_rocket)

        if impact:
            evade_actions, evade_steps_count = self.evade_asteroid(own_rocket, impact_asteroid)
            defense_shoot_actions, defense_steps_count = self.defense_shoot_asteroid_actions(own_rocket,
                                                                                                impact_asteroid)

        hit, attack_actions, attack_steps_count = self.shoot_in_all_directions_to_hit_enemy(own_rocket,
                                                                                               enemy_rocket,
                                                                                               state.neutral_asteroids,
                                                                                               enemy_asteroids,
                                                                                               own_bullets,
                                                                                               enemy_bullets)
        return (attack_steps_count,
                defense_steps_count,
                evade_steps_count,
                stop_steps_count,
                impact_steps_count,
                number_of_close_asteroids,
                total_number_of_dangerous_asteroids,
                own_rocket.health,
                enemy_rocket.health),\
               (attack_actions, defense_shoot_actions, evade_actions, stop_actions)


class Attacking_agent(Agent):
    def __init__(self, player_number):
        super().__init__(player_number)
        # self.screen = screen
        self.shoot_reload_ticks = 0
        self.active_steps = 0
        self.inactive_steps = 0
        self.inactiv_ticks = 0
        self.plan = []
        self.finished_plan = True

    def choose_actions(self, state, opposite_agent_actions):

        own_rocket, enemy_rocket, neutral_asteroids, own_asteroids, enemy_asteroids, own_bullets, enemy_bullets = super().assign_objects_to_agent(state)

        if self.reevaluate_plan():
            self.active_steps = self.active_steps + 1
            hit, actions, count = super().shoot_in_all_directions_to_hit_enemy(own_rocket, enemy_rocket,
                                                                               state.neutral_asteroids, enemy_asteroids,
                                                                               own_bullets, enemy_bullets)
            if hit:
                super().store_plan(actions)
        else:
            self.inactive_steps = self.inactive_steps + 1

        actions = super().choose_action_from_plan()
        return super().convert_actions(actions)



    def reevaluate_plan(self):
        if self.inactiv_ticks > 0:
            self.inactiv_ticks = 0
            return True

        if not self.finished_plan_attack:
            return False

        self.inactiv_ticks = self.inactiv_ticks + 1
        return False

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
            actions.append(RocketBaseAction(int(action_number)))

        return actions

class Evasion_agent(Agent):
    def __init__(self, player_number, draw_modul = None):
        super().__init__(player_number)
        self.shoot_reload_ticks = 0
        self.inactive_steps = 0
        self.finished_plan_evasion = True
        self.draw_modul = draw_modul


    def choose_actions(self, state):
        own_rocket, enemy_rocket, neutral_asteroids, own_asteroids, enemy_asteroids, own_bullets, enemy_bullets = super().assign_objects_to_agent(state)
        #COOL
        #closest_asteroids = super().find_N_closest_asteroids(own_rocket, neutral_asteroids, enemy_asteroids, 3)
        #for close_ast in closest_asteroids:
        #    self.draw_modul.draw_line((own_rocket.centerx, own_rocket.centery),
        #                              (own_rocket.centerx + close_ast[0][0], own_rocket.centery + close_ast[0][1]))

        #enemy_vector = super().object_object_vector(enemy_rocket, own_rocket)
        #self.draw_modul.draw_line((own_rocket.centerx, own_rocket.centery),
        #                          (own_rocket.centerx + enemy_vector[0], own_rocket.centery + enemy_vector[1]))

        #self.draw_modul.save_image()
        #self.draw_modul.render()


        if self.reevaluate_plan():
            impact, impact_asteroid, impact_steps = super().first_impact_asteroid(own_rocket, state.neutral_asteroids, own_bullets, enemy_asteroids)
            #with stopping agent it looks less chaotic, but shows similar results
            stop_found, stop_actions, stop_actions_count = super().stop_moving(own_rocket)
            if impact_asteroid is None:
                if stop_found:
                    super().store_plan(stop_actions)
                else:
                    super().finish_plan()
                    return super().convert_actions([])

            if impact_asteroid is not None and impact_steps < 25:
                actions, steps_count = super().evade_asteroid(own_rocket, impact_asteroid)
                super().store_plan(actions)
        else:
            self.inactive_steps = self.inactive_steps + 1

        actions = super().choose_action_from_plan()

        return super().convert_actions(actions)

    def reevaluate_plan(self):
        if self.inactiv_ticks > INACTIV_STEPS_LIMIT:
            self.inactiv_ticks = 0
            return True

        if not self.finished_plan_evasion:
            self.inactiv_ticks = self.inactiv_ticks + 1
            return False

        self.inactiv_ticks = self.inactiv_ticks + 1
        return False

class Stable_defensive_agent(Agent):
    def __init__(self, player_number):
        super().__init__(player_number)
        # self.screen = screen
        self.shoot_reload_ticks = 0
        self.python_time = 0
        self.numpy_time = 0
        self.asteroids_arr = []
        self.bullets_arr = []
        self.target_asteroid = None
        self.inactive_steps = 0
        self.active_steps = 0

    def choose_actions(self, state):

        own_rocket, enemy_rocket, neutral_asteroids, own_asteroids, enemy_asteroids, own_bullets, enemy_bullets = super().assign_objects_to_agent(state)

        if super().reevaluate_plan():
            self.active_steps = self.active_steps + 1
            self.active_ticks = 1

            impact_neutral_asteroid, impact_neutral_asteroid_steps = super().first_impact_neutral_asteroid(own_rocket, state.neutral_asteroids, own_bullets)
            self.asteroids_arr.append(len(state.neutral_asteroids))
            self.bullets_arr.append(len(own_bullets))

            impact_enemy_asteroid, impact_enemy_asteroid_steps = super().first_impact_enemy_asteroid(own_rocket, enemy_asteroids, own_bullets)


            if impact_neutral_asteroid_steps < impact_enemy_asteroid_steps:
                impact_asteroid = impact_neutral_asteroid
            elif impact_neutral_asteroid_steps > impact_enemy_asteroid_steps:
                impact_asteroid = impact_enemy_asteroid
            elif impact_neutral_asteroid is None and impact_enemy_asteroid is None:
                self.finish_plan()
                return super().convert_actions([])
            else:
                impact_asteroid = impact_enemy_asteroid




            if super().shoot_will_hit_explicit_asteroid(own_rocket, impact_asteroid):
                actions = super().simple_shot()
                super().finish_plan()
                return super().convert_actions(actions)

            self.target_asteroid = impact_asteroid

            super().recalculate_target_position(own_rocket, impact_asteroid)

            actions, actions_steps = super().face_asteroid(own_rocket, impact_asteroid)
            if not actions:
                actions = [super().simple_shot()]
            super().store_plan(actions)
        else:
            self.inactive_steps = self.inactive_steps + 1
            if self.target_asteroid is not None:
                self.target_asteroid.move()

                if super().shoot_will_hit_explicit_asteroid(own_rocket, self.target_asteroid):
                    actions = super().simple_shot()
                    super().finish_plan()
                    return super().convert_actions(actions)

        actions = super().choose_action_from_plan()

        return super().convert_actions(actions)


class Genetic_agent(Agent):
    def __init__(self, player_number, decision_function):
        super().__init__(player_number)
        # self.screen = screen
        self.inactiv_ticks = 0
        self.attack_count = 0
        self.defense_count = 0
        self.evasion_count = 0
        self.active_choose_steps = 0
        self.inactive_choose_steps = 0
        self.stop_count = 0
        self.odd = 0
        self.decision_function = decision_function
        self.penalty = 0
        self.finished_plan_gp = False
        self.history=[0,0,0,0]

    def choose_actions(self, state):
        actions = []
        #if self.reevaluate_plan():

        if super().reevaluate_plan():
            self.active_choose_steps += 1
            (attack_actions, attack_steps_count), (defense_shoot_actions, defense_steps_count), (evade_actions, evade_steps_count), (stop_actions, stop_steps_count), impact_steps_count = self.get_state_stats(state)

            ###
            action_plans = (attack_actions, defense_shoot_actions, evade_actions, stop_actions)
            if action_plans != ([],[],[],[]):
                actions_index = self.decision_function(attack_steps_count, defense_steps_count, evade_steps_count,
                                                       stop_steps_count, impact_steps_count)
                if actions_index() == ActionPlanEnum.ATTACK:
                    actions = attack_actions
                    self.history[int(ActionPlanEnum.ATTACK.value)] += 1
                    self.attack_count += 1
                elif actions_index() == ActionPlanEnum.DEFFENSE:
                    actions = defense_shoot_actions
                    self.history[int(ActionPlanEnum.DEFFENSE.value)] += 1
                    self.defense_count += 1
                elif actions_index() == ActionPlanEnum.EVASION:
                    actions = evade_actions
                    self.history[int(ActionPlanEnum.EVASION.value)] += 1
                    self.evasion_count += 1
                elif actions_index() == ActionPlanEnum.STOP:
                    actions = stop_actions
                    self.history[int(ActionPlanEnum.STOP.value)] += 1
                    self.stop_count += 1

            ###

            super().store_plan(actions)
        else:
            self.inactive_choose_steps += 1



        return super().convert_actions(super().choose_action_from_plan())

    def get_state_stats(self, state):
        own_rocket, enemy_rocket, neutral_asteroids, own_asteroids, enemy_asteroids, own_bullets, enemy_bullets = super().assign_objects_to_agent(state)
        impact, impact_asteroid, impact_steps_count = super().first_impact_asteroid(own_rocket, neutral_asteroids,
                                                                                    own_bullets, enemy_asteroids)

        attack_actions = []
        attack_steps_count = NOT_FOUND_STEPS_COUNT

        evade_actions = []
        evade_steps_count = NOT_FOUND_STEPS_COUNT

        defense_shoot_actions = []
        defense_steps_count = NOT_FOUND_STEPS_COUNT

        stop_actions = []
        stop_steps_count = NOT_FOUND_STEPS_COUNT

        _, stop_actions, stop_steps_count = super().stop_moving(own_rocket)

        if impact:
            evade_actions, evade_steps_count = super().evade_asteroid(own_rocket, impact_asteroid)
            defense_shoot_actions, defense_steps_count = super().defense_shoot_asteroid_actions(own_rocket,
                                                                                                impact_asteroid)
        #if self.odd < 1:
        #    self.odd = self.odd + 1
        #else:
        #    self.odd = 0
        hit, attack_actions, attack_steps_count = super().shoot_in_all_directions_to_hit_enemy(own_rocket,
                                                                                                   enemy_rocket,
                                                                                                   state.neutral_asteroids,
                                                                                                   enemy_asteroids,
                                                                                                   own_bullets,
                                                                                                   enemy_bullets)
        return (attack_actions, attack_steps_count), (defense_shoot_actions, defense_steps_count), (evade_actions, evade_steps_count), (stop_actions, stop_steps_count), impact_steps_count


class DQAgent(Agent):
    def __init__(self, player_number, num_inputs, num_outputs, batch_size = 32, num_batches = 64, model = None, extended = False):
        super().__init__(player_number)
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.batch_size = batch_size
        self.num_batches = num_batches
        self.eps = 1.0
        self.eps_decay = 0.9989
        self.gamma = 0.95
        self.exp_buffer = []
        self.active_choose_steps = 0
        self.inactive_choose_steps = 0
        self.inactiv_ticks = 0
        self.attack_count = 0
        self.defense_count = 0
        self.evasion_count = 0
        self.stop_count = 0
        self.penalty = 0
        self.odd = 0
        self.history=[0,0,0,0]
        self.extended = extended
        if model is None:
            self.build_model()
        else:
            self.model = model

    # vytvari model Q-site
    def build_model(self):
        self.model = tf.keras.models.Sequential([tf.keras.layers.Dense(24, activation=tf.nn.relu, input_dim=self.num_inputs, name='dense_1'),
                                                 tf.keras.layers.Dense(24, activation=tf.nn.relu, name = 'dense_02'),
                                                 tf.keras.layers.Dense(self.num_outputs, activation='linear', name='dense_03')])
        opt = tf.keras.optimizers.Adam(lr=0.001)
        self.model.compile(optimizer=opt, loss='mse')

    def reevaluate_plan(self, train):
        if train:
            return True

        return super().reevaluate_plan()


    # copied from GP and to ancestor
    def get_state_stats(self, state):
        own_rocket, enemy_rocket, neutral_asteroids, own_asteroids, enemy_asteroids, own_bullets, enemy_bullets = super().assign_objects_to_agent(state)
        impact, impact_asteroid, impact_steps_count = super().first_impact_asteroid(own_rocket, neutral_asteroids,
                                                                                    own_bullets, enemy_asteroids)

        number_of_close_asteroids = self.number_of_asteroids_in_range(own_rocket, neutral_asteroids, enemy_asteroids)
        total_number_of_dangerous_asteroids = len(neutral_asteroids) + len(enemy_asteroids)


        attack_actions = []
        attack_steps_count = NOT_FOUND_STEPS_COUNT

        evade_actions = []
        evade_steps_count = NOT_FOUND_STEPS_COUNT

        defense_shoot_actions = []
        defense_steps_count = NOT_FOUND_STEPS_COUNT

        stop_actions = []
        stop_steps_count = NOT_FOUND_STEPS_COUNT

        _, stop_actions, stop_steps_count = super().stop_moving(own_rocket)

        if impact:
            evade_actions, evade_steps_count = super().evade_asteroid(own_rocket, impact_asteroid)
            defense_shoot_actions, defense_steps_count = super().defense_shoot_asteroid_actions(own_rocket,
                                                                                                impact_asteroid)

        if self.odd < 1 and not self.extended:
            self.odd = self.odd + 1
        else:
            self.odd = 0
            hit, attack_actions, attack_steps_count = super().shoot_in_all_directions_to_hit_enemy(own_rocket,
                                                                                                   enemy_rocket,
                                                                                                   state.neutral_asteroids,
                                                                                                   enemy_asteroids,
                                                                                                   own_bullets,
                                                                                                   enemy_bullets)
        return  (attack_actions, attack_steps_count), \
                (defense_shoot_actions, defense_steps_count), \
                (evade_actions, evade_steps_count), \
                (stop_actions, stop_steps_count), \
                impact_steps_count, \
                number_of_close_asteroids, \
                total_number_of_dangerous_asteroids, \
                own_rocket.health, \
                enemy_rocket.health

    def choose_random_action_plan(self):
        val = np.random.randint(self.num_outputs)
        self.history[val] += 1
        return val

    def choose_action_plan_index(self, state):
        if np.random.uniform() < self.eps:
            return self.choose_random_action_plan()
        else:
            val = np.argmax(self.model.predict(state)[0])
            self.history[val] += 1
            return val

    def get_action_from_action_plan(self, plan_index, action_plans):
        action_plan = action_plans[plan_index]

        super().store_plan(action_plan)

        return super().convert_actions(super().choose_action_from_plan())


    def choose_actions(self, state, train=False):
        if train:
            (attack_actions, attack_steps_count), (defense_shoot_actions, defense_steps_count), (
                evade_actions, evade_steps_count), (stop_actions, stop_steps_count), impact_steps_count = self.get_state_stats(state)
            transformed_state = (attack_steps_count, defense_steps_count, evade_steps_count, stop_steps_count, impact_steps_count)

            if np.random.uniform() < self.eps:
                actions_index = np.random.randint(self.num_outputs)
            else:
                actions_index = np.argmax(self.model.predict(transformed_state)[0])



        else:
            if self.reevaluate_plan(train=False):
                self.active_choose_steps += 1

                (attack_actions, attack_steps_count), \
                (defense_shoot_actions, defense_steps_count), \
                (evade_actions, evade_steps_count), \
                (stop_actions, stop_steps_count), \
                impact_steps_count, \
                number_of_close_asteroids, \
                total_number_of_dangerous_asteroids, \
                own_rocket_health, \
                enemy_rocket_health = self.get_state_stats(state)



                action_plans = [attack_actions, defense_shoot_actions, evade_actions, stop_actions]

                if self.extended:
                    transformed_state = (attack_steps_count, defense_steps_count, evade_steps_count, stop_steps_count, impact_steps_count, number_of_close_asteroids, total_number_of_dangerous_asteroids, own_rocket_health, enemy_rocket_health)
                else:
                    transformed_state = (attack_steps_count, defense_steps_count, evade_steps_count, stop_steps_count, impact_steps_count)

                transformed_state = np.array([transformed_state])

                if action_plans != [[],[],[],[]]:
                    not_empty = 0
                    valid_index = 0
                    for index in range(4):
                        if action_plans[index] != []:
                            not_empty += 1
                            valid_index = index

                    if not_empty == 1:
                        actions = action_plans[valid_index]
                        self.history[valid_index] +=1
                    else:
                        actions_index = np.argmax(self.model.predict(transformed_state)[0])
                        actions = action_plans[actions_index]
                        self.history[actions_index] += 1

                    super().store_plan(actions)
            else:
                self.inactive_choose_steps += 1

        return super().convert_actions(super().choose_action_from_plan())

    # vraci akci agenta - pokud trenujeme tak epsilon-greedy, jinak nejlepsi podle site
    def action(self, state, train=False):
        if train and np.random.uniform() < self.eps:
            return np.random.randint(self.num_outputs)
        else:
            return np.argmax(self.model.predict(state)[0])

    # ulozeni informaci do experience bufferus
    def record_experience(self, exp):
        self.exp_buffer.append(exp)
        if len(self.exp_buffer) > 10000:
            self.exp_buffer = self.exp_buffer[-10000:]

    # trenovani z bufferu
    def train(self, input_buffer = None):
        if input_buffer is not None:
            self.exp_buffer = input_buffer
        if (len(self.exp_buffer) <= self.batch_size):
            return

        for _ in range(self.num_batches):
            batch = random.sample(self.exp_buffer, self.batch_size)
            states = np.array([s for (s, _, _, _, _) in batch])
            next_states = np.array([ns for (_, _, _, ns, _) in batch])
            states = states.reshape((-1, self.num_inputs))
            next_states = next_states.reshape((-1, self.num_inputs))
            pred = self.model.predict(states)
            next_pred = self.model.predict(next_states)
            # spocitame cilove hodnoty
            for i, (s, a, r, ns, go) in enumerate(batch):
                pred[i][a] = r
                if not go:
                    pred[i][a] = r + self.gamma*np.amax(next_pred[i])

            self.model.fit(states, pred, epochs=1, verbose=0)
        # snizime epsilon pro epsilon-greedy strategii
        if self.eps > 0.01:
            self.eps = self.eps*self.eps_decay

class Low_level_sensor_DQAgent(Agent):
    def __init__(self, player_number, num_inputs, num_outputs, batch_size = 32, num_batches = 64, model = None, draw_module = None):
        super().__init__(player_number)
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.batch_size = batch_size
        self.num_batches = num_batches
        self.buffer_size = 3000
        self.eps = 1.0
        self.eps_decay = 0.9998
        self.gamma = 0.95
        self.exp_buffer = []
        self.inactiv_ticks = 0
        self.attack_count = 0
        self.defense_count = 0
        self.evasion_count = 0
        self.stop_count = 0
        self.penalty = 0
        self.odd = 0
        self.history = [0, 0, 0, 0, 0, 0]
        self.draw_module = draw_module
        if model is None:
            self.build_model()
        else:
            self.model = model


    # vytvari model Q-site
    def build_model(self):
        self.model = tf.keras.models.Sequential([tf.keras.layers.Dense(24, activation=tf.nn.relu, input_dim=self.num_inputs
                                                                       #, name='dense_1'
                                                                       ),
                                                 tf.keras.layers.Dense(24, activation=tf.nn.relu
                                                                       #, name = 'dense_02'
                                                                       ),
                                                 tf.keras.layers.Dense(24, activation=tf.nn.relu),
                                                 tf.keras.layers.Dense(self.num_outputs, activation='linear')])
        opt = tf.keras.optimizers.Adam(lr=0.001)
        self.model.compile(optimizer=opt, loss='mse')

    def train(self):
        if (len(self.exp_buffer) <= self.batch_size):
            return

        for _ in range(self.num_batches):
            batch = random.sample(self.exp_buffer, self.batch_size)
            states = np.array([s for (s, _, _, _, _) in batch])
            next_states = np.array([ns for (_, _, _, ns, _) in batch])
            states = states.reshape((-1, self.num_inputs))
            next_states = next_states.reshape((-1, self.num_inputs))
            pred = self.model.predict(states)
            next_pred = self.model.predict(next_states)
            # spocitame cilove hodnoty
            for i, (s, a, r, ns, go) in enumerate(batch):
                pred[i][a] = r
                if not go:
                    pred[i][a] = r + self.gamma*np.amax(next_pred[i])

            self.model.fit(states, pred, epochs=1, verbose=0)
            #gc.collect()
        # snizime epsilon pro epsilon-greedy strategii
        if self.eps > 0.01:
            self.eps = self.eps*self.eps_decay

    def record_experience(self, exp):
        self.exp_buffer.append(exp)
        if len(self.exp_buffer) > self.buffer_size:
            self.exp_buffer = self.exp_buffer[-self.buffer_size:]

    def get_simple_actions_from_action_value(self, value):
        if value == 0:
            actions = [RocketBaseAction.ROTATE_LEFT]
        if value == 1:
            actions = [RocketBaseAction.ROTATE_RIGHT]
        if value == 2:
            actions = [RocketBaseAction.ACCELERATE]
        if value == 3:
            actions = [RocketBaseAction.SHOT]
        if value == 4:
            actions = [RocketBaseAction.SPLIT_SHOOT]
        if value == 5:
            actions = []
        return actions


    def choose_action_index(self, state, train=False):
        if train and np.random.uniform() < self.eps:
            val = np.random.randint(self.num_outputs)
            actions = self.get_simple_actions_from_action_value(val)

            if not self.can_shoot():
                while actions == [RocketBaseAction.SHOT] or actions == [RocketBaseAction.SPLIT_SHOOT]:
                    val = np.random.randint(self.num_outputs)
                    actions = self.get_simple_actions_from_action_value(val)

            self.history[val] += 1
        else:
            predictions = self.model.predict(state)[0]
            best_args = predictions.argsort()[-3:][::-1]
            val = best_args[0]
            ticks = self.shoot_reload_ticks
            if not self.can_shoot():
                for i in range(3):
                    val = best_args[i]
                    actions = self.get_simple_actions_from_action_value(val)
                    if actions != [RocketBaseAction.SHOT] and actions != [RocketBaseAction.SPLIT_SHOOT]:
                        break



            #val = np.argmax(self.model.predict(state)[0])
            self.history[val] +=1

        return val

    def choose_actions(self, state):
        state = self.low_level_state_info(state)
        action_index = self.choose_action_index(state, train=False)
        actions = self.get_simple_actions_from_action_value(action_index)
        actions = super().convert_actions(actions)
        return actions




# vytvorime agenta (4 vstupy, 2 akce)


class Input_agent(Agent):
     def __init__(self,  screen, player_number):
         super().__init__(player_number)
         self.input=True
         self.screen = screen

     def  choose_actions(self, state):
         actions_one = []
         actions_two = []
         actions = []
         events = pygame.event.get(pygame.KEYDOWN)

         for event in events:
             if(event.key == pygame.K_f):
                 #actions.append(Rocket_action.ROCKET_ONE_SHOOT)
                 # actions_one.append(Rocket_action.ROCKET_ONE_SHOOT)
                 actions_two.append(RocketBaseAction.SHOT)
             if(event.key == pygame.K_g):
                 #actions.append(Rocket_action.ROCKET_ONE_SPLIT_SHOOT)
                 # actions_one.append(Rocket_action.ROCKET_ONE_SPLIT_SHOOT)
                 actions_two.append(RocketBaseAction.SPLIT_SHOOT)
             if(event.key == pygame.K_o):
                 #for second player switch back to action_two
                 actions_one.append(RocketBaseAction.SHOT)
             if(event.key == pygame.K_p):
                 # for second player switch back to action_two
                 actions_one.append(RocketBaseAction.SPLIT_SHOOT)


         all_keys = pygame.key.get_pressed()
         if all_keys[pygame.K_UP]:
             #actions.append(Rocket_action.ROCKET_ONE_ACCELERATE)
             # actions_one.append(Rocket_action.ROCKET_ONE_ACCELERATE)
             actions_one.append(RocketBaseAction.ACCELERATE)
         if all_keys[pygame.K_LEFT]:
             #actions.append(Rocket_action.ROCKET_ONE_ROTATE_LEFT)
             # actions_one.append(Rocket_action.ROCKET_ONE_ROTATE_LEFT)
             actions_one.append(RocketBaseAction.ROTATE_LEFT)
         if all_keys[pygame.K_RIGHT]:
             #actions.append(Rocket_action.ROCKET_ONE_ROTATE_RIGHT)
             # actions_one.append(Rocket_action.ROCKET_ONE_ROTATE_RIGHT)
             actions_one.append(RocketBaseAction.ROTATE_RIGHT)

         if all_keys[pygame.K_a]:
             #actions.append(Rocket_action.ROCKET_TWO_ROTATE_LEFT)
             # actions_two.append(Rocket_action.ROCKET_TWO_ROTATE_LEFT)
             actions_two.append(RocketBaseAction.ROTATE_LEFT)
         if all_keys[pygame.K_d]:
             #actions.append(Rocket_action.ROCKET_TWO_ROTATE_RIGHT)
             # actions_two.append(Rocket_action.ROCKET_TWO_ROTATE_RIGHT)
             actions_two.append(RocketBaseAction.ROTATE_RIGHT)
         if all_keys[pygame.K_w]:
             #actions.append(Rocket_action.ROCKET_TWO_ACCELERATE)
             # actions_two.append(Rocket_action.ROCKET_TWO_ACCELERATE)
             actions_two.append(RocketBaseAction.ACCELERATE)



         # clearing it apparently prevents from stucking
         pygame.event.clear()

         return actions_one\
             , actions_two

class ActionPlanEnum(Enum):
    ATTACK = 0
    DEFFENSE = 1
    EVASION = 2
    STOP = 3

