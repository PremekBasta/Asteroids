import pygame
import math
from enum import Enum
class Rect(pygame.sprite.Sprite):
    def __init__(self,width,height,color,value):
        super().__init__()
        self.image = pygame.Surface([2*width, 2*height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.colliderect = pygame.rect.Rect((0,0),(width,height))
        self.colliderect.midbottom = self.rect.midbottom
        self.value = value

    def update(self, *args):
        if self.value == 1:
            self.rect = self.rect.move(1, 1)
            self.colliderect.midbottom = self.rect.midbottom
        elif self.value == 2:
            self.rect = self.rect.move(-1, -1)
            self.colliderect.midbottom = self.rect.midbottom
        pass

class Rocket(pygame.sprite.Sprite):
    max_speed = 100
    rocket_angle_rotation = 12
    rocket_rotation_images = [pygame.image.load('images/rocket_0.png'), pygame.image.load('images/rocket_12.png'), pygame.image.load('images/rocket_24.png'),
                              pygame.image.load('images/rocket_36.png'), pygame.image.load('images/rocket_48.png'), pygame.image.load('images/rocket_60.png'),
                              pygame.image.load('images/rocket_72.png'), pygame.image.load('images/rocket_84.png'), pygame.image.load('images/rocket_96.png'),
                              pygame.image.load('images/rocket_108.png'), pygame.image.load('images/rocket_120.png'), pygame.image.load('images/rocket_132.png'),
                              pygame.image.load('images/rocket_144.png'), pygame.image.load('images/rocket_156.png'), pygame.image.load('images/rocket_168.png'),
                              pygame.image.load('images/rocket_180.png'), pygame.image.load('images/rocket_192.png'), pygame.image.load('images/rocket_204.png'),
                              pygame.image.load('images/rocket_216.png'), pygame.image.load('images/rocket_228.png'), pygame.image.load('images/rocket_240.png'),
                              pygame.image.load('images/rocket_252.png'), pygame.image.load('images/rocket_264.png'), pygame.image.load('images/rocket_276.png'),
                              pygame.image.load('images/rocket_288.png'), pygame.image.load('images/rocket_300.png'), pygame.image.load('images/rocket_312.png'),
                              pygame.image.load('images/rocket_324.png'), pygame.image.load('images/rocket_336.png'), pygame.image.load('images/rocket_348.png')]

    def __init__(self, screen):
        super().__init__()
        self.angle = 0
        self.x = 50
        self.y = 50
        self.speedx = 0
        self.speedy = 0
        self.screen = screen
        for image in Rocket.rocket_rotation_images:
            image.set_colorkey((0,0,0))
        self.image = Rocket.rocket_rotation_images[0]
        self.rect = self.image.get_rect()

    def rotate_left(self):
        self.angle = self.angle + Rocket.rocket_angle_rotation + 360
        self.angle = self.angle % 360

    def rotate_right(self):
        self.angle = self.angle - Rocket.rocket_angle_rotation
        self.angle = self.angle % 360

    def accelerate(self):
        self.speedx = self.speedx - int(math.sin(self.angle / 180 * math.pi) * 20 / 2)
        self.speedy = self.speedy - int(math.cos(self.angle / 180 * math.pi) * 20 / 2)
        print("speed x: " + str(self.speedx))
        print("speed y: " + str(self.speedy))
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
        self.screen.blit(Rocket.rocket_rotation_images[self.angle // 12], (self.rect.left, self.rect.top))
        # self.screen.blit(Rocket.rocket_rotation_images[self.angle // 12], (self.x + 10, self.y + 10))
        # pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, 20, 20))

    def update(self, *args):
        self.x = self.x + self.speedx / 8
        self.rect.centerx = self.rect.centerx + self.speedx / 8

        self.y = self.y + self.speedy / 8
        self.rect.centery = self.rect.centery + self.speedy / 8

class Bullet(pygame.sprite.Sprite):

    bullet_angle_images = [pygame.image.load('images/bullet_one_0.png'), pygame.image.load('images/bullet_one_12.png'), pygame.image.load('images/bullet_one_24.png'),
                           pygame.image.load('images/bullet_one_36.png'), pygame.image.load('images/bullet_one_48.png'), pygame.image.load('images/bullet_one_60.png'),
                           pygame.image.load('images/bullet_one_72.png'), pygame.image.load('images/bullet_one_84.png'), pygame.image.load('images/bullet_one_96.png'),
                           pygame.image.load('images/bullet_one_108.png'), pygame.image.load('images/bullet_one_120.png'), pygame.image.load('images/bullet_one_132.png'),
                           pygame.image.load('images/bullet_one_144.png'), pygame.image.load('images/bullet_one_156.png'), pygame.image.load('images/bullet_one_168.png'),
                           pygame.image.load('images/bullet_one_180.png'), pygame.image.load('images/bullet_one_192.png'), pygame.image.load('images/bullet_one_204.png'),
                           pygame.image.load('images/bullet_one_216.png'), pygame.image.load('images/bullet_one_228.png'), pygame.image.load('images/bullet_one_240.png'),
                           pygame.image.load('images/bullet_one_252.png'), pygame.image.load('images/bullet_one_264.png'), pygame.image.load('images/bullet_one_276.png'),
                           pygame.image.load('images/bullet_one_288.png'), pygame.image.load('images/bullet_one_300.png'), pygame.image.load('images/bullet_one_312.png'),
                           pygame.image.load('images/bullet_one_324.png'), pygame.image.load('images/bullet_one_336.png'), pygame.image.load('images/bullet_one_348.png')]

    def __init__(self, screen, rocket):
        super().__init__()
        self.image = Bullet.bullet_angle_images[rocket.angle // 12]
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rocket = rocket
        self.lifecount = 50
        self.rect.centerx = self.rocket.rect.centerx
        self.rect.centery = self.rocket.rect.centery

        self.speedx = int(-240 * math.sin(self.rocket.angle / 180 * math.pi))
        self.speedy = int(-240 * math.cos(self.rocket.angle / 180 * math.pi))
        # TODO borders

    def update(self, *args):
        self.rect.centerx = self.rect.centerx + self.speedx / 8
        self.rect.centery = self.rect.centery + self.speedy / 8
        self.lifecount = self.lifecount - 1

        # TODO substitute for constants

    def draw(self):
        self.screen.blit(self.image, (self.rect.left, self.rect.top))
        # pygame.draw.rect(self.screen, (255,255,255), (self.x, self.y, 20, 20))

    def is_alive(self):
        return self.lifecount > 0

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(100,100,50,50)
        self.speedx = 1
        self.speedy = 1

    def update(self):
        self.rect.centerx = self.rect.centerx + self.speedx
        self.rect.centery = self.rect.centery + self.speedy

    def draw(self):
        pygame.draw.rect(self.screen, (255,255,255), self.rect)



class Rocket_action(Enum):
    ROCKET_ONE_ACCELERATE = 1
    ROCKET_ONE_ROTATE_LEFT = 2
    ROCKET_ONE_ROTATE_RIGHT = 3
    ROCKET_ONE_SHOOT = 4
    ROCKET_TWO_ACCELERATE = 5
    ROCKET_TWO_ROTATE_LEFT = 6
    ROCKET_TWO_ROTATE_RIGHT = 7
    ROCKET_TWO_SHOOT = 8
