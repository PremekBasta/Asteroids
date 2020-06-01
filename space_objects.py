import math
from enum import Enum, IntEnum
from constants import *


random.seed(RANDOM_SEED)


class Rocket:
    def __init__(self, player):
        super().__init__()
        self.angle = 0
        self.speedx = 0
        self.speedy = 0
        self.player = player
        self.health = ROCKET_HEALTH
        self.radius = int(ROCKET_IMAGE_WIDTH * ROCKET_RADIUS_RATIO)
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
        # Modifies rocket's speed. Adds vector of current rocket's angle orientation to it's speed.
        # If resulting speed exceeds maximal speed limit speed vector will be shortened.
        # Angle orientation of resulting speed will be preserved, but speed vector will be shortened to maximal speed limit.
        x_acc_difference = int(math.sin(self.angle / 180 * math.pi) * 10 / 2)
        y_acc_difference = int(math.cos(self.angle / 180 * math.pi) * 10 / 2)
        if (self.speedx * x_acc_difference) > 0 and (self.speedy * y_acc_difference) > 0:
            self.speedx = self.speedx - 3 * x_acc_difference
            self.speedy = self.speedy - 3 * y_acc_difference
        elif (self.speedx * x_acc_difference) > 0 and self.speedy == 0:
            self.speedx = self.speedx - 3 * x_acc_difference
            self.speedy = self.speedy - y_acc_difference
        else:
            self.speedx = self.speedx - x_acc_difference
            self.speedy = self.speedy - y_acc_difference
        if math.sqrt(math.pow(self.speedx, 2) + math.pow(self.speedy, 2)) > MAX_ROCKET_SPEED:
            minusx = False
            minusy = False
            if self.speedx < 0:
                minusx = True
            if self.speedy < 0:
                minusy = True

            if self.speedy == 0:
                self.speedx = int(self.speedx * math.sqrt(math.pow(MAX_ROCKET_SPEED, 2) / math.pow(self.speedx, 2)))

            else:
                ratio = self.speedx / self.speedy
                self.speedy = int(math.sqrt(math.pow(MAX_ROCKET_SPEED, 2) / (math.pow(ratio, 2) + 1)))
                self.speedx = int(math.sqrt(math.pow(MAX_ROCKET_SPEED, 2) - math.pow(self.speedy, 2)))
                if minusx:
                    self.speedx = -self.speedx
                if minusy:
                    self.speedy = -self.speedy


    def move(self, *args):
        self.centerx = int((self.centerx + self.speedx / 8) % SCREEN_WIDTH)
        self.centery = int((self.centery + self.speedy / 8) % SCREEN_HEIGHT)


class Bullet():

    def __init__(self, rocket, split=0):
        super().__init__()
        self.rocket = rocket
        self.angle = int(rocket.angle)
        if split:
            self.split = 1
        else:
            self.split = 0

        self.radius = int(BULLET_IMAGE_WIDTH * BULLET_RADIUS_RATIO)
        self.life_count = BULLET_LIFE_COUNT

        self.centerx = int(self.rocket.centerx)
        self.centery = int(self.rocket.centery)

        self.speedx = int(-120 * math.sin(self.rocket.angle / 180 * math.pi))
        self.speedy = int(-120 * math.cos(self.rocket.angle / 180 * math.pi))

    def move(self):
        self.centerx = int((self.centerx + self.speedx / 8) % SCREEN_WIDTH)
        self.centery = int((self.centery + self.speedy / 8) % SCREEN_HEIGHT)
        self.life_count = self.life_count - 1

    def is_alive(self):
        return self.life_count > 0


class AsteroidSize(IntEnum):
    BIG = 2
    MIDDLE = 1
    SMALL = 0

