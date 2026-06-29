import pygame
from settings import *
import globalvariables

class Lost:
    def __init__(self, screen, game_state_manager):
        self.display_surface = screen
        self.game_state_manager = game_state_manager
        self.image = pygame.image.load('../assets/lost.png').convert()
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.image_rect = self.image.get_rect()

    def handle_keydown_events(self, event):
        if event.key == pygame.K_SPACE:
            number = 0
            with open('level.txt', 'w') as file:
                file.write(str(number))

            with open('score.txt', 'w') as file:
                file.write(str(globalvariables.score))
            self.game_state_manager.set_state('start')

    def handle_click_events(self, event):
        pass

    def run(self):
        self.display_surface.blit(self.image, self.image_rect)