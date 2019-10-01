
import pygame
import random
import sys, time
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
        self.asteroids_one = []
        self.asteroids_two = []
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

        self._generate_asteroid_()

        self._check_collisions_()

        self._update_sprites_()

        self._draw_sprites_()


    def _generate_asteroid_(self):
        if random.randint(0,100) == 1:
            self.asteroids_neutral.append(Asteroid(self.screen, self.RocketOne, self.RocketTwo, None, None, None))

    def _check_collisions_(self):
        # Bullets ONE with NEUTRAL asteroids
        for bullet_one in self.bullets_one:
            for asteroid in self.asteroids_neutral:
                if bullet_one.rect.colliderect(asteroid.collision_rect):
                    self.asteroids_neutral.remove(asteroid)
                    new_asteroid = Asteroid(self.screen, None, None, asteroid, bullet_one.rocket,
                                            bullet_one)

                    if bullet_one in self.bullets_one:
                        self.bullets_one.remove(bullet_one)

                    if new_asteroid.valid:
                        self.asteroids_one.append(new_asteroid)
                    continue

        # Bullets ONE with TWO's asteroids
        for bullet_one in self.bullets_one:
            for asteroid_two in self.asteroids_two:
                if bullet_one.rect.colliderect(asteroid_two.collision_rect):
                    self.asteroids_two.remove(asteroid_two)

                    new_asteroid = Asteroid(self.screen, None, None, asteroid_two, bullet_one.rocket,
                                            bullet_one)
                    print(f"new asteroid is valid: {new_asteroid.valid == True}")

                    if bullet_one in self.bullets_one:
                        self.bullets_one.remove(bullet_one)

                    if new_asteroid.valid:
                        self.asteroids_one.append(new_asteroid)

        # Bullets TWO with ONE' asteroids
        for bullet_two in self.bullets_two:
            for asteroid_one in self.asteroids_one:
                if bullet_two.rect.colliderect(asteroid_one.collision_rect):
                    self.asteroids_one.remove(asteroid_one)

                    new_asteroid = Asteroid(self.screen, None, None, asteroid_one, bullet_two.rocket,
                                            bullet_two)
                    print(f"new asteroid is valid: {new_asteroid.valid == True}")
                    if bullet_two in self.bullets_two:
                        self.bullets_two.remove(bullet_two)

                    if new_asteroid.valid:
                        self.asteroids_two.append(new_asteroid)

        # Bullets TWO with NEUTRAL asteroids
        for bullet_two in self.bullets_two:
            for asteroid in self.asteroids_neutral:
                if bullet_two.rect.colliderect(asteroid.collision_rect):
                    self.asteroids_neutral.remove(asteroid)
                    new_asteroid = Asteroid(self.screen, self.RocketOne, self.RocketTwo, asteroid, bullet_two.rocket,
                                            bullet_two)

                    if bullet_two in self.bullets_two:
                        self.bullets_two.remove(bullet_two)

                    if new_asteroid.valid:
                        self.asteroids_two.append(new_asteroid)
                    continue



        for asteroid in self.asteroids_neutral:
            # Rocket ONE with NEUTRAL asteroid
            if asteroid.collision_rect.colliderect(self.RocketOne.collision_rect):
                asteroid.draw()
                self.RocketOne.draw()
                pygame.display.update()
                time.sleep(2)
                quit()
            # Rocket TWO with NEUTRAL asteroid
            if asteroid.collision_rect.colliderect(self.RocketTwo.collision_rect):
                asteroid.draw()
                self.RocketTwo.draw()
                pygame.display.update()
                time.sleep(2)
                quit()

        for asteroid_one in self.asteroids_one:
            if asteroid_one.collision_rect.colliderect(self.RocketTwo.collision_rect):
                asteroid_one.draw()
                self.RocketTwo.draw()
                pygame.display.update()
                time.sleep(2)
                quit()

        for asteroid_two in self.asteroids_two:
            if asteroid_two.collision_rect.colliderect(self.RocketOne.collision_rect):
                asteroid_two.draw()
                self.RocketOne.draw()
                pygame.display.update()
                time.sleep(2)
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

        for asteroid_one in self.asteroids_one:
            asteroid_one.update()

        for asteroid_two in self.asteroids_two:
            asteroid_two.update()



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