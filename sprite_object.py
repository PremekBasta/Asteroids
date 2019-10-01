import pygame, random
import math
from enum import Enum


class Rect(pygame.sprite.Sprite):
    def __init__(self, width, height, color, value):
        super().__init__()
        self.image = pygame.Surface([2 * width, 2 * height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.colliderect = pygame.rect.Rect((0, 0), (width, height))
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

        self.image = Rocket.rocket_rotation_images[player][0]
        self.image_rect = self.image.get_rect()
        self.image_rect.centery = self.screen.get_height() / 2
        self.image_rect.centerx = self.screen.get_width() / 2
        if player == 1:
            self.image_rect.centerx = self.image_rect.centerx - 150
        else:
            self.image_rect.centerx = self.image_rect.centerx + 150
        collide_left = self.image_rect.left + 0.215 * self.image_rect.width
        collide_top = self.image_rect.top + 0.215 * self.image_rect.height
        collide_width = self.image_rect.width * 0.57
        collide_height = self.image_rect.height * 0.57
        self.collision_rect = pygame.Rect(collide_left, collide_top, collide_width, collide_height)

    def rotate_left(self):
        self.angle = self.angle + Rocket.rocket_angle_rotation + 360
        self.angle = self.angle % 360

    def rotate_right(self):
        self.angle = self.angle - Rocket.rocket_angle_rotation
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
        # pygame.draw.rect(self.screen, (255, 255, 255), self.collision_rect)
        self.screen.blit(Rocket.rocket_rotation_images[self.player][self.angle // 12], (self.image_rect.left, self.image_rect.top))



    def update(self, *args):
        self.image_rect.centerx = self.image_rect.centerx + self.speedx / 8
        if self.image_rect.centerx < 0:
            self.image_rect.centerx = self.screen.get_width()
        if self.image_rect.centerx > self.screen.get_width():
            self.image_rect.centerx = 0

        self.image_rect.centery = self.image_rect.centery + self.speedy / 8
        if self.image_rect.centery < 0:
            self.image_rect.centery = self.screen.get_height()
        if self.image_rect.centery > self.screen.get_height():
            self.image_rect.centery = 0

        self.collision_rect.center = self.image_rect.center


class Bullet(pygame.sprite.Sprite):
    bullet_angle_images = [[pygame.image.load('images/bullet_one_0.png'), pygame.image.load('images/bullet_one_12.png'),
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
                            pygame.image.load('images/bullet_two_336.png'), pygame.image.load('images/bullet_two_348.png')]]

    def __init__(self, screen, rocket):
        super().__init__()
        for image in Bullet.bullet_angle_images[0]:
            image.set_colorkey((0, 0, 0))
        self.image = Bullet.bullet_angle_images[rocket.player][rocket.angle // 12]
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rocket = rocket
        self.lifecount = 50
        self.rect.centerx = self.rocket.image_rect.centerx
        self.rect.centery = self.rocket.image_rect.centery

        self.speedx = int(-240 * math.sin(self.rocket.angle / 180 * math.pi))
        self.speedy = int(-240 * math.cos(self.rocket.angle / 180 * math.pi))


    def update(self, *args):
        self.rect.centerx = self.rect.centerx + self.speedx / 8
        if self.rect.centerx < 0:
            self.rect.centerx = self.screen.get_width()
        if self.rect.centerx > self.screen.get_width():
            self.rect.centerx = 0

        self.rect.centery = self.rect.centery + self.speedy / 8
        if self.rect.centery < 0:
            self.rect.centery = self.screen.get_height()
        if self.rect.centery > self.screen.get_height():
            self.rect.centery = 0

        self.lifecount = self.lifecount - 1


    def draw(self):
        self.screen.blit(self.image, (self.rect.left, self.rect.top))
        # pygame.draw.rect(self.screen, (255,255,255), (self.x, self.y, 20, 20))

    def is_alive(self):
        return self.lifecount > 0


class Asteroid(pygame.sprite.Sprite):
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
            print(f"old_asteroid.size_index: {old_asteroid.size_index}")
            if old_asteroid.size_index == 0:
                print("returning None")
                self.valid = False
                return

            self.player = rocket_shooter.player
            self.speedx = impact_bullet.speedx / 20
            self.speedy = impact_bullet.speedy / 20
            self.size_index = old_asteroid.size_index - 1
            print(self.size_index)
            self.image = Asteroid.asteroid_images[self.player][self.size_index][random.randint(0, 2)]
        else:
            player = 2
            self.speedx = -5 + random.randint(0, 10)
            self.speedy = -5 + random.randint(0, 10)
            self.size_index = 2
            self.image = Asteroid.asteroid_images[2][2][random.randint(0, 2)]


        self.image_rect = self.image.get_rect()

        if rocket_shooter is not None:
            self.image_rect.centerx = old_asteroid.image_rect.centerx
            self.image_rect.centery = old_asteroid.image_rect.centery
        else:
            self.__place_asteroid__(screen.get_width(), screen.get_height(), rocket_one.collision_rect, rocket_two.collision_rect)

        collide_left = self.image_rect.left + 0.215 * self.image_rect.width
        collide_top = self.image_rect.top + 0.215 * self.image_rect.height
        collide_width = self.image_rect.width * 0.57
        collide_height = self.image_rect.height * 0.57
        self.collision_rect = pygame.Rect(collide_left, collide_top, collide_width, collide_height)


    def __place_asteroid__(self, screen_width, screen_height, rocket_one_rect, rocket_two_rect):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        while True:
            if(
                math.fabs(x - rocket_one_rect.centerx) > 100 and
                math.fabs(x - rocket_two_rect.centerx) > 100 and
                x > 50 and x < screen_width - 50 and
                math.fabs(y - rocket_one_rect.centery) > 100 and
                math.fabs(y - rocket_two_rect.centery) > 100 and
                y > 50 and y < screen_height - 50
            ):
                break
            x = x + 10
            y = y + 10
            if x > screen_width:
                x = x - screen_width
            if y > screen_height:
                y = y -screen_height

        self.image_rect.centerx = x
        self.image_rect.centery = y

    @classmethod
    def initialize_images(cls):
        for i in range(3):
            for images in Asteroid.asteroid_images[i]:
                for image in images:
                    image.set_colorkey((0,0,0,0))

    def update(self):
        self.image_rect.centerx = self.image_rect.centerx + self.speedx
        if self.image_rect.centerx < 0:
            self.image_rect.centerx = self.screen.get_width()
        if self.image_rect.centerx > self.screen.get_width():
            self.image_rect.centerx = 0

        self.image_rect.centery = self.image_rect.centery + self.speedy
        if self.image_rect.centery < 0:
            self.image_rect.centery = self.screen.get_height()
        if self.image_rect.centery > self.screen.get_height():
            self.image_rect.centery = 0

        self.collision_rect.centerx = self.image_rect.centerx
        self.collision_rect.centery = self.image_rect.centery

    def draw(self):
        # pygame.draw.rect(self.screen, (255, 255, 255), self.collision_rect)
        self.screen.blit(self.image, (self.image_rect.left, self.image_rect.top))



class Rocket_action(Enum):
    ROCKET_ONE_ACCELERATE = 1
    ROCKET_ONE_ROTATE_LEFT = 2
    ROCKET_ONE_ROTATE_RIGHT = 3
    ROCKET_ONE_SHOOT = 4
    ROCKET_TWO_ACCELERATE = 5
    ROCKET_TWO_ROTATE_LEFT = 6
    ROCKET_TWO_ROTATE_RIGHT = 7
    ROCKET_TWO_SHOOT = 8
