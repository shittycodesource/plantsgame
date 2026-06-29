import pygame

class Button:
    def __init__(self, data, screen, game_state_manager):
        self.display_surface = screen
        self.game_state_manager = game_state_manager

        self.data = data
        self.text = data['text']
        self.state = data['state']
        self.id = data['id']

        self.image_plain = pygame.image.load(f'../assets/{self.text.lower()}-btn.png').convert()
        self.image_plain = pygame.transform.scale(self.image_plain, (53*4, 20*4))

        self.image_hover = pygame.image.load(f'../assets/{self.text.lower()}-btn-hover.png').convert()
        self.image_hover = pygame.transform.scale(self.image_hover, (53*4, 20*4))

        self.image = self.image_plain
        self.rect = self.image.get_rect()
        
        self.rect.center = self.display_surface.get_rect().center
        self.rect.y = 240 + ((20*4) + 20) * data["id"] 

        self.is_hover = False

    def on_click(self, pos):
        if self.is_hover:
            self.game_state_manager.set_state(self.state)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def hover(self, pos):
        if self.rect.collidepoint(pos):
            self.image = self.image_hover
            self.is_hover = True
        else:
            self.image = self.image_plain
            self.is_hover = False

    def render(self):
        self.display_surface.blit(self.image, self.rect)