class Asteroid():

    def __init__(self, rocket_one, rocket_two, old_asteroid, rocket_shooter, impact_bullet):
        super().__init__()
        self.valid = True
        if rocket_shooter is not None:
            if old_asteroid.size_index == AsteroidSize.SMALL:
                self.valid = False
                return

            self.player = rocket_shooter.player
            if old_asteroid.size_index == AsteroidSize.BIG:
                self.speedx = impact_bullet.speedx / 20
                self.speedy = impact_bullet.speedy / 20
            else:
                self.speedx = impact_bullet.speedx // 14
                self.speedy = impact_bullet.speedy // 14

            self.size_index = AsteroidSize(int(old_asteroid.size_index - 1))
            self.random_image_index = random.randint(0, 2)
        else:
            self.player = 2
            self.random_image_index = random.randint(0, 2)
            self.speedx = -5 + random.randint(0, 10)
            self.speedy = -5 + random.randint(0, 10)
            self.size_index = AsteroidSize.BIG

        if self.size_index == AsteroidSize.SMALL:
            self.image_height, self.image_width = ASTEROID_IMAGE_DIMENSION_SIZE_0, ASTEROID_IMAGE_DIMENSION_SIZE_0
        elif self.size_index == AsteroidSize.MIDDLE:
            self.image_height, self.image_width = ASTEROID_IMAGE_DIMENSION_SIZE_1, ASTEROID_IMAGE_DIMENSION_SIZE_1
        else:
            self.image_height, self.image_width = ASTEROID_IMAGE_DIMENSION_SIZE_2, ASTEROID_IMAGE_DIMENSION_SIZE_2

        self.radius = int(self.image_width * ASTEROID_RADIUS_RATIO)

        if rocket_shooter is not None:
            self.centerx = old_asteroid.centerx
            self.centery = old_asteroid.centery

        else:
            self.place_asteroid(rocket_one, rocket_two)

    def get_angle(self):
        return int(math.atan2(-self.speedy, self.speedx) * 180 / math.pi - 90) % 360

    def place_asteroid(self, rocket_one, rocket_two):
        global random
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        for i in range(10000):
            if (
                    math.fabs(x - rocket_one.centerx) > 100 and
                    math.fabs(x - rocket_two.centerx) > 100 and
                    50 < x < SCREEN_WIDTH - 50 and
                    math.fabs(y - rocket_one.centery) > 100 and
                    math.fabs(y - rocket_two.centery) > 100 and
                    50 < y < SCREEN_HEIGHT - 50
            ):
                break
            x = x + 10
            y = y + 10
            if x > SCREEN_WIDTH:
                x = x - SCREEN_WIDTH
            if y > SCREEN_HEIGHT:
                y = y - SCREEN_HEIGHT

        self.centerx = x
        self.centery = y

    @classmethod
    def split_asteroid(cls, rocket, old_asteroid, bullet):
        asteroid_one = Asteroid(None, None, old_asteroid, rocket, bullet)
        asteroid_two = Asteroid(None, None, old_asteroid, rocket, bullet)
        if not asteroid_one.valid:
            return None, None

        asteroid_one.speedx = int(math.cos(ASTEROID_SPLIT_ANGLE / 360 * 2 * math.pi) *
                                  asteroid_one.speedx - math.sin(ASTEROID_SPLIT_ANGLE / 360 * 2 * math.pi) *
                                  asteroid_one.speedy)
        asteroid_one.speedy = int(math.sin(ASTEROID_SPLIT_ANGLE / 360 * 2 * math.pi) *
                                  asteroid_one.speedx + math.cos(ASTEROID_SPLIT_ANGLE / 360 * 2 * math.pi) *
                                  asteroid_one.speedy)

        asteroid_two.speedx = int(math.cos(-ASTEROID_SPLIT_ANGLE / 360 * 2 * math.pi) *
                                  asteroid_two.speedx - math.sin(-ASTEROID_SPLIT_ANGLE / 360 * 2 * math.pi) *
                                  asteroid_two.speedy)
        asteroid_two.speedy = int(math.sin(-ASTEROID_SPLIT_ANGLE / 360 * 2 * math.pi) *
                                  asteroid_two.speedx + math.cos(-ASTEROID_SPLIT_ANGLE / 360 * 2 * math.pi) *
                                  asteroid_two.speedy)

        return asteroid_one, asteroid_two

    def move(self):
        self.centerx = int((self.centerx + self.speedx) % SCREEN_WIDTH)
        self.centery = int((self.centery + self.speedy) % SCREEN_HEIGHT)

    def reverse_move(self, steps_count):
        self.centerx = int((self.centerx - steps_count * self.speedx) % SCREEN_WIDTH)
        self.centery = int((self.centery - steps_count * self.speedy) % SCREEN_HEIGHT)



def collides(objectA, objectB):
    return math.sqrt(
        math.pow(objectA.centerx - objectB.centerx, 2) + math.pow(objectA.centery - objectB.centery, 2)) < (
                   objectA.radius + objectB.radius)


class RocketBaseAction(Enum):
    ROTATE_LEFT = 1
    ROTATE_RIGHT = 2
    ACCELERATE = 3
    SHOT = 4
    SPLIT_SHOOT = 5
