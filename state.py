from dto import SpaceObjectDTO

class State:
    def __init__(self, neutral_asteroids,
                 player_one_rocket, player_one_asteroids, player_one_bullets,
                 player_two_rocket, player_two_asteroids, player_two_bullets):

        # Neutral asteroids
        self.neutral_asteroids = []
        for neutral_asteroid in neutral_asteroids:
            self.neutral_asteroids.append(SpaceObjectDTO(neutral_asteroid.collision_rect, neutral_asteroid.speedx,
                                                         neutral_asteroid.speedy, neutral_asteroid.screen.get_width(),
                                                         neutral_asteroid.screen.get_height(), neutral_asteroid.get_angle()))

        # Player ONE
        # Rocket ONE
        self.player_one_rocket = SpaceObjectDTO(player_one_rocket.collision_rect, player_one_rocket.speedx / 8,
                                                player_one_rocket.speedy / 8, player_one_rocket.screen.get_width(),
                                                player_one_rocket.screen.get_height(), player_one_rocket.angle)
        # Asteroids ONE
        self.player_one_asteroids = []
        for player_one_asteroid in player_one_asteroids:
            self.player_one_asteroids.append(SpaceObjectDTO(player_one_asteroid.collision_rect, player_one_asteroid.speedx,
                                                            player_one_asteroid.speedy, player_one_asteroid.screen.get_width(),
                                                            player_one_asteroid.screen.get_height(), player_one_asteroid.get_angle()))
        # Bullets ONE
        self.player_one_bullets = []
        for player_one_bullet in player_one_bullets:
            self.player_one_bullets.append(SpaceObjectDTO(player_one_bullet.collision_rect, player_one_bullet.speedx / 8,
                                                          player_one_bullet.speedy / 8, player_one_bullet.screen.get_width(),
                                                          player_one_bullet.screen.get_height(), player_one_bullet.angle))

        # Player TWO
        # Rocket TWO
        self.player_two_rocket = SpaceObjectDTO(player_two_rocket.collision_rect, player_two_rocket.speedx / 8,
                                                player_two_rocket.speedy / 8, player_two_rocket.screen.get_width(),
                                                player_two_rocket.screen.get_height(), player_two_rocket.angle)
        #Asteroids TWO
        self.player_two_asteroids = []
        for player_two_asteroid in player_two_asteroids:
            self.player_two_asteroids.append(SpaceObjectDTO(player_two_asteroid.collision_rect, player_two_asteroid.speedx,
                                                            player_two_asteroid.speedy, player_two_asteroid.screen.get_width(),
                                                            player_two_asteroid.screen.get_height(), player_two_asteroid.get_angle()))
        # Bullets TWO
        self.player_two_bullets = []
        for player_two_bullet in player_two_bullets:
            self.player_two_bullets.append(SpaceObjectDTO(player_two_bullet.collision_rect, player_two_bullet.speedx / 8,
                                                          player_two_bullet.speedy / 8, player_two_bullet.screen.get_width(),
                                                          player_two_bullet.screen.get_height(),player_two_bullet.angle))
