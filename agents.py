import random
from sprite_object import Rocket_action
import pygame

class Agent():
    def __init__(self, player_number):
        super().__init__()
        self.player_number = player_number

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

class Input_agent(Agent):
    def __init__(self, player_number):
        super().__init__(player_number)

    def choose_actions(self):
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

        return actions_one, actions_two
