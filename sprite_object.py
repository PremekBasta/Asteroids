import pygame, random
import math
from enum import Enum
from constants import *



class Rocket():
    max_speed = MAX_ROCKET_SPEED
    rocket_angle_rotation = ROCKET_ANGLE_ROTATION
    rocket_rotation_images = [
        [pygame.image.load('images/rocket_one_0.png'), pygame.image.load('images/rocket_one_12.png'),
         pygame.image.load('images/rocket_one_24.png'), pygame.image.load('images/rocket_one_36.png'),
         pygame.image.load('images/rocket_one_48.png'), pygame.image.load('images/rocket_one_60.png'),
         pygame.image.load('images/rocket_one_72.png'), pygame.image.load('images/rocket_one_84.png'),
         pygame.image.load('images/rocket_one_96.png'), pygame.image.load('images/rocket_one_108.png'),
         pygame.image.load('images/rocket_one_120.png'), pygame.image.load('images/rocket_one_132.png'),
         pygame.image.load('images/rocket_one_144.png'), pygame.image.load('images/rocket_one_156.png'),
         pygame.image.load('images/rocket_one_168.png'), pygame.image.load('images/rocket_one_180.png'),
         pygame.image.load('images/rocket_one_192.png'), pygame.image.load('images/rocket_one_204.png'),
         pygame.image.load('images/rocket_one_216.png'), pygame.image.load('images/rocket_one_228.png'),
         pygame.image.load('images/rocket_one_240.png'), pygame.image.load('images/rocket_one_252.png'),
         pygame.image.load('images/rocket_one_264.png'), pygame.image.load('images/rocket_one_276.png'),
         pygame.image.load('images/rocket_one_288.png'), pygame.image.load('images/rocket_one_300.png'),
         pygame.image.load('images/rocket_one_312.png'), pygame.image.load('images/rocket_one_324.png'),
         pygame.image.load('images/rocket_one_336.png'), pygame.image.load('images/rocket_one_348.png')],
        [pygame.image.load('images/rocket_two_0.png'), pygame.image.load('images/rocket_two_12.png'),
         pygame.image.load('images/rocket_two_24.png'), pygame.image.load('images/rocket_two_36.png'),
         pygame.image.load('images/rocket_two_48.png'), pygame.image.load('images/rocket_two_60.png'),
         pygame.image.load('images/rocket_two_72.png'), pygame.image.load('images/rocket_two_84.png'),
         pygame.image.load('images/rocket_two_96.png'), pygame.image.load('images/rocket_two_108.png'),
         pygame.image.load('images/rocket_two_120.png'), pygame.image.load('images/rocket_two_132.png'),
         pygame.image.load('images/rocket_two_144.png'), pygame.image.load('images/rocket_two_156.png'),
         pygame.image.load('images/rocket_two_168.png'), pygame.image.load('images/rocket_two_180.png'),
         pygame.image.load('images/rocket_two_192.png'), pygame.image.load('images/rocket_two_204.png'),
         pygame.image.load('images/rocket_two_216.png'), pygame.image.load('images/rocket_two_228.png'),
         pygame.image.load('images/rocket_two_240.png'), pygame.image.load('images/rocket_two_252.png'),
         pygame.image.load('images/rocket_two_264.png'), pygame.image.load('images/rocket_two_276.png'),
         pygame.image.load('images/rocket_two_288.png'), pygame.image.load('images/rocket_two_300.png'),
         pygame.image.load('images/rocket_two_312.png'), pygame.image.load('images/rocket_two_324.png'),
         pygame.image.load('images/rocket_two_336.png'), pygame.image.load('images/rocket_two_348.png')]]

    def __init__(self, screen, player):
        super().__init__()
        self.angle = 0
        self.speedx = 0
        self.speedy = 0
        self.screen = screen
        self.player = player
        for i in range(2):
            for image in Rocket.rocket_rotation_images[i]:
                image.set_colorkey((0,0,0))

        self.health = 100

        self.image = Rocket.rocket_rotation_images[player][0]
        self.image_rect = self.image.get_rect()
        self.image_width = self.image_rect.width
        self.image_height = self.image_rect.height
        self.radius = int(self.image_rect.width * ROCKET_RADIUS_RATIO)
        self.centerx = int(SCREEN_WIDTH / 2)
        self.centery = int(SCREEN_HEIGHT / 2)

        if player == 1:
            self.centerx = self.centerx - 150
            self.health_bar_color = PLAYER_ONE_COLOR
        else:
            self.centerx = self.centerx + 150
            self.health_bar_color = PLAYER_TWO_COLOR


    def rotate_left(self):
        self.angle = self.angle + ROCKET_ANGLE_ROTATION + 360
        self.angle = self.angle % 360

    def rotate_right(self):
        self.angle = self.angle - ROCKET_ANGLE_ROTATION
        self.angle = self.angle % 360

    def accelerate(self):
        self.speedx = self.speedx - int(math.sin(self.angle / 180 * math.pi) * 20 / 2)
        self.speedy = self.speedy - int(math.cos(self.angle / 180 * math.pi) * 20 / 2)
        if math.sqrt(math.pow(self.speedx, 2) + math.pow(self.speedy, 2)) > Rocket.max_speed:
            minusx = False
            minusy = False
            if self.speedx < 0:
                minusx = True
            if self.speedy < 0:
                minusy = True

            if self.speedy == 0:
                self.speedx = int(self.speedx * math.sqrt(math.pow(Rocket.max_speed, 2) / math.pow(self.speedx, 2)))
            else:
                ratio = self.speedx / self.speedy
                self.speedy = int(math.sqrt(math.pow(Rocket.max_speed, 2) / (math.pow(ratio, 2) + 1)))
                self.speedx = int(math.sqrt(math.pow(Rocket.max_speed, 2) - math.pow(self.speedy, 2)))

            if minusx:
                self.speedx = -self.speedx
            if minusy:
                self.speedy = -self.speedy

    def draw(self):
        pygame.draw.rect(self.screen, self.health_bar_color, pygame.Rect(0.85*SCREEN_WIDTH - self.player * 0.82*SCREEN_WIDTH, 0.95*SCREEN_HEIGHT, self.health, 10))
        # pygame.draw.circle(self.screen, (255, 255, 255), (self.centerx, self.centery), self.radius)
        self.screen.blit(Rocket.rocket_rotation_images[self.player][self.angle // 12], (self.centerx - self.image_width / 2, self.centery - self.image_height / 2))

    def move(self, *args):
        self.centerx = int((self.centerx + self.speedx / 8) % SCREEN_WIDTH)
        self.centery = int((self.centery + self.speedy / 8) % SCREEN_HEIGHT)


class Bullet():
    bullet_angle_images = [[[pygame.image.load('images/bullet_one_0.png'), pygame.image.load('images/bullet_one_12.png'),
                            pygame.image.load('images/bullet_one_24.png'), pygame.image.load('images/bullet_one_36.png'),
                            pygame.image.load('images/bullet_one_48.png'), pygame.image.load('images/bullet_one_60.png'),
                            pygame.image.load('images/bullet_one_72.png'), pygame.image.load('images/bullet_one_84.png'),
                            pygame.image.load('images/bullet_one_96.png'), pygame.image.load('images/bullet_one_108.png'),
                            pygame.image.load('images/bullet_one_120.png'), pygame.image.load('images/bullet_one_132.png'),
                            pygame.image.load('images/bullet_one_144.png'), pygame.image.load('images/bullet_one_156.png'),
                            pygame.image.load('images/bullet_one_168.png'), pygame.image.load('images/bullet_one_180.png'),
                            pygame.image.load('images/bullet_one_192.png'), pygame.image.load('images/bullet_one_204.png'),
                            pygame.image.load('images/bullet_one_216.png'), pygame.image.load('images/bullet_one_228.png'),
                            pygame.image.load('images/bullet_one_240.png'), pygame.image.load('images/bullet_one_252.png'),
                            pygame.image.load('images/bullet_one_264.png'), pygame.image.load('images/bullet_one_276.png'),
                            pygame.image.load('images/bullet_one_288.png'), pygame.image.load('images/bullet_one_300.png'),
                            pygame.image.load('images/bullet_one_312.png'), pygame.image.load('images/bullet_one_324.png'),
                            pygame.image.load('images/bullet_one_336.png'), pygame.image.load('images/bullet_one_348.png')],
                           [pygame.image.load('images/bullet_two_0.png'), pygame.image.load('images/bullet_two_12.png'),
                            pygame.image.load('images/bullet_two_24.png'), pygame.image.load('images/bullet_two_36.png'),
                            pygame.image.load('images/bullet_two_48.png'), pygame.image.load('images/bullet_two_60.png'),
                            pygame.image.load('images/bullet_two_72.png'), pygame.image.load('images/bullet_two_84.png'),
                            pygame.image.load('images/bullet_two_96.png'), pygame.image.load('images/bullet_two_108.png'),
                            pygame.image.load('images/bullet_two_120.png'), pygame.image.load('images/bullet_two_132.png'),
                            pygame.image.load('images/bullet_two_144.png'), pygame.image.load('images/bullet_two_156.png'),
                            pygame.image.load('images/bullet_two_168.png'), pygame.image.load('images/bullet_two_180.png'),
                            pygame.image.load('images/bullet_two_192.png'), pygame.image.load('images/bullet_two_204.png'),
                            pygame.image.load('images/bullet_two_216.png'), pygame.image.load('images/bullet_two_228.png'),
                            pygame.image.load('images/bullet_two_240.png'), pygame.image.load('images/bullet_two_252.png'),
                            pygame.image.load('images/bullet_two_264.png'), pygame.image.load('images/bullet_two_276.png'),
                            pygame.image.load('images/bullet_two_288.png'), pygame.image.load('images/bullet_two_300.png'),
                            pygame.image.load('images/bullet_two_312.png'), pygame.image.load('images/bullet_two_324.png'),
                            pygame.image.load('images/bullet_two_336.png'), pygame.image.load('images/bullet_two_348.png')]],

                           [[pygame.image.load('images/bullet_one_split_0.bmp'), pygame.image.load('images/bullet_one_split_12.bmp'),
                            pygame.image.load('images/bullet_one_split_24.bmp'), pygame.image.load('images/bullet_one_split_36.bmp'),
                            pygame.image.load('images/bullet_one_split_48.bmp'), pygame.image.load('images/bullet_one_split_60.bmp'),
                            pygame.image.load('images/bullet_one_split_72.bmp'), pygame.image.load('images/bullet_one_split_84.bmp'),
                            pygame.image.load('images/bullet_one_split_96.bmp'), pygame.image.load('images/bullet_one_split_108.bmp'),
                            pygame.image.load('images/bullet_one_split_120.bmp'), pygame.image.load('images/bullet_one_split_132.bmp'),
                            pygame.image.load('images/bullet_one_split_144.bmp'), pygame.image.load('images/bullet_one_split_156.bmp'),
                            pygame.image.load('images/bullet_one_split_168.bmp'), pygame.image.load('images/bullet_one_split_180.bmp'),
                            pygame.image.load('images/bullet_one_split_192.bmp'), pygame.image.load('images/bullet_one_split_204.bmp'),
                            pygame.image.load('images/bullet_one_split_216.bmp'), pygame.image.load('images/bullet_one_split_228.bmp'),
                            pygame.image.load('images/bullet_one_split_240.bmp'), pygame.image.load('images/bullet_one_split_252.bmp'),
                            pygame.image.load('images/bullet_one_split_264.bmp'), pygame.image.load('images/bullet_one_split_276.bmp'),
                            pygame.image.load('images/bullet_one_split_288.bmp'), pygame.image.load('images/bullet_one_split_300.bmp'),
                            pygame.image.load('images/bullet_one_split_312.bmp'), pygame.image.load('images/bullet_one_split_324.bmp'),
                            pygame.image.load('images/bullet_one_split_336.bmp'), pygame.image.load('images/bullet_one_split_348.bmp')],
                           [pygame.image.load('images/bullet_two_split_0.bmp'), pygame.image.load('images/bullet_two_split_12.bmp'),
                            pygame.image.load('images/bullet_two_split_24.bmp'), pygame.image.load('images/bullet_two_split_36.bmp'),
                            pygame.image.load('images/bullet_two_split_48.bmp'), pygame.image.load('images/bullet_two_split_60.bmp'),
                            pygame.image.load('images/bullet_two_split_72.bmp'), pygame.image.load('images/bullet_two_split_84.bmp'),
                            pygame.image.load('images/bullet_two_split_96.bmp'), pygame.image.load('images/bullet_two_split_108.bmp'),
                            pygame.image.load('images/bullet_two_split_120.bmp'), pygame.image.load('images/bullet_two_split_132.bmp'),
                            pygame.image.load('images/bullet_two_split_144.bmp'), pygame.image.load('images/bullet_two_split_156.bmp'),
                            pygame.image.load('images/bullet_two_split_168.bmp'), pygame.image.load('images/bullet_two_split_180.bmp'),
                            pygame.image.load('images/bullet_two_split_192.bmp'), pygame.image.load('images/bullet_two_split_204.bmp'),
                            pygame.image.load('images/bullet_two_split_216.bmp'), pygame.image.load('images/bullet_two_split_228.bmp'),
                            pygame.image.load('images/bullet_two_split_240.bmp'), pygame.image.load('images/bullet_two_split_252.bmp'),
                            pygame.image.load('images/bullet_two_split_264.bmp'), pygame.image.load('images/bullet_two_split_276.bmp'),
                            pygame.image.load('images/bullet_two_split_288.bmp'), pygame.image.load('images/bullet_two_split_300.bmp'),
                            pygame.image.load('images/bullet_two_split_312.bmp'), pygame.image.load('images/bullet_two_split_324.bmp'),
                            pygame.image.load('images/bullet_two_split_336.bmp'), pygame.image.load('images/bullet_two_split_348.bmp')]]]

    def __init__(self, screen, rocket, split):
        super().__init__()
        self.rocket = rocket
        self.angle = rocket.angle
        if split:
            self.split = 1
        else:
            self.split = 0
        self.image = Bullet.bullet_angle_images[self.split][rocket.player][rocket.angle // 12]
        self.screen = screen
        self.image_rect = self.image.get_rect()
        self.image_width = self.image_rect.width
        self.image_height = self.image_rect.height
        self.radius = int(self.image_rect.width * BULLET_RADIUS_RATIO)
        self.life_count = BULLET_LIFE_COUNT

        self.centerx = int(self.rocket.centerx)
        self.centery = int(self.rocket.centery)

        self.speedx = int(-120 * math.sin(self.rocket.angle / 180 * math.pi))
        self.speedy = int(-120 * math.cos(self.rocket.angle / 180 * math.pi))

    @classmethod
    def initialize_images(cls):
        for split_set in Bullet.bullet_angle_images:
            for player_set in split_set:
                for image in player_set:
                    image.set_colorkey(COLOR_BLACK)

    def move(self, *args):
        self.centerx = int((self.centerx + self.speedx / 8) % SCREEN_WIDTH)
        self.centery = int((self.centery + self.speedy / 8) % SCREEN_HEIGHT)


    def draw(self):
        # pygame.draw.circle(self.screen, (255, 255, 255), (self.centerx, self.centery), self.radius)
        self.screen.blit(self.image, (self.centerx - self.image_width / 2, self.centery - self.image_height / 2))

    def is_alive(self):
        return self.life_count > 0


class Asteroid():
    asteroid_images =  [
                        [
                            [pygame.image.load('images/asteroid_one_50x50_00.bmp'),
                            pygame.image.load('images/asteroid_one_50x50_01.bmp'),
                            pygame.image.load('images/asteroid_one_50x50_02.bmp')],

                            [pygame.image.load('images/asteroid_one_71x71_00.bmp'),
                            pygame.image.load('images/asteroid_one_71x71_01.bmp'),
                            pygame.image.load('images/asteroid_one_71x71_02.bmp')]],


                        [
                            [pygame.image.load('images/asteroid_two_50x50_00.bmp'),
                            pygame.image.load('images/asteroid_two_50x50_01.bmp'),
                            pygame.image.load('images/asteroid_two_50x50_02.bmp')],

                            [pygame.image.load('images/asteroid_two_71x71_00.bmp'),
                            pygame.image.load('images/asteroid_two_71x71_01.bmp'),
                            pygame.image.load('images/asteroid_two_71x71_02.bmp')]],


                        [
                            [pygame.image.load('images/asteroid_40x40_00.bmp'),
                             pygame.image.load('images/asteroid_40x40_01.bmp'),
                             pygame.image.load('images/asteroid_40x40_02.bmp')],

                            [pygame.image.load('images/asteroid_71x71_00.bmp'),
                             pygame.image.load('images/asteroid_71x71_01.bmp'),
                             pygame.image.load('images/asteroid_71x71_02.bmp')],

                            [pygame.image.load('images/asteroid_110x110_00.bmp'),
                             pygame.image.load('images/asteroid_110x110_01.bmp'),
                             pygame.image.load('images/asteroid_110x110_02.bmp')]]
                        ]



    def __init__(self, screen, rocket_one, rocket_two, old_asteroid, rocket_shooter, impact_bullet):
        super().__init__()
        self.valid = True
        self.screen = screen
        if rocket_shooter is not None:
            if old_asteroid.size_index == 0:
                self.valid = False
                return

            self.player = rocket_shooter.player
            if old_asteroid.size_index == 2:
                self.speedx = impact_bullet.speedx / 20
                self.speedy = impact_bullet.speedy / 20
            else:
                self.speedx = impact_bullet.speedx // 14
                self.speedy = impact_bullet.speedy // 14

            self.size_index = old_asteroid.size_index - 1

            self.image = Asteroid.asteroid_images[self.player][self.size_index][random.randint(0, 2)]
        else:
            player = 2
            self.speedx = -5 + random.randint(0, 10)
            self.speedy = -5 + random.randint(0, 10)
            self.size_index = 2
            self.image = Asteroid.asteroid_images[2][2][random.randint(0, 2)]




        self.image_rect = self.image.get_rect()
        self.image_width = self.image_rect.width
        self.image_height = self.image_rect.height
        self.radius = int(self.image_rect.width * ASTEROID_RADIUS_RATIO)

        if rocket_shooter is not None:
            self.centerx = old_asteroid.centerx
            self.centery = old_asteroid.centery


        else:
            self.__place_asteroid__(rocket_one, rocket_two)



    def get_angle(self):
        return int(math.atan2(-self.speedy, self.speedx) * 180 / math.pi - 90) % 360

    def __place_asteroid__(self, rocket_one, rocket_two):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        while True:
            if(
                math.fabs(x - rocket_one.centerx) > 100 and
                math.fabs(x - rocket_two.centerx) > 100 and
                x > 50 and x < SCREEN_WIDTH - 50 and
                math.fabs(y - rocket_one.centery) > 100 and
                math.fabs(y - rocket_two.centery) > 100 and
                y > 50 and y < SCREEN_HEIGHT - 50
            ):
                break
            x = x + 10
            y = y + 10
            #TODO use %
            if x > SCREEN_WIDTH:
                x = x - SCREEN_WIDTH
            if y > SCREEN_HEIGHT:
                y = y -SCREEN_HEIGHT

        self.centerx = x
        self.centery = y

    @classmethod
    def initialize_images(cls):
        for i in range(3):
            for images in Asteroid.asteroid_images[i]:
                for image in images:
                    image.set_colorkey((0,0,0,0))

    @classmethod
    def split_asteroid(cls, screen, rocket, old_asteroid, bullet):
        asteroid_one = Asteroid(screen, None, None, old_asteroid, rocket, bullet)
        asteroid_two = Asteroid(screen, None, None, old_asteroid, rocket, bullet)
        if asteroid_one.valid == False:
            return None, None


        asteroid_one.speedx = int(math.cos(15 / 360 * 2 * math.pi) * (asteroid_one.speedx) - math.sin(15 / 360 * 2 * math.pi) * (asteroid_one.speedy))
        asteroid_one.speedy = int(math.sin(15 / 360 * 2 * math.pi) * (asteroid_one.speedx) + math.cos(15 / 360 * 2 * math.pi) * (asteroid_one.speedy))


        asteroid_two.speedx = int(math.cos(-15 / 360 * 2 * math.pi) * (asteroid_two.speedx) - math.sin(-15 / 360 * 2 * math.pi) * (asteroid_two.speedy))
        asteroid_two.speedy = int(math.sin(-15 / 360 * 2 * math.pi) * (asteroid_two.speedx) + math.cos(-15 / 360 * 2 * math.pi) * (asteroid_two.speedy))

        return asteroid_one, asteroid_two

    def move(self):
        self.centerx = int((self.centerx + self.speedx) % SCREEN_WIDTH)
        self.centery = int((self.centery + self.speedy) % SCREEN_HEIGHT)

    def reverse_move(self, steps_count):
        self.centerx = int((self.centerx - steps_count * self.speedx) % SCREEN_WIDTH)
        self.centery = int((self.centery - steps_count * self.speedy) % SCREEN_HEIGHT)

    def draw(self):
        # pygame.draw.circle(self.screen, (255, 255, 255), (self.centerx, self.centery), self.radius)
        self.screen.blit(self.image, (self.centerx - self.image_width / 2, self.centery - self.image_height / 2))


def collides(objectA, objectB):
    return math.sqrt(math.pow(objectA.centerx - objectB.centerx, 2) + math.pow(objectA.centery - objectB.centery, 2)) < (
                objectA.radius + objectB.radius)

class Rocket_action(Enum):
    ROCKET_ONE_ACCELERATE = 1
    ROCKET_ONE_ROTATE_LEFT = 2
    ROCKET_ONE_ROTATE_RIGHT = 3
    ROCKET_ONE_SHOOT = 4
    ROCKET_ONE_SPLIT_SHOOT = 5
    ROCKET_TWO_ACCELERATE = 6
    ROCKET_TWO_ROTATE_LEFT = 7
    ROCKET_TWO_ROTATE_RIGHT = 8
    ROCKET_TWO_SHOOT = 9
    ROCKET_TWO_SPLIT_SHOOT = 10

class Rocket_base_action(Enum):
    ROTATE_LEFT = 1
    ROTATE_RIGHT = 2
    ACCELERATE = 3
    SHOT = 4
    SPLIT_SHOOT = 5
