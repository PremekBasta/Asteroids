import math
from constants import *


class SpaceObjectDTO():
    def __init__(self, radius, centerx, centery, speedx, speedy, angle, size_index = 0, player = 1, life_count = 0):
        self.radius = radius
        self.centerx = centerx
        self.centery = centery
        self.speedx = int(speedx)
        self.speedy = int(speedy)
        self.angle = angle
        self.size_index = size_index
        self.player = player
        self.life_count = life_count


    def move(self, steps_count = 1):
        # self.centerx = int((self.centerx + steps_count * self.speedx) % SCREEN_WIDTH)
        # self.centery = int((self.centery + steps_count * self.speedy) % SCREEN_HEIGHT)

        self.life_count = self.life_count - steps_count * 1

        self.centerx = int((self.centerx + steps_count * self.speedx / 8) % SCREEN_WIDTH)
        self.centery = int((self.centery + steps_count * self.speedy / 8) % SCREEN_HEIGHT)

    def reverse_move(self, steps_count = 1):
        self.centerx = int((self.centerx - steps_count * self.speedx / 8) % SCREEN_WIDTH)
        self.centery = int((self.centery - steps_count * self.speedy / 8) % SCREEN_HEIGHT)
        self.life_count = self.life_count + steps_count

    def is_alive(self):
        return self.life_count > 0

    def rotate_left(self, steps_count = 1):
        self.angle = self.angle +  steps_count * ROCKET_ANGLE_ROTATION + 360
        self.angle = self.angle % 360

    def rotate_right(self, steps_count = 1):
        self.angle = self.angle - steps_count * ROCKET_ANGLE_ROTATION
        self.angle = self.angle % 360


    def accelerate(self):
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


            if (self.speedy == 0):
                self.speedx = int(self.speedx * math.sqrt(math.pow(MAX_ROCKET_SPEED, 2) / math.pow(self.speedx, 2)))

            else:
                ratio = self.speedx / self.speedy
                self.speedy = int(math.sqrt(math.pow(MAX_ROCKET_SPEED, 2) / (math.pow(ratio, 2) + 1)))
                self.speedx = int(math.sqrt(math.pow(MAX_ROCKET_SPEED, 2) - math.pow(self.speedy, 2)))
                if minusx:
                    self.speedx = -self.speedx
                if minusy:
                    self.speedy = -self.speedy


    def collides(self, object):
        return math.sqrt(math.pow(self.centerx - object.centerx, 2) + math.pow(self.centery - object.centery, 2)) < (self.radius + object.radius)

def copy_object(o):
    return SpaceObjectDTO(o.radius, o.centerx, o.centery, o.speedx, o.speedy, o.angle, o.size_index, o.player, o.life_count)

def collides(objectA, objectB):
    # return np.sqrt(np.power(objectA.centerx - objectB.centerx, 2) + np.power(objectA.centery - objectB.centery, 2)) < (
    #             objectA.radius + objectB.radius)
    return math.sqrt(math.pow(objectA.centerx - objectB.centerx, 2) + math.pow(objectA.centery - objectB.centery, 2)) < (
            objectA.radius + objectB.radius)
