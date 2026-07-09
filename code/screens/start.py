import pygame

from screens.button import Button
from settings.const import SCREEN_WIDTH, SCREEN_HEIGHT

class Start:
    def __init__(self, screen, game_state_manager, score):
        self.game_state_manager = game_state_manager
        self.score = score
        self.score_value = self.score.read_score()

        self.display_surface = screen
        self.image = pygame.image.load('../assets/menu.png').convert()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.image_rect = self.image.get_rect()

        self.title_image = pygame.image.load('../assets/menu-title.png').convert_alpha()
        self.title_image = pygame.transform.scale(self.title_image, (247 * 4, 22 * 4))
        
        self.title_image_rect = self.title_image.get_rect()
        self.title_image_rect.center = self.display_surface.get_rect().center
        self.title_image_rect.y = 40

        self.buttons = [ 
            { "text": "PlAY", "state": "level", "id": 0 },
            { "text": "Exit", "state": "exit",  "id": 1 }
        ]
        self.button_classes = [ Button(data, self.display_surface, self.game_state_manager) for data in self.buttons ]
        self.font = pygame.font.Font('../assets/Tiny5.ttf', 40)



    def check_hovers(self, pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for btn in self.button_classes:
            if btn.is_hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        for btn in self.button_classes:
            btn.hover(pos)
            

    def handle_click_events(self, event):
        for btn in self.button_classes:
            btn.on_click(event.pos)


    def handle_keydown_events(self, event):
        if event.key == pygame.K_SPACE:
            self.game_state_manager.set_state('level')


    def render_buttons(self):
        for btn in self.button_classes:
            btn.render()


    def render_score(self):
        text = self.font.render(f"Best score: {self.score_value}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))

        self.display_surface.blit(text, text_rect)


    def run(self):
        self.check_hovers(pygame.mouse.get_pos())

        self.display_surface.blit(self.image, self.image_rect)
        self.display_surface.blit(self.title_image, self.title_image_rect)

        self.render_buttons()
        self.render_score()