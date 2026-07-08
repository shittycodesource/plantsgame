import pygame
from settings.const import SCREEN_WIDTH, SCREEN_HEIGHT

class Won:
    def __init__(self, screen, game_state_manager, score):
        self.display_surface = screen
        
        self.game_state_manager = game_state_manager
        
        self.image = pygame.image.load('../assets/won.png').convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.image_rect = self.image.get_rect()

    def handle_keydown_events(self, event):
        if event.key == pygame.K_SPACE:
            # number = 0
            # with open('../local/level.txt', 'r') as file:
            #     number = int(file.readline())

            # with open('../local/level.txt', 'w') as file:
            #     file.write(str(number + 1))
            
            # with open('../local/score.txt', 'w') as file:
            #     file.write(str(globalvariables.score))

            # print('update lvl', number + 1)

            self.game_state_manager.set_state('level')


    def handle_click_events(self, event):
        pass

    def run(self):
        self.display_surface.blit(self.image, self.image_rect)